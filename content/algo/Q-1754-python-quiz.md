---
id: Q-1754
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 61 题）
module: algo
sub: 语法与类型
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

PyTorch 默认 dtype 与 NumPy 相反：整数给 int64，浮点给 float32（NumPy 是 float64），为省显存与提吞吐。要双精度须显式指定。`device` 打印 `cpu` 不带 `:0`，因为 CPU 无卡号、`index` 为 None；CUDA 才打印 `cuda:0`。

## 高频追问

1. **为什么浮点默认 float32 而 NumPy 是 float64？** —— 深度学习对精度不敏感但对显存与带宽敏感，fp32 在 GPU 上吞吐是 fp64 的数倍
2. **`torch.Tensor([1,2])` 和 `torch.tensor([1,2])` 一样吗？** —— 不一样，前者是构造函数别名固定产出 float32，后者按字面量推断得 int64
3. **int64 与 float32 相加结果是什么类型？** —— 提升为 float32，可用 `torch.result_type` 验证；float64 与 float32 相加则得 float64

## 易错点

- 以为整数默认 int32——实际是 `torch.int64`，答 int32 就选了 B
- 以为 device 打印 `cpu:0`——CPU 无索引，`str(t.device)` 就是 `cpu`
- 把 NumPy 的 float64 习惯带过来——`np.array([1.0])` 转 torch 后是 float64，与 float32 模型相加报 dtype 错

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
