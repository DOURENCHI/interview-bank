---
id: Q-1741
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 48 题）
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
print(np.dot([1, 2], [3, 4]), np.linalg.norm([3, 4]))
```

- **A.** 11 5.0
- **B.** 10 5.0
- **C.** 11 7.0
- **D.** 7 5.0

## 口述答案

答案是 **A. 11 5.0**，实际输出 `11 5.0`。

dot 是点积 = 1×3 + 2×4 = 11；范数是向量长度 √(3²+4²) = 5.0。

## 讲深一层

讲深一层：np.dot 对一维是内积、对二维是矩阵乘，语义随维度变化，这也是它容易被误用的原因；想明确矩阵乘用 @ 或 np.matmul。np.linalg.norm 默认算 L2 范数，对矩阵是 Frobenius 范数（全体元素平方和开根），要按行或列求范数得传 axis 或 ord。范数返回 float，即使输入是整数数组。

## 高频追问

1. **dot 和 \* 区别？** —— 内积/矩阵乘 vs 逐元素乘。
2. **怎么算 L1 范数？** —— `np.linalg.norm(x, ord=1)`。
3. **矩阵的默认 norm 是什么？** —— Frobenius 范数，全体元素平方和开根。

## 易错点

- 把 dot 当逐元素乘：[1,2]·[3,4] 得 11 而不是 [3,8]
- 以为 norm 返回整数：5.0 是 float
- 对矩阵默认 norm 当谱范数：实际是 Frobenius，谱范数要 ord=2

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
