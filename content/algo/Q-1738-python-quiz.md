---
id: Q-1738
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 45 题）
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
print(np.argmax([1, 9, 3]), np.argmin([4, 2, 8]))
```

- **A.** 1 1
- **B.** 1 3
- **C.** 2 1
- **D.** 0 1

## 口述答案

答案是 **A. 1 1**，实际输出 `1 1`。

argmax/argmin 返回「下标」不是值：最大的是 9 在下标 1，最小的是 2 也在下标 1。

## 讲深一层

讲深一层：argmax/argmin 返回的是下标而非值，多维数组不传 axis 时先把数组拉平再取扁平下标。遇到并列最大值返回「第一个」出现的下标，这由实现保证但不是数学定义。传 axis 后返回降维后的下标数组，配合 np.take_along_axis 才能取回对应值；空数组调用抛 ValueError。

## 高频追问

1. **怎么用 argmax 取值？** —— `a.flat[i]` 或 `a[np.unravel_index(i, a.shape)]`。
2. **有并列最大值取哪个？** —— 第一个，下标最小。
3. **多维怎么按轴取？** —— argmax(axis=1) 得每行最大值所在列号。

## 易错点

- 把 argmax 的结果当最大值：输出 1 而不是 9
- 以为并列时随机取：稳定返回第一个下标
- 对空数组调 argmax：抛 ValueError，需先判 size

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
