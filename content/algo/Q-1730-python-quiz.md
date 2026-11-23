---
id: Q-1730
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 37 题）
module: algo
sub: 语法与类型
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
print(a.T.shape, a.reshape(4).shape, a.reshape(-1).shape)
```

- **A.** (2, 2) (4,) (4,)
- **B.** (2, 2) (4, 1) (4,)
- **C.** (2, 2) (4,) (1, 4)
- **D.** (4, 4) (4,) (4,)

## 口述答案

答案是 **A. (2, 2) (4,) (4,)**，实际输出 `(2, 2) (4,) (4,)`。

转置后形状不变（方阵）；reshape(4) 拉平成一维；reshape(-1) 里的 -1 表示「由其他维度自动推算」，这里也是 4 个元素一维。

## 讲深一层

讲深一层：reshape 在内存连续时返回视图、否则复制，所以它可能悄悄产生副本。-1 表示该维由总数自动推算，且只能出现一个；reshape(4)、reshape(-1) 完全等价。a.T 只交换 strides，是视图；方阵转置 shape 不变，容易误以为没生效。

## 高频追问

1. **reshape 会复制吗？** —— 能视图就视图，跨步不连续时复制。
2. **reshape(-1,1) 干什么？** —— 拉成一列，形状 (n,1)，常用于广播。
3. **a.T 改原数组吗？** —— 不改数据，但它是视图，赋值会写回原数组。

## 易错点

- 以为 reshape 总返回新数组：可能是视图，改它会影响原数组
- 写 reshape(4,-1) 想推第二维：元素数不整除会抛 ValueError
- 看方阵转置 shape 没变就以为失败：数据已转置，只是形状巧合相同

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
