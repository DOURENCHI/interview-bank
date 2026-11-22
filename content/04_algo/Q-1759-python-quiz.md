---
id: Q-1759
title: 这段 Python 代码输出什么？（04 线性模型与梯度下降 · 第 66 题）
module: 04_algo
sub: 函数与异常
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
xs = np.array([1.0, 2.0, 3.0])
ys = np.array([2.0, 4.0, 6.0])
w = float((xs @ ys) / (xs @ xs))
print(w)
```

- **A.** 2.0
- **B.** 1.5
- **C.** 2.5
- **D.** 3.0

## 口述答案

答案是 **A. 2.0**，实际输出 `2.0`。

最小二乘闭式解 w = Σxy / Σx² = 28/14 = 2.0。梯度下降是逼近这个值，闭式解一步到位。

## 讲深一层

这是无截距最小二乘的正规方程解：最小化 `Σ(xw−y)²` 对 w 求导令零，得 `w = Σxy/Σx²`，与 `(XᵀX)⁻¹Xᵀy` 一致。`@` 对 1-D 张量就是内积，等价 `np.dot`。加截距后要解 2×2 方程组，w 变成 `Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²`；本例因 y=2x 过原点，加不加截距都得 2.0。

## 高频追问

1. **有 bias 时闭式解怎么算？** —— 解 `[[Σx², Σx],[Σx, n]]·[w, b]ᵀ = [Σxy, Σy]ᵀ`，一个二元一次方程组
2. **为什么梯度下降也奔着 2.0 去？** —— 优化的是同一个平方损失，凸函数只有这一个极小点
3. **`xs @ ys` 换成 `np.outer` 会怎样？** —— 得到 3×3 矩阵，外面套 `float()` 直接报错，只能对标量转型

## 易错点

- 分母写成 `ys @ ys`——得 28/56=0.5，公式记反是最典型的失分
- 忘写 `float()`——打印成 `np.float64(2.0)`，与题目输出格式不符
- 以为 `xs @ ys` 是矩阵乘——1-D 时是内积返回标量，2-D 才是矩阵乘

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 04 线性模型与梯度下降
