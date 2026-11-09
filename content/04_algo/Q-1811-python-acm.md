---
id: Q-1811
title: autograd：梯度、累加与 no_grad 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: draft
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 Python 程序对应的读入与输出写法是什么？

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
z = x * 2
loss = (z - 3).pow(2).sum()
loss.backward()
print("x.grad =", x.grad.tolist())

y = torch.tensor([2.0], requires_grad=True)
(y * 3).sum().backward()
(y * 5).sum().backward()
print("两次 backward 后 y.grad =", y.grad.tolist(), "（梯度累加）")

m = torch.tensor([1.0], requires_grad=True)
with torch.no_grad():
    n = m * 2
print("no_grad 下 requires_grad =", n.requires_grad)

t = torch.tensor([1.0, 2.0])
print("item() =", t.sum().item(), "| 直接 print =", t.sum())
```

输出样例：

```
x.grad = [-4.0, 4.0, 12.0]
两次 backward 后 y.grad = [8.0] （梯度累加）
no_grad 下 requires_grad = False
item() = 3.0 | 直接 print = tensor(3.)
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
