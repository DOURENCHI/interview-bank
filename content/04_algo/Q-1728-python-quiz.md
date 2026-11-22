---
id: Q-1728
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 35 题）
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
print(a.shape, a.ndim, a.dtype, a.size)
```

- **A.** (2, 2) 2 int64 4
- **B.** (2, 2) 2 int32 4
- **C.** (4,) 1 int64 4
- **D.** (2, 2) 2 int64 2

## 口述答案

答案是 **A. (2, 2) 2 int64 4**，实际输出 `(2, 2) 2 int64 4`。

shape 是各维长度、ndim 是维数、size 是元素总数（2×2=4）；dtype 由字面量推断，整数默认 int64（Linux/macOS）或 int32（Windows）。

## 讲深一层

讲深一层：shape 是元组、ndim 等于 len(shape)、size 是各维乘积，三者互为校验。dtype 由 np.array 推断，纯 Python int 在 64 位 Linux/macOS 上是 int64，Windows 默认 int32，同一段代码跨平台输出会变；要稳定就显式写 dtype=np.int64。

## 高频追问

1. **怎么保证跨平台 dtype 一致？** —— 构造时显式指定 dtype。
2. **size 和 len 区别？** —— size 是元素总数，len 只返回第 0 维长度。
3. **shape (4,) 和 (4,1) 区别？** —— 前者一维，后者二维单列，广播行为不同。

## 易错点

- 把 size 当成行数：2×2 的 size 是 4，不是 2
- 在 Windows 上断言 int64：默认可能是 int32，答案随平台变
- 以为 ndim 是元素个数：ndim 是维数，这里为 2

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
