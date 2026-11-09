---
id: Q-1768
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 74 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
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
m = torch.nn.Linear(2, 2)
print(all(p.requires_grad for p in m.parameters()))
```

- **A.** True
- **B.** False
- **C.** None
- **D.** 0

## 口述答案

答案是 **A. True**，实际输出 `True`。

nn.Module 的参数默认 requires_grad=True，所以全部为真——这是梯度能自动回传的前提。

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
