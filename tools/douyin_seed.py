# -*- coding: utf-8 -*-
"""把抖音图文的 OCR 文本切成面试题，跨库去重后写成题卡（先 indexed 待补答案）。

流程：douyin_ocr.jsonl → 分段切题 → 质量筛 → 与现有题库 Dice 去重 →
      候选清单 sources/douyin_candidates.json → （--write）写 content/*.md 骨架卡

用法：
  python tools/douyin_seed.py --dry            # 只看候选，不写文件
  python tools/douyin_seed.py --write --limit 30
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from nc_seed import module_of, dice  # noqa: E402

OCR_FILE = ROOT / "sources" / "douyin_ocr.jsonl"
CAND_FILE = ROOT / "sources" / "douyin_candidates.json"

NUM_PAT = re.compile(r"^\s*(?:[（(]?(\d{1,2})[)）.、．]|[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮]|"
                      r"[一二三四五六七八九十]+[、.．])\s*")
ASK = re.compile(r"[?？]|什么|为什么|为啥|怎么|如何|有哪些|区别|原理|是什么|讲讲|谈谈|"
                 r"说说|介绍一下|有哪些|是否|能否|可不可以|哪些")
BAD = re.compile(r"关注|点赞|收藏|转发|私信|扫码|主页|置顶|第\s*\d+\s*期|资料|"
                 r"整理|更新|领取|资料包|内推|扫码|福利|课程|训练营|加群|微信|公众号")
ANSWER_MARK = re.compile(r"^\s*(?:答案?|问题)\s*[：:]\s*")
QUESTION_MARK = re.compile(r"^\s*(?:问|问题|Q)\s*[：:]\s*")


def segments(text: str) -> list[tuple[str, list[str]]]:
    """把一页 OCR 文本切成 (题干, 要点行) 列表。

    三种版式都覆盖：
    A) 编号清单：「1. 题目」「2. 题目」——按编号切块；
    B) 问答配对：「问：…」「答：…」——答 并入上一题；
    C) 每行一题：没编号、每行以问号结尾——逐行切。
    折行由 douyin_ocr 的 _join_wrapped 提前合并，这里只做切分。
    """
    lines = [l.strip() for l in (text or "").splitlines() if l.strip()]
    if not lines:
        return []

    # A) 编号块
    numbered = [i for i, l in enumerate(lines) if NUM_PAT.match(l)]
    if len(numbered) >= 2:
        out: list[tuple[str, list[str]]] = []
        for k, start_i in enumerate(numbered):
            end_i = numbered[k + 1] if k + 1 < len(numbered) else len(lines)
            body = lines[start_i:end_i]
            head = NUM_PAT.sub("", body[0]).strip()
            pts = [NUM_PAT.sub("", b).strip() for b in body[1:]]
            out.append((head, [p for p in pts if p]))
        return out

    # B/C) 逐行：有「答：」并入上一题；否则按问号/疑问词起新题
    out = []
    cur_q, cur_pts = "", []
    for ln in lines:
        if ANSWER_MARK.match(ln):
            if cur_q:
                cur_pts.append(ANSWER_MARK.sub("", ln).strip())
            continue
        if ASK.search(ln) and (ln.endswith(("?", "？")) or ln.startswith(("问", "Q"))):
            if cur_q:
                out.append((cur_q, cur_pts))
            cur_q, cur_pts = QUESTION_MARK.sub("", ln).strip(), []
        elif cur_q:
            cur_pts.append(ln)
    if cur_q:
        out.append((cur_q, cur_pts))
    return out


def split_qa(head: str, pts: list[str]) -> tuple[str, list[str]]:
    """题干里带「答：」的直接拆开。"""
    m = ANSWER_MARK.match(head)
    if m:
        return head[:m.start()].strip(), [head[m.end():].strip()] + pts
    for i, p in enumerate(pts):
        m2 = ANSWER_MARK.match(p)
        if m2:
            return head, pts[:i] + [p[m2.end():].strip()] + pts[i + 1:]
    return head, pts


def usable(q: str) -> bool:
    if not (6 <= len(q) <= 60):
        return False
    if BAD.search(q):
        return False
    if not ASK.search(q):
        return False
    if re.match(r"^[\d\s.、]+$", q):
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ocr", default=str(OCR_FILE))
    ap.add_argument("--out", default=str(CAND_FILE))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dup", type=float, default=0.62, help="与题库相似度≥此值视为重复")
    ap.add_argument("--write", action="store_true", help="写入 content/ 骨架卡")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    if not Path(args.ocr).exists():
        print(f"缺少 {args.ocr}，先跑 tools/douyin_ocr.py", file=sys.stderr)
        return 1

    from build import load_questions
    bank = [(q["id"], q["title"]) for q in load_questions()]

    rows = [json.loads(l) for l in Path(args.ocr).read_text(encoding="utf-8").splitlines() if l.strip()]
    if args.limit:
        rows = rows[:args.limit]

    cands, seen_local = [], []
    for r in rows:
        for pi, page in enumerate(r.get("pages", [])):
            for head, pts in segments(page.get("text", "")):
                q, pts2 = split_qa(head, pts)
                if not usable(q):
                    continue
                # 与题库比对
                best, bs = "", 0.0
                for qid, t in bank:
                    s = dice(q, t)
                    if s > bs:
                        best, bs = qid, s
                if bs >= args.dup:
                    continue
                # 与本批已收的去重
                if any(dice(q, x["title"]) >= 0.85 for x in seen_local):
                    continue
                seen_local.append({"title": q})
                mod, sub = module_of(q + " " + " ".join(pts2))
                cands.append({
                    "title": q, "points": pts2[:6], "module": mod, "sub": sub,
                    "priority": "P1", "near": best, "sim": round(bs, 2),
                    "conf": page.get("conf", 0), "img": page.get("img", ""),
                    "aweme_id": r.get("aweme_id", ""), "url": r.get("url", ""),
                    "desc": r.get("desc", ""), "date": r.get("date", ""),
                })

    Path(args.out).write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"候选 {len(cands)} 道 → {args.out}")
    if cands:
        print("样例：")
        for c in cands[:12]:
            print(f"  [{c['module']}/{c['sub']}] {c['title'][:38]}  (近似 {c['near']} {c['sim']}, conf {c['conf']})")
    if args.write:
        print("写卡功能需人工确认题目质量后再开（避免污染题库）；先用 --dry 看清单。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
