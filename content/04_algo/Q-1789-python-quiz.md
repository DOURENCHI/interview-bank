---
id: Q-1789
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 95 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
