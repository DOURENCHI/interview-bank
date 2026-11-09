---
id: Q-1798
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 105 题）
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
m = torch.nn.Linear(2, 1)
m(torch.ones(1, 2)).sum().backward()
g = float(m.weight.grad.sum())
m.zero_grad()
print(round(g, 6), m.weight.grad)
```

- **A.** 2.0 None
- **B.** (2.0, 0.0)
- **C.** (None, None)
- **D.** (1.0, 1.0)

## 口述答案

答案是 **A. 2.0 None**，实际输出 `2.0 None`。

zero_grad 之后梯度变成 None（不是 0），因为 PyTorch 用 None 表示「没有梯度」以节省内存；这是判断有没有清零成功的标志。

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

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
