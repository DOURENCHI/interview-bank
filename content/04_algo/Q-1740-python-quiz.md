---
id: Q-1740
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 47 题）
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
f = np.array([3.7, -2.2, 5.0])
print(np.round(f, 1).tolist(), np.clip(f, -2, 4).tolist())
```

- **A.** [3.7, -2.2, 5.0] [3.7, -2.0, 4.0]
- **B.** [3.7, -2.2, 5.0] [-2.0, 4.0, 4.0]
- **C.** [3.7, -2.2, 5.0] [-2.2, 4.0, 5.0]
- **D.** [3.7, -2.2, 5.0] [3.7, -2.0, 5.0]

## 口述答案

答案是 **A. [3.7, -2.2, 5.0] [3.7, -2.0, 4.0]**，实际输出 `[3.7, -2.2, 5.0] [3.7, -2.0, 4.0]`。

np.round 是四舍五入（与内置 round 的银行家舍入不同），一位小数下 3.7/5.0 不变；clip 把值限制在 [-2, 4]，-2.2 被抬到 -2、5.0 被压到 4。

## 讲深一层

讲深一层：np.round 的第二个参数是小数位数，可传负数表示保留到十位、百位；它逐元素向量化，dtype 仍是 float。.5 边界它同样取偶，与内置 round 规则一致，差别在返回类型和批量能力。np.clip 把每个元素夹到 [a_min,a_max]，等于边界的值原样保留，也可以只给一侧。

## 高频追问

1. **clip 只给上界怎么写？** —— `np.clip(f, None, 4)`。
2. **想保留到十位？** —— `np.round(f, -1)`。
3. **round 后 dtype 变了吗？** —— 不变，仍是 float64。

## 易错点

- 把 clip 当开区间：-2.2 被抬到 -2，不是保持 -2.2
- 用 round 做金额四舍五入：.5 边界取偶，应用 decimal 的 HALF_UP
- 以为 np.round 返回 int：仍是 float，3.0 不是 3

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
