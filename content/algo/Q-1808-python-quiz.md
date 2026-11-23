---
id: Q-1808
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 115 题）
module: algo
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
torch.manual_seed(13)
a = torch.randn(3).tolist()
torch.manual_seed(13)
b = torch.randn(3).tolist()
print(a == b, [round(v, 6) for v in a])
```

- **A.** True [-0.111659, -1.14561, 1.410316]
- **B.** (False, [-0.111659, -1.14561, 1.410316])
- **C.** (True, [0.111659, 1.14561, -1.410316])
- **D.** (False, [0.0, 0.0, 0.0])

## 口述答案

答案是 **A. True [-0.111659, -1.14561, 1.410316]**，实际输出 `True [-0.111659, -1.14561, 1.410316]`。

固定 seed 后随机序列完全可复现，所以两次结果完全相等。不固定 seed 就没法复现 bug。

## 讲深一层

`manual_seed` 重置 CPU 全局 RNG，同种子同调用序列必得同结果，所以两次 `randn(3)` 全等。GPU 要另调 `cuda.manual_seed_all`；cuDNN 的 benchmark 会换算法，还需 `cudnn.deterministic=True` 才真可复现。

## 高频追问

1. **为什么两次完全相同？** —— RNG 状态被重置到同一起点，序列从头重放
2. **换个 seed 数值会变吗？** —— 会，生成的序列完全不同
3. **为什么线上仍可能不可复现？** —— DataLoader worker 种子、cuDNN 算法选择、多线程浮点归约顺序

## 易错点

- 认为 seed 只影响第一次调用——它重置整个状态，后续序列都可复现
- 只设 CPU seed——GPU 张量仍随机，需 `manual_seed_all`
- 以为设了 seed 就完全确定——cuDNN benchmark 与多 worker 仍引入不确定性

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
