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


def norm(s: str) -> str:
    return re.sub(r"[\s，。、？！：:（）()\[\]【】“”\"'…·—+,.?《》/\\]", "", s or "")


def find_dup(q: str, bank: list, thr: float):
    """判重：先看包含关系（短题干更准），再看 Dice 相似度。

    只用 Dice 时，短标题（「进程和线程的核心区别是什么？」vs 题库 0.57）会擦着阈值漏判，
    包含关系能把这类「同题不同措辞」挡住。
    """
    nq = norm(q)
    for qid, t in bank:
        nt = norm(t)
        if len(nq) >= 6 and len(nt) >= 6 and (nq in nt or nt in nq):
            return qid, 1.0, "包含"
        s = dice(q, t)
        if s >= thr:
            return qid, s, "相似"
    return "", 0.0, ""


GENERIC = re.compile(
    r"是什么|为什么|为啥|怎么|如何|有哪些|哪些|区别|原理|讲讲|谈谈|说说|介绍一下|是否|能否|"
    r"可不可以|请问|简述|需要|实现|方式|方法|作用|特点|场景|流程|步骤|优化|设计|处理|使用|支持|"
    r"出现|理解|掌握|核心|过程|机制|什么|哪些|以及|并且|以及|和|与|的|吗|呢|它|这|那|个|些|"
    r"问题|情况|内容|部分|地方|时候|时间|东西|方式|目前|现在|一般|具体|主要|相关|不同|一样|"
    r"参数|配置|关键|设置|常见|典型|实际|具体|真正|本质|深入|扩展|进阶")
TERM_SPLIT = re.compile(r"[\s，。、？！：:（）()\[\]【】/、,.;；|｜]+")
TERM_OK = re.compile(r"[\u4e00-\u9fa5A-Za-z0-9+#]")


TRIM = "是的了把和与及或吗呢啊呀把被让给从向对跟给"


def _terms(text: str) -> list[str]:
    """剥掉通用词后剩下的技术名词（2 字以上）。

    还要把首尾的虚词剪掉：「什么|是虚拟内存」→「虚拟内存」——
    否则「是什么」被拆成「什么」+「是」，术语就带上了无意义的「是」字。
    """
    core = GENERIC.sub("|", text or "")
    out = []
    for t in TERM_SPLIT.split(core):
        t = t.strip(TRIM)
        if len(t) >= 2 and TERM_OK.search(t) and t not in GENERIC.pattern:
            out.append(t)
    return out


def topic_match(q: str, bank: list, limit: int = 2):
    """主题级疑似匹配：用题库自身出现的术语与问题求交集。

    纯字符串相似度对「同题不同措辞」会漏判（「进程和线程的核心区别是什么？」vs
    「进程和线程有什么区别？」），但主题词交集能抓住。**只标记不丢弃**——
    「零拷贝」一个词能命中多道不同角度的题，必须留给人判断。
    """
    q_terms = set(_terms(q))
    if not q_terms:
        return []
    hits, seen = [], set()
    for qid, t in bank:
        t_terms = set(_terms(t))
        # 子串包含也算（题库里「零拷贝做」与问题里的「零拷贝」是同一个点）
        shared = {a for a in q_terms for b in t_terms if a == b or (len(a) >= 3 and a in b) or (len(b) >= 3 and b in a)}
        if shared:
            hits.append((qid, "/".join(sorted(shared))[:18]))
            seen.add(qid)
            if len(hits) >= limit:
                break
    return hits


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
                # 与题库比对（含包含关系，短题干更准）
                best, bs, how = find_dup(q, bank, args.dup)
                if bs >= args.dup:
                    continue
                topics = topic_match(q, bank)
                # 与本批已收的去重
                if any(dice(q, x["title"]) >= 0.85 for x in seen_local):
                    continue
                seen_local.append({"title": q})
                mod, sub = module_of(q + " " + " ".join(pts2))
                cands.append({
                    "title": q, "points": pts2[:6], "module": mod, "sub": sub,
                    "priority": "P1", "near": best, "sim": round(bs, 2), "dup_by": how,
                    "topic_near": topics,
                    "conf": page.get("conf", 0), "img": page.get("img", ""),
                    "aweme_id": r.get("aweme_id", ""), "url": r.get("url", ""),
                    "desc": r.get("desc", ""), "date": r.get("date", ""),
                })

    Path(args.out).write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"候选 {len(cands)} 道 → {args.out}")
    flagged = [c for c in cands if c.get("topic_near")]
    if flagged:
        print(f"其中 {len(flagged)} 道与题库同主题（需人工判断是否值得单独成题）：")
    if cands:
        print("样例：")
        for c in cands[:12]:
            tp = ("｜同主题:" + ",".join(f"{q}({t})" for q, t in c.get("topic_near", []))) if c.get("topic_near") else ""
            print(f"  [{c['module']}/{c['sub']}] {c['title'][:34]}  (近似 {c['near']} {c['sim']}, conf {c['conf']}){tp}")
    if args.write:
        print("写卡功能需人工确认题目质量后再开（避免污染题库）；先用 --dry 看清单。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
