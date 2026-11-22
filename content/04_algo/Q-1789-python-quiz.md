---
id: Q-1789
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 96 题）
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
import torch
c = torch.nn.Conv2d(64, 32, 1)
print(tuple(c(torch.randn(1, 64, 8, 8)).shape), c.weight.shape)
```

- **A.** (1, 32, 8, 8) torch.Size([32, 64, 1, 1])
- **B.** ((1, 64, 8, 8), torch.Size([32, 64, 1, 1]))
- **C.** ((1, 32, 8, 8), torch.Size([64, 32, 1, 1]))
- **D.** ((1, 32, 7, 7), torch.Size([32, 64, 1, 1]))

## 口述答案

答案是 **A. (1, 32, 8, 8) torch.Size([32, 64, 1, 1])**，实际输出 `(1, 32, 8, 8) torch.Size([32, 64, 1, 1])`。

1×1 卷积只改通道数不改空间尺寸：64→32，8×8 不变；权重形状 (out=32, in=64, 1, 1)。

## 讲深一层

1×1 卷积在通道维做线性组合，等价于对每个像素施加一个 `Linear(64,32)`，权重跨空间位置共享。k=1、p=0、s=1 时输出尺寸公式退化为 H 不变，所以 8×8 原样保留。它常用来升降维（NiN、ResNet bottleneck），参数量 `32×64+32 = 2080`，与特征图大小无关。

## 高频追问

1. **参数量多少？** —— 2080，`32×64` 加 32 个 bias
2. **与 `Linear(64,32)` 的区别？** —— 逐像素共享同一组权重，不依赖像素位置
3. **1×1 能改空间尺寸吗？** —— 只能靠 `stride>1`（或后续池化），核本身不缩尺寸

## 易错点

- 答 `(1,32,7,7)`——把 1×1 当 3×3 减了核，即选项 D
- weight 写成 `(64,32,1,1)`——通道顺序反了，即选项 C
- 认为 1×1 卷积没有参数——它是最小的可学习通道变换

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
