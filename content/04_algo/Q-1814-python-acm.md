---
id: Q-1814
title: nn.Module：参数量、冻结与 train/eval 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: indexed
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 Python 程序对应的读入与输出写法是什么？

```python
import torch
import torch.nn as nn

torch.manual_seed(3)

m = nn.Linear(3, 2)
print("weight", tuple(m.weight.shape), "bias", tuple(m.bias.shape))
print("参数量", sum(p.numel() for p in m.parameters()))

seq = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 1))
print("Sequential 参数量", sum(p.numel() for p in seq.parameters()))
print("前向输出形状", tuple(seq(torch.randn(4, 4)).shape))

for p in m.parameters():
    p.requires_grad_(False)
print("冻结后仍有可训练参数吗", any(p.requires_grad for p in m.parameters()))

torch.manual_seed(5)
dp = nn.Sequential(nn.Linear(4, 4), nn.Dropout(0.5))
dp.train()
a = float(dp(torch.ones(1, 4)).sum().detach())
dp.eval()
b = float(dp(torch.ones(1, 4)).sum().detach())
print(f"train 模式输出和 {a:.4f} | eval 模式输出和 {b:.4f}")
```

输出样例：

```
weight (2, 3) bias (2,)
参数量 8
Sequential 参数量 49
前向输出形状 (4, 1)
冻结后仍有可训练参数吗 False
train 模式输出和 3.4002 | eval 模式输出和 1.4552
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
