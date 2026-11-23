---
id: Q-1788
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 95 题）
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
conv = torch.nn.Conv2d(3, 16, 3)
x = torch.randn(1, 3, 8, 8)
print(tuple(conv(x).shape), conv.weight.shape[0])
```

- **A.** (1, 16, 6, 6) 16
- **B.** ((1, 3, 6, 6), 3)
- **C.** ((1, 16, 8, 8), 16)
- **D.** ((1, 16, 6, 6), 3)

## 口述答案

答案是 **A. (1, 16, 6, 6) 16**，实际输出 `(1, 16, 6, 6) 16`。

输出通道数由 out_channels=16 决定，空间尺寸由核和输入决定；weight 形状是 (16, 3, 3, 3)，第 0 维就是输出通道 16。

## 讲深一层

输出通道数只由 `out_channels` 决定，与输入通道无关；输入通道必须等于 `in_channels`，否则直接报错。weight 形状 `(out, in, kH, kW) = (16,3,3,3)`，bias `(16,)`，共 `16×3×3×3+16 = 448` 个参数。空间尺寸 `8−3+1=6`，与通道数互不影响。

## 高频追问

1. **这个层多少参数？** —— 448，`16×3×3×3` 加 16 个 bias
2. **输入通道传错会怎样？** —— `RuntimeError: expected input to have 3 channels, but got 1`
3. **为什么 weight 第 0 维是 out？** —— 与 Linear 的 out-first 约定一致，便于按输出通道切分与并行

## 易错点

- 答 `(1,3,6,6)`——以为通道跟着输入走，这是选项 B 的坑
- 把 `weight.shape[0]` 说成 3——那是 in_channels，第 0 维是 16
- 忘记 bias——参数算成 432，少 16

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
