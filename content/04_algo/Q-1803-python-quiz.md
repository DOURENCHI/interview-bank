---
id: Q-1803
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 109 题）
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
torch.manual_seed(10)
d = torch.nn.Dropout(0.5)
d.train()
out = d(torch.ones(1000))
print(round(float((out == 0).float().mean()), 4))
```

- **A.** 0.499
- **B.** 0.5, 
- **C.** 0.999
- **D.** 0.0

## 口述答案

答案是 **A. 0.499**，实际输出 `0.499`。

Dropout 在 train 模式按 p=0.5 随机置零，实测 1000 个里有 499 个是 0，接近 0.5。

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

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
