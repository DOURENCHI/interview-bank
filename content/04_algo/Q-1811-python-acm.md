---
id: Q-1811
title: NumPy 形状、广播与聚合 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: draft
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 Python 程序对应的读入与输出写法是什么？

```python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([1, 2, 3])
c = np.array([[1, 2, 3], [4, 5, 6]])

print("shape", a.shape, "ndim", a.ndim, "size", a.size, "dtype", a.dtype)
print("a[0,1]", a[0, 1], "| a[1]", a[1], "| a[:,0]", a[:, 0])
print("T.shape", a.T.shape, "| reshape(4).shape", a.reshape(4).shape)
print("sum", a.sum(), "| axis=0", a.sum(axis=0), "| axis=1", a.sum(axis=1))
print("argmax", np.argmax([1, 9, 3]), "argmin", np.argmin([4, 2, 8]))
print("广播 b+c 形状", (b + c).shape)
print("逐元素乘 c*b", (c * b).tolist())
print("round/clip", np.round(np.array([3.7, -2.2, 5.0]), 1).tolist(),
      np.clip(np.array([3.7, -2.2, 5.0]), -2, 4).tolist())
```

输出样例：

```
shape (2, 2) ndim 2 size 4 dtype int64
a[0,1] 2 | a[1] [3 4] | a[:,0] [1 3]
T.shape (2, 2) | reshape(4).shape (4,)
sum 10 | axis=0 [4 6] | axis=1 [3 7]
argmax 1 argmin 1
广播 b+c 形状 (2, 3)
逐元素乘 c*b [[1, 4, 9], [4, 10, 18]]
round/clip [3.7, -2.2, 5.0] [3.7, -2.0, 4.0]
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
