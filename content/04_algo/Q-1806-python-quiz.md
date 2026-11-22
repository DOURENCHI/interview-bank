---
id: Q-1806
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 113 题）
module: 04_algo
sub: 并发与性能
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-21
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

`torch.device("cpu")` 打印 `cpu`，其 `index` 为 None——CPU 没有卡号概念。CUDA 张量打印 `cuda:0`，因为要多卡区分。`torch.zeros(2)` 默认落在 CPU，不会因为装了 CUDA 版就自动上卡，必须显式 `.to("cuda")`。

## 高频追问

1. **为什么不是 `cpu:0`？** —— CPU 无索引，`torch.device("cpu").index` 是 None
2. **怎么判断有可用 GPU？** —— `torch.cuda.is_available()`，再配合 `torch.cuda.device_count()`
3. **`.to("cuda")` 在无卡机器上？** —— 报 `AssertionError: Torch not compiled with CUDA enabled`

## 易错点

- 答 `cpu:0`——那是 CUDA 风格写法，CPU 不带索引
- 用字符串比较 device——应比较 `torch.device` 对象，字符串形式不保证一致
- 认为 `zeros` 默认在 cuda——默认 CPU，需显式搬运

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
