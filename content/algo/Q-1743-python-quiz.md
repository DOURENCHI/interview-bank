---
id: Q-1743
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 50 题）
module: algo
sub: 容器与切片
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-21
tags: [Python, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```python
import numpy as np
a = np.array([1, 2, 3])
print(a[np.array([0, 2])].tolist())
```

- **A.** [1, 3]
- **B.** [0, 2]
- **C.** [1, 2, 3]
- **D.** [2, 3]

## 口述答案

答案是 **A. [1, 3]**，实际输出 `[1, 3]`。

用整数数组做「花式索引」一次取多个元素，按下标顺序取出 [1, 3]——注意结果是新数组不是原数组的视图。

## 讲深一层

讲深一层：用整数数组索引称为花式索引，结果形状由索引数组的形状决定，且返回的是副本而非视图——这与切片返回视图正好相反，改结果不会影响原数组。索引可重复、可为负，越界则抛 IndexError。布尔数组是另一类花式索引，按掩码挑元素，长度必须与被索引轴一致。

## 高频追问

1. **花式索引返回视图吗？** —— 返回副本，与切片不同。
2. **怎么按条件筛选？** —— `a[a > 1]`，布尔掩码。
3. **索引能重复吗？** —— 能，[0,0,1] 会取三次。

## 易错点

- 以为 a[[0,2]] 返回视图：是副本，改它原数组不变
- 把二维的两个索引数组当笛卡尔积：实际按位置配对，长度需一致
- 用越界下标：抛 IndexError，不像切片会自动截断

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
