---
id: Q-1799
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 106 题）
module: algo
sub: 并发与性能
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
import torch
m = torch.nn.Linear(2, 1)
opt = torch.optim.Adam(m.parameters(), lr=0.01)
m(torch.randn(4, 2)).sum().backward()
opt.step()
print(tuple(opt.state[m.weight].keys()))
```

- **A.** ('step', 'exp_avg', 'exp_avg_sq')
- **B.** ('exp_avg',)
- **C.** ('step',)
- **D.** ()

## 口述答案

答案是 **A. ('step', 'exp_avg', 'exp_avg_sq')**，实际输出 `('step', 'exp_avg', 'exp_avg_sq')`。

Adam 为每个参数维护步数、一阶动量和二阶动量三个状态，这是它比 SGD 收敛快的原因。

## 讲深一层

首次 `step()` 后为每个参数建 state：`step` 记录 t 用于偏差修正，`exp_avg` 是一阶矩（梯度指数平均），`exp_avg_sq` 是二阶矩（梯度平方的指数平均），后两者形状同参数。`step()` 之前 state 是空字典，所以打印时机决定结果。这也是 Adam 显存约为参数三倍的原因。

## 高频追问

1. **`step` 有什么用？** —— 偏差修正 `1−β^t`，否则前几步动量偏小、更新过慢
2. **显存开销多大？** —— 除参数外多存两份同形张量，约 3 倍参数量
3. **SGD 带 momentum 的 state 是什么？** —— 只有 `momentum_buffer` 一项

## 易错点

- 在 `opt.step()` 之前打印——得到空 tuple `()`，即选项 D
- 认为 state 是全局共享——每个参数一份，按参数对象索引
- 把 `exp_avg_sq` 当方差——它是梯度平方的滑动平均，不是统计方差

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
