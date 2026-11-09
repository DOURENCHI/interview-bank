---
id: Q-1764
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 71 题）
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
torch.manual_seed(3)
m = torch.nn.Linear(1, 1)
m(torch.ones(1, 1)).sum().backward()
g1 = float(m.weight.grad.sum())
m.zero_grad()
m(torch.ones(1, 1)).sum().backward()
g2 = float(m.weight.grad.sum())
print(round(g1, 6), round(g2, 6))
```

- **A.** 1.0 1.0
- **B.** (2.0, 1.0)
- **C.** (1.0, 2.0)
- **D.** (0.0, 0.0)

## 口述答案

答案是 **A. 1.0 1.0**，实际输出 `1.0 1.0`。

不调 zero_grad 时梯度会累加成 2.0；清零后再算是 1.0。两者数值相同是巧合（这里权重恰好为 1），关键是「必须清零」这件事。

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

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
