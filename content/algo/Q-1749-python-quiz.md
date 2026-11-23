---
id: Q-1749
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 56 题）
module: algo
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
x = torch.tensor([1.0], requires_grad=True)
with torch.no_grad():
    y = x * 2
print(y.requires_grad)
```

- **A.** False
- **B.** True
- **C.** None
- **D.** 0

## 口述答案

答案是 **A. False**，实际输出 `False`。

no_grad 上下文里所有运算都不记录计算图，输出张量不再需要梯度——推理阶段用它省内存省时间。

## 讲深一层

讲深一层：no_grad 关掉的是「记录计算图」，不是关掉计算，y 仍是正常张量、数值正确，只是 requires_grad 为 False、grad_fn 为 None。它按线程生效，可作上下文管理器或装饰器；PyTorch 1.9 起推理更推荐 inference_mode()，省得更多，但结果不能再参与求导。

## 高频追问

1. **no_grad 里张量还能求导吗？** —— 不能，图没建，backward 会报错。
2. **和 inference_mode 区别？** —— 后者更彻底，禁止结果再被用于自动微分。
3. **为什么推理要用它？** —— 省显存和计算，避免无谓建图。

## 易错点

- 以为 y 变成普通 list 或 numpy：仍是 Tensor，只是不需要梯度
- 在 no_grad 里取 x.grad：拿不到，图未建、梯度为 None
- 以为影响其他线程：它是线程局部的，别的线程照常建图

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
