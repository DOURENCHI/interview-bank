---
id: Q-1732
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 39 题）
module: 04_algo
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
a = np.array([[1, 2], [3, 4]])
print(a.mean(), a.max(), a.min())
```

- **A.** 2.5 4 1
- **B.** 2.5 1 4
- **C.** 10 4 1
- **D.** 2 4 1

## 口述答案

答案是 **A. 2.5 4 1**，实际输出 `2.5 4 1`。

mean 是所有元素均值 (1+2+3+4)/4 = 2.5，输出是 float；max/min 返回元素本身不是下标。

## 讲深一层

讲深一层：mean 对整型数组也返回 float64，因为要保证小数精度；max/min 返回元素值本身，要下标得用 argmax/argmin。三者默认对全部元素操作，传 axis 才按维聚合。含 NaN 时 mean 与 max 都返回 nan，需改用 np.nanmean / np.nanmax 跳过缺失值，这是数据清洗里最常见的坑。

## 高频追问

1. **怎么取最大值的位置？** —— np.argmax(a)，返回扁平化后的下标。
2. **整型数组 mean 是什么类型？** —— float64。
3. **有 NaN 怎么办？** —— np.nanmean / np.nanmax，普通版会传染 nan。

## 易错点

- 把 max 当成返回下标：返回的是值 4，下标要用 argmax
- 以为 mean 返回 int：2.5 是 float，按整除思路会得 2
- 数组里有 NaN 仍用 mean：结果变 nan，而不是忽略缺失值

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
