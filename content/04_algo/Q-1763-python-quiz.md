---
id: Q-1763
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 69 题）
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
