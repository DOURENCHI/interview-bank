---
id: Q-1763
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 70 题）
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
m = torch.nn.Sequential(torch.nn.Linear(4, 8), torch.nn.ReLU(), torch.nn.Linear(8, 1))
print(sum(p.numel() for p in m.parameters()))
```

- **A.** 49
- **B.** 41
- **C.** 37
- **D.** 56

## 口述答案

答案是 **A. 49**，实际输出 `49`。

第一层 4×8+8 = 40，第二层 8×1+1 = 9，ReLU 无参数，合计 49。这是判断模型复杂度的第一个数字。

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
