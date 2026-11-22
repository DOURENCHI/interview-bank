---
id: Q-1746
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 53 题）
module: 04_algo
sub: 容器与切片
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
x = torch.tensor([1.0, 2.0], requires_grad=True)
y = x * x
y.sum().backward()
print(x.grad.tolist())
```

- **A.** [2.0, 4.0]
- **B.** [1.0, 4.0]
- **C.** [2.0, 2.0]
- **D.** [4.0, 4.0]

## 口述答案

答案是 **A. [2.0, 4.0]**，实际输出 `[2.0, 4.0]`。

y = x²，dy/dx = 2x，代入 1 和 2 得 2 和 4。自动微分对每个元素分别算梯度。

## 讲深一层

讲深一层：y=x*x 是逐元素平方，dy/dx=2x，所以 1、2 分别得 2、4；这里 x 在乘法里出现两次，反向时两条边各贡献一份 x，加起来正好 2x，这也解释了为什么 x*x 与 x**2 梯度相同。若把 sum 去掉直接对向量 backward，必须显式传 gradient 参数指定上游梯度。

## 高频追问

1. **x\*x 和 x\*\*2 梯度一样吗？** —— 一样，都是 2x。
2. **为什么每个元素独立？** —— 逐元素运算，互不耦合。
3. **不求 sum 怎么反向？** —— `y.backward(torch.ones_like(y))`。

## 易错点

- 把梯度算成 x 本身：得 [1,2]，漏掉系数 2
- 以为乘法要跨元素求和：逐元素乘不耦合，梯度逐元素独立
- 对向量直接 backward：抛 RuntimeError，需传 gradient

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
