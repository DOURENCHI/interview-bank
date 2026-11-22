---
id: Q-1794
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 101 题）
module: 04_algo
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
import torch
bn = torch.nn.BatchNorm1d(3)
bn.train()
bn(torch.randn(4, 3))
bn.eval()
print(tuple(bn(torch.randn(4, 3)).shape))
```

- **A.** (4, 3)
- **B.** ((4, 1),)
- **C.** ((1, 3),)
- **D.** ((4, 3), (4, 3))

## 口述答案

答案是 **A. (4, 3)**，实际输出 `(4, 3)`。

BatchNorm1d 保持形状不变，只做归一化；train 模式用当前批统计量，eval 模式用运行均值方差。

## 讲深一层

`BatchNorm1d` 对 `(N,C)` 沿 N 统计每个通道的均值方差，形状逐元素不变，所以还是 `(4,3)`。train 用当前批统计量并更新 running stats，eval 用 running_mean/var。因此同一输入两种模式结果不同，但形状始终一致。

## 高频追问

1. **batch=1 时 train 会怎样？** —— 方差为 0，输出退化成偏置，某些实现直接报错
2. **为什么 eval 结果不同？** —— 统计量来源不同：批统计 vs 运行均值方差
3. **BN 有哪些状态？** —— weight/bias 是 Parameter，running_mean/var、num_batches_tracked 是 buffer

## 易错点

- 认为 BN 会改变形状——它只做归一化，形状逐元素保持
- eval 忘了切——用批统计做单样本推理，输出剧烈抖动
- 把 running_mean 当 Parameter——它是 buffer，不在 `parameters()` 里

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
