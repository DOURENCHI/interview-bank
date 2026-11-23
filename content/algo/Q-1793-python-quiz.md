---
id: Q-1793
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 100 题）
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
import torch
gru = torch.nn.GRU(4, 5, batch_first=True)
print(tuple(gru(torch.randn(2, 7, 4))[0].shape))
```

- **A.** (2, 7, 5)
- **B.** ((2, 7, 4),)
- **C.** ((1, 2, 5),)
- **D.** ((2, 4, 5),)

## 口述答案

答案是 **A. (2, 7, 5)**，实际输出 `(2, 7, 5)`。

GRU 参数比 LSTM 少（只有更新门和重置门），但输出形状与 RNN/LSTM 完全一致。

## 讲深一层

GRU 把 LSTM 的输入门与遗忘门合并成更新门，另有重置门，没有独立 cell state，所以只返回 `(out, h_n)` 两项，参数约为 LSTM 的 3/4。输出形状与 RNN、LSTM 完全一致，换模型不影响下游形状，这也是三者能互换的直接原因。

## 高频追问

1. **参数量怎么比？** —— GRU 是 `3×(H(H+I)+H)`，LSTM 是 4 倍同式，约 75%
2. **为什么只有 h？** —— 没有 cell state，隐状态同时承担短期与长期信息
3. **工程上怎么选？** —— 短序列 GRU 更快够用，长依赖 LSTM 表达力更强

## 易错点

- 以为 GRU 也返回 `(h,c)`——解包会报 `too many values to unpack`
- 答 `(2,4,5)`——把 in=4 与 hidden=5 的位置搞混
- 说 GRU 有三个门——它只有重置门与更新门两个

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
