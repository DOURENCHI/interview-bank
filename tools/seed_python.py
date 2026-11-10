#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""建 11_python 模块的题卡骨架（答案由 tools/cards/py_*.cards 填）。

只做一次：生成带 frontmatter 的空卡，之后用 apply_cards.py 写正文。
重跑会覆盖本模块所有题卡，注意别在有答案后执行。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

MODULE = "11_python"
DIR = ROOT / "content" / MODULE
BASE = 5100
TODAY = "2026-11-10"

# (尾号, 子方向, 优先级, 难度, 标题)
Q = [
    (1, "语言机制", "P0", 2, "默认参数写成空列表，为什么第二次调用还带着上次的数据？"),
    (2, "语言机制", "P0", 2, "is 和 == 有什么区别？为什么 256 是 True 而 257 是 False？"),
    (3, "语言机制", "P0", 1, "切片返回的是拷贝还是视图？越界切片为什么不会报错？"),
    (4, "语言机制", "P0", 3, "循环里创建的 lambda 为什么全都返回最后一个值？"),
    (5, "语言机制", "P0", 2, "装饰器的本质是什么？为什么必须加 functools.wraps？"),
    (6, "语言机制", "P0", 2, "浅拷贝改内层元素，为什么原对象也跟着变了？"),
    (7, "语言机制", "P0", 1, "可变对象和不可变对象有什么区别？对工程有什么实际影响？"),

    (8, "数据结构", "P0", 1, "list 和 tuple 该怎么选？除了能不能改还有什么差别？"),
    (9, "数据结构", "P0", 2, "dict 查找为什么是 O(1)？最坏情况呢？"),
    (10, "数据结构", "P0", 1, "set 去重为什么结果无序？有什么代价？"),
    (11, "数据结构", "P0", 2, "Python 的排序稳定吗？key 函数会被调用几次？"),
    (12, "数据结构", "P0", 2, "list.pop(0) 为什么慢？该用什么替代？"),
    (13, "数据结构", "P0", 2, "循环里用 += 拼字符串，为什么十几秒才跑完？"),

    (14, "迭代器与生成器", "P0", 2, "迭代器协议是什么？为什么用完就废？"),
    (15, "迭代器与生成器", "P0", 2, "读 10 GB 日志，生成器是怎么做到不占内存的？"),
    (16, "迭代器与生成器", "P1", 3, "yield from 和 for 循环里 yield 有什么区别？"),
    (17, "迭代器与生成器", "P1", 2, "生成器表达式和列表推导式该怎么选？"),
    (18, "迭代器与生成器", "P0", 2, "遍历列表时 remove 元素，为什么会漏删一个？"),

    (19, "并发与 GIL", "P0", 3, "GIL 是什么？它限制了 Python 的什么能力？"),
    (20, "并发与 GIL", "P0", 2, "多线程适合什么场景？CPU 密集为什么加了线程反而更慢？"),
    (21, "并发与 GIL", "P0", 2, "multiprocessing 怎么绕过 GIL？代价是什么？"),
    (22, "并发与 GIL", "P1", 3, "asyncio 和线程池有什么区别？什么时候该用协程？"),
    (23, "并发与 GIL", "P0", 2, "两个线程同时 i += 1 会丢更新吗？怎么保证线程安全？"),
    (24, "并发与 GIL", "P1", 2, "多进程之间怎么传数据？为什么不能用全局变量？"),
    (25, "并发与 GIL", "P1", 2, "Python 里死锁是怎么产生的？怎么避免？"),

    (26, "异常与资源", "P0", 1, "try/except/else/finally 各自什么时候执行？"),
    (27, "异常与资源", "P0", 2, "with 是怎么实现的？为什么它能保证资源一定释放？"),
    (28, "异常与资源", "P1", 2, "raise from 是干什么的？异常链有什么用？"),
    (29, "异常与资源", "P1", 1, "自定义异常该继承什么？为什么不该继承 BaseException？"),
    (30, "异常与资源", "P1", 2, "EAFP 和 LBYL 两种风格该怎么选？"),

    (31, "性能与工程", "P1", 2, "怎么定位 Python 程序的性能瓶颈？"),
    (32, "性能与工程", "P1", 3, "为什么把变量放局部能变快？LOAD_FAST 是什么？"),
    (33, "性能与工程", "P0", 2, "numpy 向量化为什么比 for 循环快几十倍？"),
    (34, "性能与工程", "P1", 1, "依赖管理怎么做？requirements.txt 有什么坑？"),
    (35, "性能与工程", "P2", 2, "类型注解会影响运行速度吗？它到底解决什么问题？"),
    (36, "性能与工程", "P1", 2, "什么时候用 Python，什么时候必须换 C++？"),
    (37, "性能与工程", "P1", 2, "PyTorch 的 DataLoader 开多进程，为什么在 Windows 上卡死？"),
    (38, "性能与工程", "P1", 3, "Python 进程内存一直涨，怎么排查？"),
    (39, "性能与工程", "P2", 2, "把 Python 脚本打包成 exe，体积为什么几百兆？"),
    (40, "性能与工程", "P1", 2, "单元测试该怎么写？pytest 和 unittest 怎么选？"),
]

BODY = """## 题目

待补充。

## 口述答案

待补充。

## 讲深一层

待补充。

## 高频追问

1. 待补充

## 易错点

- 待补充

## 关联项目

- 无（通用八股，不绑定具体项目）

## 来源

Python 语言与工程实践整理（预测题，非真实面经）
"""


def main() -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    for f in DIR.glob("Q-*.md"):
        f.unlink()
    for tail, sub, pri, diff, title in Q:
        qid = f"Q-{BASE + tail}"
        fm = f"""---
id: {qid}
title: {title}
module: {MODULE}
sub: {sub}
priority: {pri}
difficulty: {diff}
roles: []
companies: []
qtype: principle
status: indexed
source_type: inferred
source_ref: Python 语言与工程实践整理
verified_at: {TODAY}
tags: []
py_seed: true
---

"""
        (DIR / f"{qid}.md").write_text(fm + BODY, encoding="utf-8")
    print(f"生成 {len(Q)} 张 Python 题卡 → content/{MODULE}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
