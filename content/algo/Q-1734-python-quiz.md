---
id: Q-1734
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 41 题）
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
print(np.zeros((2, 3)).shape, np.ones((2,)).tolist())
```

- **A.** (2, 3) [1.0, 1.0]
- **B.** (2, 3) [1, 1]
- **C.** (3, 2) [1.0, 1.0]
- **D.** (2, 3) [0.0, 0.0]

## 口述答案

答案是 **A. (2, 3) [1.0, 1.0]**，实际输出 `(2, 3) [1.0, 1.0]`。

zeros/ones 默认 float64，所以是 1.0 不是 1；shape 参数是元组，(2,) 是一维长度 2。

## 讲深一层

讲深一层：zeros/ones 默认 dtype 是 float64，所以 1 打印成 1.0；要整数必须显式 dtype=int，这一点与 np.array([1,2]) 自动推断 int 相反。shape 传元组 (2,3)，传单个整数 3 表示长度 3 的一维。zeros 会真正写入 0，np.empty 只分配内存不初始化，内容随机但更快。

## 高频追问

1. **怎么创建整型全零？** —— `np.zeros((2,3), dtype=int)`。
2. **zeros 和 empty 区别？** —— 前者置零，后者内容未初始化。
3. **怎么按已有数组形状建？** —— `np.zeros_like(a)`，dtype 也跟随。

## 易错点

- 以为 np.ones((2,)) 输出 [1, 1]：默认 float64，实际 [1.0, 1.0]
- 把 shape 写成 np.zeros(2,3)：抛 TypeError，多维必须传元组
- 用 np.empty 当全零：内容是残留内存的随机值

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
