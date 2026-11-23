---
id: Q-1745
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 52 题）
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
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
(x * 2).sum().backward()
print(x.grad.tolist())
```

- **A.** [2.0, 2.0, 2.0]
- **B.** [1.0, 1.0, 1.0]
- **C.** [2.0, 4.0, 6.0]
- **D.** [0.0, 0.0, 0.0]

## 口述答案

答案是 **A. [2.0, 2.0, 2.0]**，实际输出 `[2.0, 2.0, 2.0]`。

z = 2x，dz/dx = 2，所以每个元素的梯度都是 2——线性函数的梯度是常数。

## 讲深一层

讲深一层：sum 的反向是把上游梯度 1 原样分给每个元素，所以 (2x).sum() 对每个 x 的梯度都是 2，与 x 取值无关——线性函数的导数就是系数。若把 sum 换成 mean，梯度会被均摊成 2/n，n=3 时约 0.667，这是损失函数选择直接影响梯度尺度的典型例子。

## 高频追问

1. **换成 mean 梯度是多少？** —— 2/3≈0.667，因为除以了元素个数。
2. **梯度为什么与 x 无关？** —— 线性函数导数是常数系数。
3. **不做 sum 直接 backward 行吗？** —— 只有标量能直接 backward，向量要传 gradient 参数。

## 易错点

- 以为梯度是 [2,4,6]：那是函数值 2x，不是导数
- 把 sum 当平均：sum 不减除，梯度仍是 2 不是 0.667
- 对向量 loss 直接 backward：抛 RuntimeError: grad can be implicitly created only for scalar outputs

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
