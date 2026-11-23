---
id: Q-1733
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 40 题）
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
print(np.arange(0, 10, 2).tolist(), np.linspace(0, 1, 3).tolist())
```

- **A.** [0, 2, 4, 6, 8] [0.0, 0.5, 1.0]
- **B.** [0, 2, 4, 6, 8] [0.0, 0.3333333333333333, 0.6666666666666666, 1.0]
- **C.** [2, 4, 6, 8] [0.0, 0.5, 1.0]
- **D.** [0, 2, 4, 6, 8, 10] [0.0, 0.5, 1.0]

## 口述答案

答案是 **A. [0, 2, 4, 6, 8] [0.0, 0.5, 1.0]**，实际输出 `[0, 2, 4, 6, 8] [0.0, 0.5, 1.0]`。

arange 左闭右开；linspace(0,1,3) 是「含端点、均分 3 份」得 0/0.5/1，注意它是按个数取点不是按步长。

## 讲深一层

讲深一层：arange 按步长生成、左闭右开，语义等同内置 range；linspace 按点的个数生成、默认含两端，所以 linspace(0,1,3) 得 0/0.5/1。要固定点数用 linspace，改步长用 arange。浮点步长下 arange 会累积误差、末项可能少一个。

## 高频追问

1. **怎么让 linspace 不含终点？** —— `endpoint=False`。
2. **arange 能生成小数吗？** —— 能但不推荐，浮点步长易少一项。
3. **怎么生成 n 个等距点？** —— `np.linspace(start, stop, n)`。

## 易错点

- 把 linspace(0,1,3) 的 3 当步长：第三个参数是点数，得 3 个值
- 以为 arange(0,10,2) 含 10：左闭右开，最大是 8
- 用 arange 生成等分点：数量会因浮点误差差一，应改用 linspace

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
