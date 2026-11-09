#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把两个考点实验台里的题库导入 04_algo 模块。

实验台的 DATA 是结构化 JSON（不是散落的 HTML），所以能直接拿到
题目、代码、选项、答案、解析——比从标题抽题可靠得多。

来源：
  C++考点实验台     quiz 62 + snips 19
  Python考点实验台  quiz 115 + snips 16

用法: python tools/import_lab.py [--dry]
重复执行不会重复生成：题卡带 auto: true + lab_src 标记，先清后建。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "04_algo"
DEC = json.JSONDecoder()

LABS = [
    ("C++", r"D:/工程/教学文档/C++实验台/C++考点实验台.html", "cpp"),
    ("Python", r"D:/工程/教学文档/Python实验台/Python考点实验台.html", "python"),
]
MODULE = "04_algo"
ID_BASE, SPAN = 1600, 500


def load_data(path: str) -> dict:
    t = Path(path).read_text(encoding="utf-8")
    i = t.find("const DATA = ")
    if i < 0:
        raise ValueError(f"{path}: 找不到 DATA")
    i += len("const DATA = ")
    return DEC.raw_decode(t[i:])[0]


def existing_max() -> int:
    nums = [int(m.group(1)) for f in CONTENT.glob("Q-*.md")
            if (m := re.match(r"Q-(\d+)", f.name))]
    return max(nums + [ID_BASE])


def opt_block(opts: list[str]) -> str:
    return "\n".join(f"- **{chr(65 + i)}.** {o}" for i, o in enumerate(opts))


def quiz_md(qid: str, lang: str, fence: str, q: dict, src: str, idx: int) -> str:
    opts, ans = q.get("opts") or [], q.get("ans", 0)
    expl = (q.get("expl") or "").strip()
    out = (q.get("out") or "").strip()
    right = f"{chr(65 + ans)}. {opts[ans]}" if 0 <= ans < len(opts) else ""
    return f"""---
id: {qid}
title: 这段 {lang} 代码输出什么？（{q.get('chap','')} · 第 {idx} 题）
module: {MODULE}
sub: {lang}语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: {src}
verified_at: 2026-11-09
tags: [{lang}, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```{fence}
{q.get('code','').strip()}
```

{opt_block(opts)}

## 口述答案

答案是 **{right}**，实际输出 `{out}`。

{expl}

## 讲深一层

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`{src}` · {q.get('chap','')}
"""


def snip_md(qid: str, lang: str, fence: str, q: dict, src: str) -> str:
    stdin = (q.get("stdin") or "").strip()
    inpart = f"\n输入样例：\n\n```\n{stdin}\n```\n" if stdin else ""
    return f"""---
id: {qid}
title: {q.get('title','')} 的 ACM 输入输出怎么写？
module: {MODULE}
sub: {lang} ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: draft
source_type: self_doc
source_ref: {src}
verified_at: 2026-11-09
tags: [{lang}, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 {lang} 程序对应的读入与输出写法是什么？

```{fence}
{q.get('code','').strip()}
```
{inpart}
输出样例：

```
{(q.get('out') or '').strip()}
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`{src}` · {q.get('chap','')}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    # 清掉上一轮导入的（只清 lab_src 标记的，不碰 seed 与手工题）
    removed = 0
    for f in CONTENT.glob("Q-*.md"):
        if re.search(r"^lab_src:", f.read_text(encoding="utf-8"), re.M):
            f.unlink()
            removed += 1
    print(f"清理旧导入 {removed} 张")

    nxt = existing_max() + 1
    start = nxt
    created = 0
    per_lab = {}
    for lang, path, fence in LABS:
        try:
            d = load_data(path)
        except (OSError, ValueError) as e:
            print(f"跳过 {lang}: {e}")
            continue
        src_rel = Path(path).relative_to("D:/工程").as_posix()
        cnt_q = cnt_s = 0
        for qi, q in enumerate(d.get("quiz", []), 1):
            if not q.get("code"):
                continue
            if nxt >= ID_BASE + SPAN:
                print(f"⚠ {MODULE} 号段用尽")
                return 1
            qid = f"Q-{nxt:04d}"
            if not args.dry:
                (CONTENT / f"{qid}-{fence}-quiz.md").write_text(
                    quiz_md(qid, lang, fence, q, src_rel, qi), encoding="utf-8")
            nxt += 1
            cnt_q += 1
            created += 1
        for q in d.get("snips", []):
            if not q.get("code"):
                continue
            if nxt >= ID_BASE + SPAN:
                print(f"⚠ {MODULE} 号段用尽")
                return 1
            qid = f"Q-{nxt:04d}"
            if not args.dry:
                (CONTENT / f"{qid}-{fence}-acm.md").write_text(
                    snip_md(qid, lang, fence, q, src_rel), encoding="utf-8")
            nxt += 1
            cnt_s += 1
            created += 1
        per_lab[lang] = (cnt_q, cnt_s)
        print(f"  {lang:7s} quiz {cnt_q:3d} + snips {cnt_s:3d}")

    print(f"\n生成 {created} 张题卡 → content/{MODULE}/")
    if created:
        print(f"编号 Q-{start:04d} ~ Q-{nxt-1:04d}")
    if args.dry:
        print("（--dry 预览，未写文件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
