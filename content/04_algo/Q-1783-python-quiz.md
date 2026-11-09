---
id: Q-1783
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 89 题）
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
logits = torch.tensor([0.5, -0.5, 1.5])
y = torch.tensor([1.0, 0.0, 1.0])
a = float(torch.nn.BCELoss()(torch.sigmoid(logits), y))
b = float(torch.nn.BCEWithLogitsLoss()(logits, y))
print(round(a, 6), round(b, 6))
```

- **A.** 0.383189 0.383189
- **B.** (0.383189, 0.693147)
- **C.** (0.5, 0.5)
- **D.** (0.0, 0.0)

## 口述答案

答案是 **A. 0.383189 0.383189**，实际输出 `0.383189 0.383189`。

两种写法数值完全一致（0.383189），这是 BCEWithLogitsLoss 存在的意义：省一次 sigmoid，且数值更稳。

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
