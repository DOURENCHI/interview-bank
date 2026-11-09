---
id: Q-1737
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 44 题）
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
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([[10, 20, 30], [40, 50, 60]])
print((a + b).tolist())
```

- **A.** [[11, 22, 33], [44, 55, 66]]
- **B.** [[10 20 30] [40 50 60]]
- **C.** [[1 2 3] [4 5 6]]
- **D.** [[11 21 31] [41 51 61]]

## 口述答案

答案是 **A. [[11, 22, 33], [44, 55, 66]]**，实际输出 `[[11, 22, 33], [44, 55, 66]]`。

形状相同的两数组逐元素相加，结果形状不变。

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

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
