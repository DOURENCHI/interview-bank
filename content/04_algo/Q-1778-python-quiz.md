---
id: Q-1778
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 85 题）
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
p = torch.tensor([0.8, 0.2])
y = torch.tensor([1.0, 0.0])
print(round(float(torch.nn.BCELoss()(p, y)), 6))
```

- **A.** 0.223144
- **B.** 0.5
- **C.** 0.8
- **D.** 0.0

## 口述答案

答案是 **A. 0.223144**，实际输出 `0.223144`。

BCELoss = -[y·log(p) + (1-y)·log(1-p)]，代入得 -(1×log0.8 + log0.8) = -2×log0.8 = 0.223144。

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

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
