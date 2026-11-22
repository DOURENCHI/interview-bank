---
id: Q-1762
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 69 题）
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
m = torch.nn.Linear(2, 1)
out = m(torch.randn(4, 2))
print(tuple(out.shape), out.requires_grad)
```

- **A.** (4, 1) True
- **B.** ((1, 4), True)
- **C.** ((4, 2), True)
- **D.** ((4, 1), False)

## 口述答案

答案是 **A. (4, 1) True**，实际输出 `(4, 1) True`。

批大小 4、每样本 2 维输入，输出形状 (4,1)；因为参数需要梯度，输出自动带上计算图，requires_grad 为 True。

## 讲深一层

`requires_grad` 沿计算图传播：任一浮点输入需要梯度，输出就需要。这里输入默认 False，但 weight/bias 是 True，所以 out 为 True 并挂 grad_fn。整数张量不能求导，`nn.Linear` 喂 long 直接报 dtype 错。

## 高频追问

1. **什么时候输出会是 False？** —— 包在 `torch.no_grad()` / `inference_mode()` 里，或所有参数的 `requires_grad` 都被冻结
2. **为什么形状是 `(4,1)` 不是 `(1,4)`？** —— 第一维是 batch（4 个样本），最后一维是 out_features=1
3. **想让输入也参与求导怎么办？** —— 先 `x.requires_grad_(True)`（x 必须是浮点），再前向，`out.grad_fn` 会多一层

## 易错点

- 认为输入没设 requires_grad 所以输出 False——参数是 True，输出就跟着 True
- 把形状写成 `(1,4)`——`Linear(2,1)` 输出最后一维恒为 1
- 以为 `requires_grad` 是只读属性——`.requires_grad_(True)` 可原地改，但只对叶子张量有意义

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
