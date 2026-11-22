---
id: Q-1744
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 51 题）
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
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
z = x * 2
loss = (z - 3).pow(2).sum()
loss.backward()
print(x.grad.tolist())
```

- **A.** [-4.0, 4.0, 12.0]
- **B.** [-4.0, 0.0, 4.0]
- **C.** [2.0, 4.0, 6.0]
- **D.** [-8.0, 0.0, 8.0]

## 口述答案

答案是 **A. [-4.0, 4.0, 12.0]**，实际输出 `[-4.0, 4.0, 12.0]`。

loss = (2x-3)² 之和，d/dx = 4(2x-3) = 8x-12，代入 x=1,2,3 得 -4, 4, 12。注意中间结果 x=2 时 z=4 离目标 3 还有 1，所以梯度不为 0。

## 讲深一层

讲深一层：计算图把 z=2x 与 loss=(z-3)² 串起来，反向先对 z 求导得 2(z-3)，再乘 z 对 x 的导数 2，合起来 4(2x-3)=8x-12，代入得 -4/4/12。梯度只累加到叶子张量的 .grad，中间结果 z.grad 为 None。requires_grad 只对浮点张量有效。

## 高频追问

1. **为什么 x=2 时梯度不是 0？** —— z=4，距目标 3 还差 1，4(2x-3)=4。
2. **中间变量有 grad 吗？** —— 没有，只有叶子节点累积，除非调用 retain_grad()。
3. **梯度形状和 x 一致吗？** —— 一致，逐元素。

## 易错点

- 忘记链式法则的系数 2：只算 2(2x-3) 得 [-2,2,6]，选错选项
- 以为 (z-3)² 在 z=4 时梯度为零：错，只有 z=3 才为零
- 用整型 tensor 开 requires_grad：抛 RuntimeError，只有浮点支持

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
