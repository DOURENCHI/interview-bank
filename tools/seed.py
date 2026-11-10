#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给没有本地文档可抽取的模块补索引级题卡。

这些题不是从你的文档里抽出来的，是按岗位 JD 推导的高频考点（source_type: inferred）。
只有题目和标签，答案留空，等补。目的只是让目录完整、覆盖可检索。

用法: python tools/seed.py
重复执行不会重复生成（按 title 去重）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ID_BASE = {"04_algo": 1600, "07_imaging": 3100, "08_robot": 3600, "10_cv_pytorch": 4600}

# (模块, 优先级, 子方向, 题目, 难度, 标签)
SEED = [
    # ---------------- 04 算法与机考（P0，华为机考是硬门槛）
    ("04_algo", "P0", "ACM模式", "华为机考为什么必须用 ACM 模式写输入输出？", 1, ["机考", "ACM", "输入输出"]),
    ("04_algo", "P0", "ACM模式", "读一行不定长整数、读到文件末尾，C++ 怎么写才不出错？", 2, ["机考", "getline", "cin"]),
    ("04_algo", "P0", "ACM模式", "输入输出格式错会掉多少分，怎么自查？", 1, ["机考", "边界", "调试"]),
    ("04_algo", "P0", "数组哈希", "字符串处理常考哪几类？", 1, ["机考", "字符串", "回文"]),
    ("04_algo", "P0", "数组哈希", "哈希表在这类题里一般解决什么问题？", 1, ["机考", "哈希", "去重"]),
    ("04_algo", "P0", "双指针滑窗", "双指针和滑动窗口的区别是什么？", 2, ["机考", "双指针", "滑动窗口"]),
    ("04_algo", "P0", "双指针滑窗", "滑动窗口什么条件下能用？", 2, ["机考", "滑动窗口", "单调性"]),
    ("04_algo", "P0", "DFS BFS", "DFS 和 BFS 怎么选？", 2, ["机考", "DFS", "BFS"]),
    ("04_algo", "P0", "DFS BFS", "二叉树遍历的递归写法和非递归写法差别在哪？", 2, ["机考", "二叉树", "遍历"]),
    ("04_algo", "P0", "DP", "动态规划的状态怎么定义？", 3, ["机考", "DP", "状态设计"]),
    ("04_algo", "P0", "DP", "0-1 背包和完全背包的区别是什么？", 2, ["机考", "DP", "背包"]),
    ("04_algo", "P0", "ACM模式", "机考第二题只拿一半样例，怎么排优先级？", 2, ["机考", "策略", "得分"]),

]

TEMPLATE = """---
id: {qid}
title: {title}
module: {module}
sub: {sub}
priority: {pri}
difficulty: {diff}
roles: []
companies: []
qtype: principle
status: indexed
source_type: inferred
source_ref: 按岗位 JD 推导，非真实面经
verified_at: 2026-11-09
tags: [{tags}]
---

## 口述答案

> 待补充。200–320 字，口语，结构：结论 → 为什么 → 落到"我做过"。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

待补充。

## 来源

按华为（车BU / 计算产品线）与亿嘉和岗位 JD 推导的高频考点，**不是真实面经**。
"""


def main() -> int:
    created = 0
    for module, pri, sub, title, diff, tags in SEED:
        d = CONTENT / module
        d.mkdir(parents=True, exist_ok=True)
        # 按 title 去重
        exists = False
        for f in d.glob("Q-*.md"):
            if title in f.read_text(encoding="utf-8", errors="ignore"):
                exists = True
                break
        if exists:
            continue
        nums = [int(m.group(1)) for f in d.glob("Q-*.md")
                if (m := re.match(r"Q-(\d+)", f.name))]
        nxt = max(nums + [ID_BASE[module]]) + 1
        qid = f"Q-{nxt:04d}"
        (d / f"{qid}.md").write_text(
            TEMPLATE.format(qid=qid, title=title, module=module, sub=sub,
                            pri=pri, diff=diff, tags=", ".join(tags)),
            encoding="utf-8")
        created += 1
    print(f"新增索引题卡 {created} 道")
    return 0


if __name__ == "__main__":
    sys.exit(main())
