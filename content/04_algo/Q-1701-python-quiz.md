---
id: Q-1701
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 8 题）
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
print(round(2.675, 2), round(0.5), round(1.5), round(-0.5))
```

- **A.** 2.67 0 2 0
- **B.** 2.68 0 2 -1
- **C.** 2.67 1 2 0
- **D.** 2.67 0 1 0

## 口述答案

答案是 **A. 2.67 0 2 0**，实际输出 `2.67 0 2 0`。

round 是「四舍六入五成双」（银行家舍入）：0.5→0、1.5→2、-0.5→0；2.675 的真实二进制值略小于 2.675，所以结果是 2.67。

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
