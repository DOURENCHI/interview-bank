---
id: Q-1716
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 22 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```python
print(bin(10), oct(10), hex(255), abs(-3))
```

- **A.** 0b1010 0o12 0xff 3
- **B.** 1010 12 ff 3
- **C.** 0b1010 0o12 0xff -3
- **D.** 0b1010 0o12 0xFF -3

## 口述答案

答案是 **A. 0b1010 0o12 0xff 3**，实际输出 `0b1010 0o12 0xff 3`。

bin/oct/hex 都带前缀（0b / 0o / 0x），hex 输出小写；abs(-3) 是 3。

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

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
