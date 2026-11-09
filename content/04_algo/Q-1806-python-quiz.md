---
id: Q-1806
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 113 题）
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
print(torch.device("cpu"), torch.zeros(2).device)
```

- **A.** cpu cpu
- **B.** cpu:0 cpu:0
- **C.** cuda:0 cuda:0
- **D.** None None

## 口述答案

答案是 **A. cpu cpu**，实际输出 `cpu cpu`。

本机是 CPU 版 PyTorch，device 就是 cpu；装了 CUDA 版才会出现 cuda:0。

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
