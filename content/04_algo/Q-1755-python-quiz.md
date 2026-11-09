---
id: Q-1755
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 61 题）
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
print(torch.tensor([1, 2]).dtype, torch.tensor([1.0]).dtype, torch.tensor([1, 2]).device)
```

- **A.** torch.int64 torch.float32 cpu
- **B.** torch.int32 torch.float64 cpu
- **C.** torch.int64 torch.float32 cuda
- **D.** torch.int64 torch.float32 cpu:0

## 口述答案

答案是 **A. torch.int64 torch.float32 cpu**，实际输出 `torch.int64 torch.float32 cpu`。

整数字面量默认 int64、浮点默认 float32；device 是 cpu（CPU 版 PyTorch 没有 cuda）。装 CUDA 版 torch 才会是 cuda:0。

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

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
