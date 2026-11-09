---
id: Q-1791
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 98 题）
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
cell = torch.nn.RNNCell(4, 5)
h = torch.zeros(2, 5)
shapes = []
for _ in range(3):
    h = cell(torch.randn(2, 4), h)
    shapes.append(tuple(h.shape))
print(shapes)
```

- **A.** [(2, 5), (2, 5), (2, 5)]
- **B.** [(2, 4), (2, 4), (2, 4)]
- **C.** [(2, 6), (2, 6), (2, 6)]
- **D.** [(5, 2), (5, 2), (5, 2)]

## 口述答案

答案是 **A. [(2, 5), (2, 5), (2, 5)]**，实际输出 `[(2, 5), (2, 5), (2, 5)]`。

RNNCell 一次处理一个时间步，输入 (批, 输入特征4)、隐状态 (批, 隐层5)，输出隐状态形状恒为 (2,5)。

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
