---
id: Q-1731
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 38 题）
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
a = np.array([[1, 2], [3, 4]])
print(a.sum(), a.sum(axis=0).tolist(), a.sum(axis=1).tolist())
```

- **A.** 10 [4, 6] [3, 7]
- **B.** 10 [3 7] [4 6]
- **C.** 10 [4 6] [4 6]
- **D.** 10 4 6

## 口述答案

答案是 **A. 10 [4, 6] [3, 7]**，实际输出 `10 [4, 6] [3, 7]`。

axis=0 沿行方向求和（每列求和）得 [4,6]；axis=1 沿列方向（每行求和）得 [3,7]——axis 指的是「被消掉的维度」。

## 讲深一层

讲深一层：axis 指的是「被消掉的那一维」，不是「沿哪个方向走」。axis=0 消掉行维，剩下每列的和 [4,6]；axis=1 消掉列维，剩下每行的和 [3,7]。记住「结果形状 = 原形状去掉该轴」就不会绕晕。axis=-1 表示最后一维，axis=(0,1) 可一次消多维，keepdims=True 保留长度 1 的轴便于广播。

## 高频追问

1. **axis=0 为什么是列求和？** —— 消掉第 0 维（行），每列剩下的元素相加。
2. **怎么保持维度？** —— `sum(axis=0, keepdims=True)` 得 (1,2)。
3. **axis=-1 是什么？** —— 最后一维，二维时等价 axis=1。

## 易错点

- 把 axis=0 当成按行求和：实际得 [4,6]，[3,7] 才是 axis=1
- 以为 axis 指遍历方向：它指被消除的维度，按方向记容易反
- 对一维数组用 axis=1：抛 AxisError，一维只有 axis=0

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
