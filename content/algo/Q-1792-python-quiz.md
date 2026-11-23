---
id: Q-1792
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 99 题）
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
import torch
lstm = torch.nn.LSTM(4, 5, batch_first=True)
print(tuple(lstm(torch.randn(2, 7, 4))[0].shape))
```

- **A.** (2, 7, 5)
- **B.** ((2, 4, 7),)
- **C.** ((1, 2, 5),)
- **D.** ((2, 7, 4),)

## 口述答案

答案是 **A. (2, 7, 5)**，实际输出 `(2, 7, 5)`。

LSTM 与 RNN 输出形状相同 (批, 序列长, 隐层)，区别在于内部多了门控与细胞状态。

## 讲深一层

LSTM 返回 `(out, (h_n, c_n))`——第二个元素本身还是二元组，最容易漏。out 形状与 RNN 相同 `(B,T,H)`，`h_n`、`c_n` 都是 `(num_layers,B,H)`。`[0]` 只取 out，所以打印 `(2,7,5)`。cell state 是 LSTM 区别于 RNN 的关键，也是它擅长长依赖的原因。

## 高频追问

1. **返回几个值？** —— 两个，第二个是 `(h_n, c_n)` 元组，解包要写 `out, (h, c) = lstm(x)`
2. **h 和 c 的形状？** —— 都是 `(1,2,5)`，层数、批、隐层
3. **为什么写 `[0]`？** —— 返回值是 tuple，没有 `.shape` 属性，必须取第一项

## 易错点

- 写 `lstm(x).shape`——报 `AttributeError: 'tuple' object has no attribute 'shape'`
- 以为返回 `(out, h)` 两元组——实际第二项还套了一层
- 输出宽度写成 `2×hidden`——门控在内部，不改变输出维度

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
