---
id: Q-1719
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 25 题）
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
print([i for i in range(5) if i % 2 == 0], {i: i * i for i in range(3)})
```

- **A.** [0, 2, 4] {0: 0, 1: 1, 2: 4}
- **B.** [0, 2, 4] {0: 0, 1: 1, 2: 8}
- **C.** [1, 3] {0: 0, 1: 1, 2: 4}
- **D.** [0, 2, 4] {1: 1, 2: 4}

## 口述答案

答案是 **A. [0, 2, 4] {0: 0, 1: 1, 2: 4}**，实际输出 `[0, 2, 4] {0: 0, 1: 1, 2: 4}`。

列表推导式的 if 是过滤条件不是三元表达式；字典推导式是 {键: 值}，键取 i、值取 i*i。

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
