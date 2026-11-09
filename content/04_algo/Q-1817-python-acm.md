---
id: Q-1817
title: CNN：卷积、池化与维度计算 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: draft
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

x = torch.arange(25, dtype=torch.float32).reshape(1, 1, 5, 5)
conv = nn.Conv2d(1, 1, kernel_size=3, bias=False)
with torch.no_grad():
    conv.weight.fill_(1.0)
out = conv(x)
print("5x5 经 3x3 卷积 ->", tuple(out.shape))
print("输出值", out.reshape(-1).tolist())

pool = nn.MaxPool2d(2)
print("2x2 池化 ->", tuple(pool(torch.tensor([[[[1.0, 2.0], [3.0, 4.0]]]])).shape))

flat = nn.Sequential(nn.Conv2d(1, 10, 3), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten())
print("28x28 全流程 ->", tuple(flat(torch.randn(1, 1, 28, 28)).shape))

print("尺寸公式 (28-3)//2+1 =", (28 - 3) // 2 + 1)

c11 = nn.Conv2d(64, 32, 1)
print("1x1 卷积 ->", tuple(c11(torch.randn(1, 64, 8, 8)).shape), "权重", tuple(c11.weight.shape))
```

输出样例：

```
5x5 经 3x3 卷积 -> (1, 1, 3, 3)
输出值 [54.0, 63.0, 72.0, 99.0, 108.0, 117.0, 144.0, 153.0, 162.0]
2x2 池化 -> (1, 1, 1, 1)
28x28 全流程 -> (1, 1690)
尺寸公式 (28-3)//2+1 = 13
1x1 卷积 -> (1, 32, 8, 8) 权重 (32, 64, 1, 1)
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

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
