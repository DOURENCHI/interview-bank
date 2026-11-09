---
id: Q-1710
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 16 题）
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
print(list(range(2, 8, 2)), list(range(3)), len(list(range(0, 10, 3))))
```

- **A.** [2, 4, 6] [0, 1, 2] 4
- **B.** [2, 4, 6, 8] [0, 1, 2] 4
- **C.** [2, 4, 6] [0, 1, 2] 3
- **D.** [2, 4, 6] [1, 2, 3] 4

## 口述答案

答案是 **A. [2, 4, 6] [0, 1, 2] 4**，实际输出 `[2, 4, 6] [0, 1, 2] 4`。

range(2, 8, 2) 左闭右开取到 7 所以是 [2,4,6]；range(0,10,3) 有 0/3/6/9 四个数，长度 4。

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
