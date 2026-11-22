---
id: Q-1748
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 55 题）
module: 04_algo
sub: 函数与异常
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
x = torch.tensor([2.0], requires_grad=True)
(x * 3).sum().backward()
(x * 5).sum().backward()
print(x.grad.tolist())
```

- **A.** [8.0]
- **B.** [3.0]
- **C.** [5.0]
- **D.** [0.0]

## 口述答案

答案是 **A. [8.0]**，实际输出 `[8.0]`。

梯度默认累加不清零：第二次 backward 又加上 5，累计 3+5=8。PyTorch 不会自动清梯度，这是训练循环里必须 zero_grad 的原因。

## 讲深一层

讲深一层：backward 只做「把本次梯度加到 .grad」，从不覆盖，所以两次反向得 3+5=8；每次前向都会新建计算图，第二次的图与第一次无关，但 .grad 这个缓冲区是共享的。这个设计不是 bug——梯度累积分批训练正是靠它把小 batch 的梯度攒成大 batch，代价是每轮必须手动 zero_grad。

## 高频追问

1. **怎么得到只含第二次的梯度？** —— backward 前 `x.grad.zero_()` 或优化器 zero_grad()。
2. **为什么设计成累加？** —— 支持梯度累积模拟大 batch。
3. **第二次 backward 会复用旧图吗？** —— 不会，每次前向新建图。

## 易错点

- 以为第二次覆盖第一次：实际得 8 不是 5
- 训练循环忘记 zero_grad：梯度累积，loss 震荡不收敛
- 以为重复 backward 一定报错：同一张图第二次才报，这里每次新建图所以合法

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
