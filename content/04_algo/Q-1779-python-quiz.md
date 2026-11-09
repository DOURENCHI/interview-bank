---
id: Q-1779
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 86 题）
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
logits = torch.tensor([2.0, -2.0])
y = torch.tensor([1.0, 0.0])
a = float(torch.nn.BCELoss()(torch.sigmoid(logits), y))
b = float(torch.nn.BCEWithLogitsLoss()(logits, y))
print([round(v, 6) for v in torch.sigmoid(logits).tolist()], round(a, 6), round(b, 6))
```

- **A.** [0.880797, 0.119203] 0.126928 0.126928
- **B.** ([0.880797, 0.119203], 0.126928, 0.693147)
- **C.** ([0.119203, 0.880797], 0.126928, 0.126928)
- **D.** ([0.880797, 0.119203], 0.0, 0.693147)

## 口述答案

答案是 **A. [0.880797, 0.119203] 0.126928 0.126928**，实际输出 `[0.880797, 0.119203] 0.126928 0.126928`。

BCEWithLogitsLoss 把 sigmoid 和 BCELoss 融合成一个数值稳定的操作，结果与手动两步完全相同（0.126928）。数值大时别先 sigmoid。

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
