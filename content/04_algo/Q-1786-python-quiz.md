---
id: Q-1786
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 93 题）
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
