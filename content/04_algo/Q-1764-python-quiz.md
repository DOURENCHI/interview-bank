---
id: Q-1764
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 71 题）
module: 04_algo
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

`sum().backward()` 上游梯度为 1，故 `∂Σout/∂w = x = 1`，与 w 初值无关；两次都在 backward 前清了零，所以都是 1.0。删掉 `zero_grad()` 才会累加。梯度是累加不是覆盖，这是支持多 loss 反传的设计代价。

## 高频追问

1. **删掉 `m.zero_grad()` 结果如何？** —— g2 变 2.0，第二次 backward 在旧梯度上叠加，训练会不知不觉放大步长
2. **为什么梯度与 w 无关？** —— 输出是 `xw+b`，对 w 的偏导就是 x，这里 x=1
3. **清零有哪几种写法？** —— `opt.zero_grad()`、`m.zero_grad()`、`p.grad = None`；前两者默认 `set_to_none=True`

## 易错点

- 认为不清零会自动覆盖——实际是累加，多轮后梯度成倍增长
- 把 g1 算成 w 的初值——权重初值是随机数，而梯度只由 x 决定
- 认为 `backward()` 会自动清零——它只累加，清不清零是调用方的事

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
