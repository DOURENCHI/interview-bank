---
id: Q-1745
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 51 题）
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
