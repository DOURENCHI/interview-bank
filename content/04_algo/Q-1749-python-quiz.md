---
id: Q-1749
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 55 题）
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
