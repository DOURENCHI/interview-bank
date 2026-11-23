---
id: Q-1786
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 93 题）
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
m = torch.nn.Sequential(torch.nn.Conv2d(1, 10, 3), torch.nn.ReLU(), torch.nn.MaxPool2d(2), torch.nn.Flatten())
print(tuple(m(torch.randn(1, 1, 28, 28)).shape))
```

- **A.** (1, 1690)
- **B.** ((1, 10),)
- **C.** ((1, 1, 28, 28),)
- **D.** ((1, 784),)

## 口述答案

答案是 **A. (1, 1690)**，实际输出 `(1, 1690)`。

28 → 卷积3核 26 → 池化 13，13×13×10 = 1690。Flatten 把每张特征图拉平，这正是「320 是怎么来的」那类计算。

## 讲深一层

28 经 3×3 无 padding 卷积得 26，2×2 池化得 13，通道 10，展平后 `13×13×10 = 1690`。`Flatten` 默认从 `dim=1` 开始，保留 batch 维。这条链是 CNN 分类头的标准算法：空间尺寸按 `(H−k)/s+1` 缩，通道按 `out_channels` 变，最后乘起来就是全连接层输入维度。

## 高频追问

1. **`Flatten` 从哪维开始展平？** —— 默认 `start_dim=1`，batch 保留，所以是 `(1,1690)` 而不是 `(1690,)`
2. **卷积加 `padding=1` 结果多少？** —— 28→28→14，`14×14×10 = 1960`
3. **这个卷积层参数量多少？** —— `10×1×3×3 + 10 = 100`，与输入尺寸无关

## 易错点

- 忘除 2——得 `26×26×10 = 6760`，漏掉池化
- 用 `28/2=14` 当卷积后尺寸——卷积先减核再加一
- 把通道乘在最前面——维度顺序是 `(N,C,H,W)`，展平后是 `C×H×W`

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
