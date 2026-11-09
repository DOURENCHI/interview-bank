---
id: Q-1761
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 68 题）
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
m = torch.nn.Linear(3, 2)
print(tuple(m.weight.shape), tuple(m.bias.shape), m.weight.shape[0] * m.weight.shape[1] + 2)
```

- **A.** (2, 3) (2,) 8
- **B.** ((3, 2), (3,), 8)
- **C.** ((2, 3), (2,), 6)
- **D.** ((2, 3), (2,), 2)

## 口述答案

答案是 **A. (2, 3) (2,) 8**，实际输出 `(2, 3) (2,) 8`。

Linear(3,2) 是「3 个输入 → 2 个输出」，权重形状 (out, in) = (2,3)、偏置 2 个，共 2×3+2 = 8 个参数。

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
