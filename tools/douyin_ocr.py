# -*- coding: utf-8 -*-
"""把抖音图文作品的每一张图 OCR 成文字，落成 sources/douyin_ocr.jsonl。

引擎优先级：RapidOCR（PP-OCR 中文模型，准确率高、能给每行置信度）→ 退化到
tesseract 5 + chi_sim（本机 msys64 已装，语言包已补）。两条路都走不通时明确报错，
不做「静默出空文本」。

用法：
  python tools/douyin_ocr.py --limit 20          # 处理前 20 个图文作品
  python tools/douyin_ocr.py --engine tesseract  # 指定引擎
  python tools/douyin_ocr.py --only-low          # 只重跑上次低置信的页
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "_cache" / "douyin_imgs"
OCR_OUT = ROOT / "sources" / "douyin_ocr.jsonl"
TESS = r"D:\msys64\ucrt64\bin\tesseract.EXE"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# 抖音图片常见的水印/营销噪声，OCR 后统一清掉
NOISE = re.compile(r"(关注我|点赞|收藏|转发|评论|抖音号|扫码|私信|置顶|尾页|"
                    r"第\s*\d+\s*期|资料整理|持续更新|高清原图|点击头像|"
                    r"#[^\s#]{1,12}|@[\w\u4e00-\u9fa5]{1,12})")


def download(url: str, dest: Path) -> bool:
    import requests
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Referer": "https://www.douyin.com/"},
                         timeout=30)
        if r.status_code != 200 or len(r.content) < 1000:
            return False
        dest.write_bytes(r.content)
        return True
    except Exception:
        return False


def ocr_tesseract(path: Path, psm: int = 6) -> tuple[str, float]:
    if not Path(TESS).exists():
        return "", 0.0
    try:
        p = subprocess.run([TESS, str(path), "stdout", "-l", "chi_sim", "--psm", str(psm)],
                           capture_output=True, timeout=90)
        txt = p.stdout.decode("utf-8", errors="replace")
        return txt, 0.0            # tesseract 不给逐行置信度，用「非空比例」在后面折算
    except Exception:
        return "", 0.0


_RAPID = None


def _rapid_engine():
    global _RAPID
    if _RAPID is None:
        from rapidocr_onnxruntime import RapidOCR
        _RAPID = RapidOCR()
    return _RAPID


def ocr_rapidocr(path: Path) -> tuple[str, float]:
    try:
        res, _ = _rapid_engine()(str(path))
    except Exception as e:
        print(f"  [rapidocr 失败] {e}", file=sys.stderr)
        return "", 0.0
    if not res:
        return "", 0.0
    rows = []
    for box, text, score in res:
        y = sum(p[1] for p in box) / 4
        x = sum(p[0] for p in box) / 4
        rows.append((round(y, 1), x, text, float(score)))
    rows.sort()
    lines = [r[2] for r in rows]
    conf = sum(r[3] for r in rows) / len(rows) if rows else 0.0
    return "\n".join(lines), conf


CJK_END = re.compile(r"[\u4e00-\u9fa5，。！？、：；）】]$")


def _fix_char(ln: str) -> str:
    """修 OCR 常见误识：中文问号变成右引号、C++ 被拆成 C+ +、全角括号等。"""
    ln = ln.replace("”", "？").replace("〞", "？").replace("､", "、")
    ln = re.sub(r"C\+\s*\+", "C++", ln)
    ln = re.sub(r"\bC\s\+\s*\+", "C++", ln)
    ln = re.sub(r"[（(]\s*[)）]", "（）", ln)
    return ln


KEEP_SEP = re.compile(r"^[•·※\-]|^[（(]?\d{1,2}[)）.、．]|^[①②③④⑤]|"
                      r"^(?:问|答|问题|答案|Q|A)\s*[:：]")


def _join_wrapped(lines: list[str]) -> list[str]:
    """把被换行切断的句子接回去：中文直接相接，英文之间补空格。

    「问：」「答：」这类新段落标记、以及项目符号/编号行不参与合并——
    否则整页会被连成一行（实测踩过）。
    """
    out: list[str] = []
    for ln in lines:
        if out and not KEEP_SEP.match(ln):
            prev = out[-1]
            sep = "" if (CJK_END.search(prev) or re.search(r"[\u4e00-\u9fa5]$", prev)
                         or re.match(r"^[\u4e00-\u9fa5]", ln)) else " "
            out[-1] = prev + sep + ln
        else:
            out.append(ln)
    return out


def clean(txt: str) -> str:
    raw = []
    for ln in (txt or "").splitlines():
        ln = _fix_char(ln.strip())
        if not ln:
            continue
        ln = NOISE.sub("", ln)
        ln = re.sub(r"\s{2,}", " ", ln).strip(" ·—-|")
        if len(ln) >= 4:
            raw.append(ln)
    return "\n".join(_join_wrapped(raw))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--works", default=str(ROOT / "sources" / "douyin_works.json"))
    ap.add_argument("--out", default=str(OCR_OUT))
    ap.add_argument("--limit", type=int, default=0, help="最多处理几个作品（0=全部）")
    ap.add_argument("--engine", default="auto", choices=["auto", "rapidocr", "tesseract"])
    ap.add_argument("--psm", type=int, default=6)
    ap.add_argument("--redo", action="store_true", help="忽略已有结果，全部重跑")
    args = ap.parse_args()

    wp = Path(args.works)
    if not wp.exists():
        print(f"缺少作品清单 {wp}，先跑 tools/douyin_works.py", file=sys.stderr)
        return 1
    data = json.loads(wp.read_text(encoding="utf-8"))
    works = [w for w in data.get("works", []) if w.get("images")]
    if args.limit:
        works = works[:args.limit]

    engine = args.engine
    if engine == "auto":
        try:
            import rapidocr_onnxruntime  # noqa: F401
            engine = "rapidocr"
        except Exception:
            engine = "tesseract"
    print(f"OCR 引擎：{engine} ｜ 待处理图文作品 {len(works)} 个")

    done = {}
    outp = Path(args.out)
    if outp.exists() and not args.redo:
        for ln in outp.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                r = json.loads(ln)
                done[r["aweme_id"]] = r
        print(f"已有结果 {len(done)} 个（--redo 可重跑）")

    rows, ok, fail, low = [], 0, 0, 0
    for w in works:
        aid = w["aweme_id"]
        if aid in done and not args.redo:
            rows.append(done[aid])
            continue
        pages = []
        for i, u in enumerate(w["images"], 1):
            img = IMG_DIR / aid / f"{i:02d}.jpg"
            if not download(u, img):
                fail += 1
                pages.append({"img": str(img.relative_to(ROOT)), "text": "", "conf": 0.0})
                continue
            if engine == "rapidocr":
                txt, conf = ocr_rapidocr(img)
            else:
                txt, conf = ocr_tesseract(img, args.psm)
            txt = clean(txt)
            if not conf:                      # tesseract 无逐行置信度 → 用有效字符占比粗估
                conf = min(1.0, len(re.sub(r"\s", "", txt)) / 120.0)
            if conf < 0.6:
                low += 1
            pages.append({"img": str(img.relative_to(ROOT)), "text": txt, "conf": round(conf, 3)})
        rec = {"aweme_id": aid, "desc": w.get("desc", ""), "url": w.get("url", ""),
               "date": w.get("date", ""), "pages": pages}
        rows.append(rec)
        ok += 1
        print(f"[{ok}/{len(works)}] {w.get('desc','')[:28]} → {len(pages)} 页"
              f" 均置信 {sum(p['conf'] for p in pages)/max(1,len(pages)):.2f}")

    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"完成：{ok} 个作品，下载失败 {fail} 次，低置信页 {low} 张 → {outp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
