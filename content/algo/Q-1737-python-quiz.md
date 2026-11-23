---
id: Q-1737
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 44 题）
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

讲深一层：形状完全相同时不需要广播，逐位置相加即可，结果形状不变；dtype 按提升规则取两者中更宽的类型，int32+int64 得 int64，int+float 得 float64。同样的 + 用在 Python list 上是拼接而不是逐元素加，[1,2]+[10,20] 得四个元素，这是 NumPy 与原生列表最容易混的地方。

## 高频追问

1. **ndarray 的 + 和 list 的 + 区别？** —— 逐元素运算 vs 拼接。
2. **形状不同能加吗？** —— 需可广播，否则 ValueError。
3. **dtype 怎么定？** —— 按类型提升，必要时 astype 显式控制。

## 易错点

- 以为 a+b 会拼接成 2×6：ndarray 是逐元素，仍 2×3
- 把列表相加的习惯套到数组：列表拼接得 4 个元素，结果完全不同
- 忽略 dtype 提升：int 与 float 相加结果变 float，打印带小数点

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
