#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""面经「未入库」题补入库（骨架，status=indexed）。

数据源：sources/nowcoder_experiences.jsonl 的 highlights —— 只处理 ref/near 都为空、
且通过质量判定的条目（剔除行为面、碎片、多问合一的追问链）。

复用 nc_seed 的模块归属 / 去重 / 编号 / 骨架模板；独立记账 sources/nowcoder_backfilled.json
保证幂等（同一题目不会二次入库）。

用法：
    python tools/nc_backfill.py --dry     # 只统计，不写文件
    python tools/nc_backfill.py --max 80  # 最多入库 80 张
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from nc_seed import (module_of, dice, is_quality, clean_title, next_ids,  # noqa: E402
                     skeleton, TODAY)
from build import load_questions  # noqa: E402

EXP = ROOT / "sources" / "nowcoder_experiences.jsonl"
MANIFEST = ROOT / "sources" / "nowcoder_backfilled.json"
CONTENT = ROOT / "content"

# 追问链/多问合一/非技术岗的特征
CHAIN_RE = re.compile(
    r"这部分问得|接着问|沿着提示词|继续问|追问|（\d）|\(\d\)|第一问|第二问|上面说|刚才说|"
    r"产品经理|销售|运营|市场|自我介绍|你有什么想问|职业规划|为什么选择我们")
# 行为面 / 叙述句 / 代码片段 / 选择题 / 截断句：一律不入库
STRONG_JUNK = re.compile(
    r"班干部|面试哪些公司|实习期间负责|用户量|冲突怎么解决|怎么解决冲突|项目结果|"
    r"介绍一下你|简单介绍|介绍下你|讲一下你|说说你|项目介绍|个人情况|优缺点|"
    r"^会|^检查|^排查|^最后|^请判断|^请算|^请你|^根据|^已知|^下面|^下列|^这时|^此时|"
    r"^[🎯🔹1-9]|[Hh]eap\.|\.empty\(|\(\)|^[A-Za-z_][\w.]*[.?]?$|"
    r"这一句|哪一句|哪个选项|选项中最|正确的是|"
    r"能不能继续|讲清楚|展开说|再讲|我[把们]|答的感觉|记一下|#.*#|"
    r"报考|专业与|大学期间|研究生|你觉得|什么信息能支持|为什么在这个场景|这个方案|"
    r"^这个|^那|^所以")
QI = re.compile(r"什么|为什么|怎么|如何|哪些|哪几|区别|异同|原理|作用|多少|是否|能不能|"
                r"会不会|有什么|是什么|干什么|怎么回事")


def strong_ok(q: str) -> bool:
    t = q.strip()
    if STRONG_JUNK.search(t) or CHAIN_RE.search(t):
        return False
    if len(re.findall(r"[\u4e00-\u9fa5]", t)) < 8:
        return False
    if t.count("？") + t.count("?") > 1:
        return False
    if not t.endswith(("？", "?")):      # 只收明确问句，陈述句一律不入库
        return False
    # 截断特征：结尾是这些虚词/助词
    if t.rstrip("？?").endswith(("这", "的", "和", "与", "把", "被", "就", "才", "而", "然后")):
        return False
    return True
ROLE_WORDS = ["C++", "嵌入式", "推理", "部署", "机器人", "算法", "Linux", "驱动",
              "SLAM", "SDK", "测试开发", "平台研发", "后端", "软件"]


def norm(s: str) -> str:
    return re.sub(r"[\s，。、？！：:（）()\[\]【】“”\"'…·—+,.?《》/\\]", "", s.lower())


def load_manifest() -> set:
    if MANIFEST.exists():
        return set(json.loads(MANIFEST.read_text(encoding="utf-8")).keys())
    return set()


def save_manifest(keys: set):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({k: TODAY for k in sorted(keys)}, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--max", type=int, default=80)
    a = ap.parse_args()

    rows = [json.loads(x) for x in EXP.read_text(encoding="utf-8").splitlines() if x.strip()]
    bank = load_questions()
    bank_titles = [q["title"] for q in bank]
    done_keys = load_manifest()

    # 1) 收集候选：未入库 + 质量判定 + 非追问链 + 单一问句
    cand = []
    skipped = {"frag": 0, "chain": 0, "dup": 0, "done": 0, "bank": 0}
    seen: list[str] = []
    for r in rows:
        role = r.get("role") or next(
            (w for w in ROLE_WORDS if w.lower() in (r["title"] + " " + (r.get("role") or "")).lower()), "软件研发")
        for h in r.get("highlights") or []:
            q = re.sub(r"^[一二三四五六七八九十]+、\s*", "", (h.get("q") or "").strip())
            if not q or h.get("ref") or h.get("near"):
                continue
            if not is_quality(q):
                skipped["frag"] += 1
                continue
            if not strong_ok(q):
                skipped["chain"] += 1
                continue
            n = norm(q)
            if n in done_keys:
                skipped["done"] += 1
                continue
            # 与题库去重
            if any(dice(q, t) >= 0.5 for t in bank_titles):
                skipped["bank"] += 1
                continue
            # 跨帖去重（同题多次出现只入一卡，记次数）
            hit = next((x for x in cand if x["norm"] == n or dice(x["norm"], n) >= 0.8), None)
            if hit:
                hit["n"] += 1
                hit["cos"].add(r["company"])
                skipped["dup"] += 1
                continue
            cand.append({"q": q, "norm": n, "company": r["company"], "url": r["url"],
                         "title": r["title"][:40], "round": r.get("round") or "",
                         "role": role, "n": 1, "cos": {r["company"]}})

    print(f"候选合格新题 {len(cand)} 道；跳过：碎片 {skipped['frag']} · 追问链 {skipped['chain']} · "
          f"题库已有 {skipped['bank']} · 跨帖重复 {skipped['dup']} · 已入库 {skipped['done']}")
    if a.dry:
        for c in cand[:25]:
            print("  +", c["q"][:66], "|", c["company"])
        return 0

    cand = cand[:a.max]
    nxt = next_ids(["02_cpp", "03_linux", "04_algo", "05_deploy", "06_ros2",
                    "07_imaging", "08_robot", "09_hardware", "10_cv_pytorch", "11_python",
                    "12_backend"])
    made = 0
    for c in cand:
        mod, sub = module_of(c["q"])
        qid = f"Q-{nxt[mod]:04d}"
        nxt[mod] += 1
        title = clean_title(c["q"])
        body = skeleton(qid, title, mod, sub, c["company"], c["role"], c["url"], c["round"])
        (CONTENT / mod / f"{qid}.md").write_text(body, encoding="utf-8")
        done_keys.add(c["norm"])
        made += 1
    save_manifest(done_keys)
    print(f"已入库 {made} 张（status=indexed，待补答案）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
