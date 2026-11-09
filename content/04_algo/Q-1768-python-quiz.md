---
id: Q-1768
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 75 题）
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
m = torch.nn.Linear(2, 2)
for p in m.parameters():
    p.requires_grad_(False)
print(any(p.requires_grad for p in m.parameters()))
```

- **A.** False
- **B.** True
- **C.** None
- **D.** 0

## 口述答案

答案是 **A. False**，实际输出 `False`。

requires_grad_(False) 冻结参数后，any 判断为 False。做迁移学习或只训部分层时就靠它。

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
