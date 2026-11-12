#!/usr/bin/env python3
"""牛客面经采集器（合规模式）。

只做三件事：
  --feed N    拉取「最新」面经流（默认前 N 页），按 contentId 去重存本地缓存
  --fetch K   对命中目标公司+岗位的帖子，用无头浏览器取正文，解析出题目
  --build     把缓存里的帖子整理成题库可用的索引（不存原帖正文、不存作者信息）

合规边界（写在代码里，不是注释里）：
  * 提交进仓库的只有：题目摘要、公司/岗位/轮次、原帖链接、抓取日期
  * 原帖正文只落在 gitignore 的 _cache/ 里，用于解析，不入库
  * 不存发帖人昵称 / 学校（个人信息）
  * 串行请求，API 间隔 1s，渲染间隔 1.5s，单日上限 300 次渲染
"""
from __future__ import annotations
import argparse, csv, json, re, subprocess, sys, time, unicodedata
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "_cache"
POSTS = CACHE / "nc_posts"
FEED = CACHE / "nc_feed.jsonl"
DAILY = CACHE / "nc_daily.json"

API = "https://gw-c.nowcoder.com/api/sparta/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
DAILY_CAP = 300
API_SLEEP, RENDER_SLEEP = 1.0, 1.5

# 目标公司注册表：companies/targets.json 是唯一来源（tier core+watch）。
# JSON 顺序即匹配顺序，"关键词更具体"的公司必须排在会吞掉它的公司之前
# （如 联影智能 → 联影医疗；西门子（工业）用负向先行排除 西门子医疗）。
def load_registry() -> list[tuple[str, list[str]]]:
    tf = ROOT / "companies" / "targets.json"
    if tf.exists():
        d = json.loads(tf.read_text(encoding="utf-8"))
        return [(c["name"], c.get("nc_keywords") or []) for c in d["companies"]
                if c.get("nc_keywords")]
    # 兜底：注册表缺失时退回内置 9 家
    return [
        ("Momenta", [r"momenta", r"魔门塔"]),
        ("华为",    [r"华为", r"huawei"]),
        ("蔚来",    [r"蔚来"]),
        ("小鹏",    [r"小鹏", r"xpeng"]),
        ("地平线",  [r"地平线", r"horizon"]),
        ("联影",    [r"联影"]),
        ("迈瑞",    [r"迈瑞", r"mindray"]),
        ("ABB",     [r"\bABB\b"]),
        ("追觅",    [r"追觅", r"dreame"]),
    ]


REGISTRY = load_registry()

ROLE_WORDS = [
    "C++", "嵌入式", "SDK", "推理", "部署", "机器人", "ROS", "算法", "后端",
    "自动驾驶", "固件", "驱动", "感知", "SLAM", "Linux", "软件工程师", "软件开发",
    "机械", "结构", "电机", "测试开发", "图像", "BSP", "单片机", "底层软件",
]


def match_company(text: str) -> str | None:
    """返回命中的公司名；歧义词用大小写敏感匹配。"""
    for comp, pats in REGISTRY:
        for pat in pats:
            flags = 0 if (pat[0].isupper() or pat.startswith("\\b") or pat[:1].isascii()
                          and pat.lower() != pat) else re.I
            if re.search(pat, text, flags):
                return comp
    return None
ROUND_RE = re.compile(r"(五面|四面|三面|二面|一面|终面|交叉面|主管面|HR面|hr面|人事面)")
STOP_MARKS = {"评论", "点赞", "收藏", "真题解析", "邀请牛友回答"}
STOP_PREFIX = re.compile(r"^(点赞成功|评论成功|收藏成功|送花成功|关注成功)")
JUNK_RE = re.compile(
    r"^(复制链接|微信|QQ|微博|分享.*|暂不保存|保存图片|屏蔽.*|关注.*|举报|取消|确定|"
    r"指定话题|指定圈子|发送|取消关注|发私信|发布于|已编辑|一键发评|快捷表情|畅所欲言.*)$")


def http_json(path: str, body: dict) -> dict:
    """POST JSON 到 sparta 网关（见 docs/nowcoder_feasibility.md 的接口清单）。"""
    import urllib.request
    req = urllib.request.Request(
        API + path, data=json.dumps(body).encode(),
        headers={"User-Agent": UA, "Content-Type": "application/json",
                 "Origin": "https://www.nowcoder.com",
                 "Referer": "https://www.nowcoder.com/interview/center"},
        method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def load_jsonl(path: Path) -> dict:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            out[d["id"]] = d
    return out


def append_jsonl(path: Path, items: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


def daily_count() -> int:
    today = date.today().isoformat()
    d = json.loads(DAILY.read_text(encoding="utf-8")) if DAILY.exists() else {}
    return d.get(today, 0)


def bump_daily(n: int):
    today = date.today().isoformat()
    d = json.loads(DAILY.read_text(encoding="utf-8")) if DAILY.exists() else {}
    if d.get("_day") != today:
        d = {"_day": today}
    d[today] = d.get(today, 0) + n
    DAILY.parent.mkdir(parents=True, exist_ok=True)
    DAILY.write_text(json.dumps(d), encoding="utf-8")


# ---------------------------------------------------------------- --feed
def cmd_feed(pages: int) -> int:
    known = load_jsonl(FEED)
    new, matched = 0, 0
    for p in range(1, pages + 1):
        try:
            resp = http_json("job-experience/experience/job/list",
                             {"page": p, "pageSize": 30, "orderBy": 0})
        except Exception as e:
            print(f"  第 {p} 页失败：{e}")
            break
        recs = (resp.get("data") or {}).get("records") or []
        items = []
        for r in recs:
            cd = r.get("contentData") or {}
            cid = cd.get("id")
            if not cid or cid in known:
                continue
            items.append({
                "id": str(cid),
                "uuid": str(cd.get("uuid") or ""),
                # 实测：/discuss/{数字id} 能渲染正文；/feed/main/detail/ 对列表里的帖子不行
                "url": f"https://www.nowcoder.com/discuss/{cid}",
                "title": (cd.get("title") or "").strip(),
                "snippet": (cd.get("content") or "").strip()[:303],
            })
        if items:
            append_jsonl(FEED, items)
            new += len(items)
            for it in items:
                if match_company(it["title"] + " " + it["snippet"]):
                    matched += 1
        print(f"  第 {p:3d} 页：{len(recs):2d} 条，新 {len(items):2d}，命中 {sum(1 for it in items if match_company(it['title']+' '+it['snippet']))}")
        time.sleep(API_SLEEP)
    total = len(load_jsonl(FEED))
    print(f"累计缓存 {total} 条（本轮新 {new}，命中目标公司 {matched}）")
    return 0


# ---------------------------------------------------------------- --fetch
def find_edge() -> str:
    for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"):
        if Path(p).exists():
            return p
    raise SystemExit("找不到 Edge")


def render(url: str) -> str:
    """无头渲染，返回可见文本行。约 4s/篇。"""
    edge = find_edge()
    proc = subprocess.run(
        [edge, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=12000", "--dump-dom", url],
        capture_output=True, timeout=90)
    html_ = proc.stdout.decode("utf-8", errors="replace")
    html_ = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", "\n", html_)
    import html as _h
    txt = _h.unescape(txt)          # 实测「点赞成功，聊一聊 &gt;」会漏过精确匹配
    return [x.strip() for x in txt.split("\n") if x.strip()]


def extract_post(lines: list[str], title: str) -> dict:
    """从渲染文本里定位正文与元信息。"""
    # 标题在可见文本里通常只出现一次；取它最后一次出现（前面是元信息）
    ti = max(i for i, x in enumerate(lines) if x == title) if title in lines else -1
    date_raw, school_job = "", ""
    if ti > 0:
        for j in range(max(0, ti - 8), ti):
            x = lines[j]
            if re.search(r"今天|昨天|刚刚|分钟前|小时前|天前|\d{4}-\d{1,2}-\d{1,2}", x):
                date_raw = x
    # 正文：标题后到第一个停止标记
    body: list[str] = []
    for x in lines[ti + 1:] if ti >= 0 else []:
        if x in STOP_MARKS or STOP_PREFIX.match(x):
            break
        if JUNK_RE.match(x) or len(x) < 2:
            continue
        body.append(x)
    return {"date_raw": date_raw, "body": body}


def parse_questions(body: list[str]) -> tuple[list[dict], list[str], str | None]:
    """按轮次切分，识别题目行。返回 (questions, reverses, round)。"""
    questions, reverses = [], []
    cur_round, cur_q, answer_buf = None, None, []
    ROUND = re.compile(r"^(五面|四面|三面|二面|一面|终面|交叉面|主管面|HR面|hr面|人事面)")
    Q_START = re.compile(r"^([-*•·]|\d{1,2}[.、]|[Qq问][:：]|问)[:：]?\s*")
    A_START = re.compile(r"^(答|A)[:：]\s*")
    IMPERATIVE = re.compile(r"请|介绍一下|介绍下|讲讲|说说|谈谈|聊一聊|描述|自我介绍")
    WHY = re.compile(r"什么|为什么|怎么|如何|哪些|哪几|区别|多少|多少种|多久|有没有|是否|会不会")

    def flush():
        nonlocal cur_q, answer_buf
        if cur_q:
            questions.append({"round": cur_round, "q": cur_q,
                              "answer_hint": " ".join(answer_buf)[:200] or None})
        cur_q, answer_buf = None, []

    for raw in body:
        line = raw.strip()
        m = ROUND.match(line)
        if m:
            flush()
            cur_round = m.group(1)
            continue
        if A_START.match(line):
            if cur_q:
                answer_buf.append(A_START.sub("", line))
            continue
        core = Q_START.sub("", line)
        # 广告/课程推荐（实测混入「跟着牛客那个《xx指南》过的」这类段落）
        if re.search(r"《|》|跟着牛客|完全指南|牛客那个|优惠券|http", line):
            continue
        # 代码注释/伪代码（实测来自机考解析帖的代码块）
        if re.match(r"^(//|/\*|\*|#include|for\s*\(|if\s*\(|while\s*\(|return\b|std::|printf|scanf|int\s+main)", line):
            continue
        # 笔试解析帖的元文本与答案分析（实测：「输入描述（原文未单独给出…」「其余选项分别错误描述了…」）
        if re.match(r"^(输入描述|输出描述|样例|示例|解题思路|参考代码|正确答案|其余选项|答案解析|思路[：:])", line):
            continue
        if re.search(r"考察维度|心得|Top ?\d|纸上谈兵", line) and len(line) > 30:
            continue
        if re.match(r"^[一二三四五六七八九十]+[、.]", line) and len(line) > 20:
            continue
        is_q = (line.endswith(("？", "?")) or WHY.search(core) or IMPERATIVE.search(core))
        # 无问号的超长陈述多半是叙事（实测「可那个会只是知道它是什么…」）
        if is_q and not line.endswith(("？", "?")) and len(core) > 45:
            continue
        # 叙事开头（转折/回忆），带疑问词也是讲故事
        if re.match(r"^[但可而而且所以然后后来说起来说白毕竟那会儿当时]", line) and not line.endswith(("？", "?")):
            continue
        if is_q and 8 <= len(core) <= 120 and core.count(" ") < 8:
            flush()
            cur_q = core
            continue
        # 长句里带追问（"……，追问：xxx？"）
        if "？" in line and len(line) <= 200 and ("追问" in line or "接着问" in line):
            flush()
            cur_q = line
            continue
        if cur_q and len(line) <= 120:
            answer_buf.append(line)
    flush()
    # 反问段
    rev = False
    for raw in body:
        if re.match(r"^反问", raw.strip()):
            rev = True
            continue
        if rev and (raw.strip() in STOP_MARKS or STOP_PREFIX.match(raw.strip())):
            break
        if rev:
            core = Q_START.sub("", raw.strip())
            if 6 <= len(core) <= 120 and (core.endswith("？") or WHY.search(core)):
                reverses.append(core)
            if re.match(r"^(一面|二面|三面|四面|HR面)", raw.strip()):
                rev = False
    return questions, reverses, cur_round


def cmd_fetch(limit: int) -> int:
    feed = load_jsonl(FEED)
    done = {p.stem for p in POSTS.glob("*.json")} if POSTS.exists() else set()
    used = daily_count()
    print(f"缓存 {len(feed)} 帖，已取正文 {len(done)}，今日已渲染 {used}/{DAILY_CAP}")
    cand = []
    for it in feed.values():
        if it["id"] in done:
            continue
        comp = match_company(it["title"] + " " + it["snippet"])
        if comp:
            cand.append((comp, it))
    cand.sort(key=lambda x: x[1]["id"])
    print(f"待取正文 {len(cand)} 帖，本轮上限 {limit}")
    n = 0
    for comp, it in cand:
        if n >= limit or used >= DAILY_CAP:
            break
        url = "https://www.nowcoder.com/discuss/" + it["id"]
        try:
            lines = render(url)
        except Exception as e:
            print(f"  ✗ {it['id']} 渲染失败：{e}")
            continue
        info = extract_post(lines, it["title"])
        qs, revs, rnd = parse_questions(info["body"])
        # 轮次优先从标题找（实测「地平线嵌入式一面面经」的轮次在标题里）
        tm = ROUND_RE.search(it["title"])
        if tm and not rnd:
            rnd = tm.group(1)
        if not rnd and "笔试" in it["title"]:
            rnd = "笔试"
        POSTS.mkdir(parents=True, exist_ok=True)
        (POSTS / f"{it['id']}.json").write_text(json.dumps({
            "id": it["id"], "url": url, "company": comp,
            "title": it["title"], "date_raw": info["date_raw"],
            "round": rnd, "questions": qs, "reverses": revs,
            "body": info["body"][:400],   # 留正文行，改解析规则后可免重渲染
            "collected_at": datetime.now().isoformat(timespec="seconds"),
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
        used += 1
        print(f"  ✓ [{comp}] {it['title'][:36]:38s} 题目 {len(qs):2d} 反问 {len(revs)}")
        time.sleep(RENDER_SLEEP)
    bump_daily(n)
    print(f"本轮渲染 {n} 篇")
    return 0


# ---------------------------------------------------------------- --papers
def cmd_papers() -> int:
    rows, page = [], 1
    while True:
        resp = http_json("company-question/get-paper-list",
                         {"page": page, "pageSize": 30, "orderBy": "default",
                          "queryType": "recommend"})
        recs = (resp.get("data") or {}).get("records") or []
        for r in recs:
            rows.append({
                "paperId": r["paperId"],
                "paperName": r["paperName"],
                "company": (r.get("companyTag") or {}).get("name", ""),
                "questionCount": r.get("questionCount"),
                "practiceCnt": r.get("practiceCnt"),
                "summaryUrl": f"https://www.nowcoder.com/exam/test/{r['paperId']}/summary",
            })
        total = resp.get("data", {}).get("totalPage", 0)
        print(f"  第 {page}/{total} 页，累计 {len(rows)}")
        if page >= total or not recs:
            break
        page += 1
        time.sleep(API_SLEEP)
    out = ROOT / "sources" / "nowcoder_papers.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"已写 {out}（{len(rows)} 套）——仅元数据，不含题面")
    return 0


# ---------------------------------------------------------------- --build
def dice(a: str, b: str) -> float:
    def bg(s):
        s = re.sub(r"[\s，。、？！：:（）()\[\]【】/\\·\-—+,.?'\"]", "", s.lower())
        return {s[i:i + 2] for i in range(len(s) - 1)} or {s}
    A, B = bg(a), bg(b)
    return 2 * len(A & B) / (len(A) + len(B)) if A and B else 0.0


def cmd_build() -> int:
    posts = sorted(POSTS.glob("*.json")) if POSTS.exists() else []
    sys.path.insert(0, str(ROOT / "tools"))
    from build import load_questions
    bank = load_questions()
    bank_titles = [(q["id"], q["title"]) for q in bank]

    def best_ref(text: str) -> tuple[str, float]:
        """题目原文 → 题库题号（Dice 最高分）。≥0.62 视为同一考点，0.45~0.62 标近似。"""
        best_id, best_sim = "", 0.0
        for qid, t in bank_titles:
            s = dice(text, t)
            if s > best_sim:
                best_id, best_sim = qid, s
        return best_id, round(best_sim, 2)

    exp_path = ROOT / "sources" / "nowcoder_experiences.jsonl"
    exp_path.parent.mkdir(parents=True, exist_ok=True)
    all_q: list[dict] = []
    posts.sort(key=lambda p: p.stat().st_mtime)
    seen_titles: set[str] = set()
    dup_posts = 0
    ref_hit = 0
    with exp_path.open("w", encoding="utf-8") as f:
        for p in posts:
            d = json.loads(p.read_text(encoding="utf-8"))
            if d["title"] in seen_titles:      # 平台重复收录，跳过
                dup_posts += 1
                continue
            seen_titles.add(d["title"])
            qs, revs = d.get("questions") or [], d.get("reverses") or []
            role = next((w for w in ROLE_WORDS if w.lower() in (d["title"] + " " +
                         " ".join(x["q"] for x in qs)).lower()), "")
            # 原文摘录：前 6 道题 + 与题库的题号关联（页面「面经」面板直接展示）
            highlights = []
            for x in qs[:6]:
                qid, sim = best_ref(x["q"])
                highlights.append({"q": x["q"][:80], "ref": qid if sim >= 0.62 else "",
                                   "near": qid if 0.45 <= sim < 0.62 else "",
                                   "sim": sim, "round": x.get("round") or ""})
                if sim >= 0.62:
                    ref_hit += 1
            rec = {"id": d["id"], "url": d["url"], "company": d["company"],
                   "role": role, "round": d.get("round") or "",
                   "date_raw": d.get("date_raw") or "", "title": d["title"][:60],
                   "n_questions": len(qs), "n_reverses": len(revs),
                   "collected_at": d.get("collected_at"),
                   "highlights": highlights}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            for x in qs:
                kind = "written" if "笔试" in d["title"] else "question"
                all_q.append({**x, "company": d["company"], "role": role,
                              "url": d["url"], "title": d["title"][:40],
                              "kind": kind})
            for q in revs:
                all_q.append({"q": q, "round": d.get("round") or "", "company": d["company"],
                              "role": role, "url": d["url"], "title": d["title"][:40],
                              "kind": "reverse"})

    # 跨帖聚类：先精确归一，再 Dice ≥0.8
    def norm(s):
        return re.sub(r"[\s，。、？！：:（）()\[\]【】“”\"'…·—]", "", s).lower()
    clusters: list[dict] = []
    for q in sorted(all_q, key=lambda x: -len(x["q"])):
        nq = norm(q["q"])
        hit = next((c for c in clusters
                    if c["norm"] == nq or dice(c["norm"], nq) >= 0.8), None)
        if hit:
            hit["occ"] += 1
            hit["sources"].append(q)
        else:
            clusters.append({"norm": nq, "q": q["q"], "occ": 1,
                             "kind": q["kind"], "sources": [q]})

    # 与库内比对
    for c in clusters:
        best, bs = "", 0.0
        for _, t in bank_titles:
            s = dice(c["q"], t)
            if s > bs:
                best, bs = t, s
        c["bank"], c["bank_sim"] = best, round(bs, 2)

    clusters.sort(key=lambda c: -c["occ"])
    qpath = ROOT / "sources" / "nowcoder_questions.csv"
    with qpath.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["题目摘要", "出现次数", "类型", "公司", "岗位", "轮次",
                    "与库内最高相似", "库内题号对应", "原帖链接"])
        for c in clusters:
            src = c["sources"][0]
            w.writerow([c["q"][:80], c["occ"], c["kind"], src.get("company", ""),
                        src.get("role", ""), src.get("round", ""),
                        c["bank_sim"], c["bank"][:40], src["url"]])

    multi = sum(1 for c in clusters if c["occ"] > 1)
    fresh = sum(1 for c in clusters if c["bank_sim"] < 0.7)
    print(f"面经 {len(posts)} 篇（重复帖 {dup_posts}）→ 题目 {len(all_q)} 条 → 去重后 {len(clusters)} 道"
          f"（多帖重复 {multi}，与库内不重合 {fresh}）")
    print(f"已写 {exp_path.name} / {qpath.name}（缓存正文留在 _cache/，不入库）")
    return 0


def cmd_reparse() -> int:
    """用当前解析规则重跑缓存里的正文（不重新渲染）。"""
    import glob
    for f in glob.glob(str(POSTS / "*.json")):
        p = Path(f)
        d = json.loads(p.read_text(encoding="utf-8"))
        body = d.get("body") or []
        if not body:
            print(f"  跳过 {d['id']}（缓存无正文）")
            continue
        qs, revs, rnd = parse_questions(body)
        d.update(questions=qs, reverses=revs, round=rnd)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  {d['id']} 题目 {len(qs):2d} 反问 {len(revs)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", type=int, metavar="N", help="拉前 N 页面经流")
    ap.add_argument("--fetch", type=int, metavar="K", help="渲染 K 篇命中帖的正文")
    ap.add_argument("--papers", action="store_true", help="拉 124 套真题卷元数据")
    ap.add_argument("--reparse", action="store_true", help="用当前规则重解析缓存正文")
    ap.add_argument("--build", action="store_true", help="整理索引与题目清单")
    a = ap.parse_args()
    if a.feed:
        cmd_feed(a.feed)
    if a.fetch:
        cmd_fetch(a.fetch)
    if a.papers:
        cmd_papers()
    if a.reparse:
        cmd_reparse()
    if a.build:
        cmd_build()
    if not (a.feed or a.fetch or a.papers or a.build or a.reparse):
        ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
