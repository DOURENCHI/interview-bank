---
id: Q-1795
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 102 题）
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
import torch.nn as nn
import torch.nn.functional as F
class Res(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.c1 = nn.Conv2d(c, c, 3, padding=1)
        self.c2 = nn.Conv2d(c, c, 3, padding=1)
    def forward(self, x):
        return x + self.c2(F.relu(self.c1(x)))
print(tuple(Res(8)(torch.randn(1, 8, 16, 16)).shape))
```

- **A.** (1, 8, 16, 16)
- **B.** ((1, 16, 16, 16),)
- **C.** ((1, 8, 14, 14),)
- **D.** ((1, 8, 8, 8),)

## 口述答案

答案是 **A. (1, 8, 16, 16)**，实际输出 `(1, 8, 16, 16)`。

padding=1 保持空间尺寸，残差相加要求形状一致，所以残差块进出形状完全相同——这是残差能「深下去」的前提。

## 讲深一层

3×3 卷积配 `padding=1`、`stride=1`，输出满足 `H+2−3+1 = H`，所以残差块进出完全同形，`x + F(x)` 才合法。通道若变化必须加 1×1 投影把 x 变到同通道，否则广播失败或报错。恒等通路让梯度直接回传，这是深网可训的前提。

## 高频追问

1. **c1 改成 2c 通道会怎样？** —— 相加报 shape mismatch，需要 downsample 分支做 1×1 投影
2. **去掉 padding 呢？** —— 16→14，空间维不符，无法相加
3. **为什么残差好训？** —— 梯度有恒等旁路，缓解连乘导致的消失

## 易错点

- 忘 padding 直接相加——报 `The size of tensor a (14) must match tensor b (16)`
- 以为会自动 broadcast 到 `(1,16,16,16)`——通道 8≠16 且空间维不同，广播失败
- 把残差写成 `cat`——通道翻倍，下游形状全变

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
