---
id: Q-1729
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 35 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
