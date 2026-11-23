---
id: Q-1801
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 108 题）
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
m = torch.nn.Linear(2, 1)
print(m.weight_decay if hasattr(m, "weight_decay") else "n/a")
```

- **A.** n/a
- **B.** 0.01
- **C.** 0.0
- **D.** 1e-4

## 口述答案

答案是 **A. n/a**，实际输出 `n/a`。

weight_decay 是优化器的参数不是层的参数，所以 Linear 上没有这个属性——要写在 torch.optim.SGD(..., weight_decay=...) 里。

## 讲深一层

`weight_decay` 是优化器超参，按 `θ ← θ − lr(g + wd·θ)` 施加，层不持有。`Module.__getattr__` 只查参数、buffer 与子模块，找不到抛 AttributeError，所以 `hasattr` 为 False。要分层设 wd 得拆 param_groups。

## 高频追问

1. **`hasattr` 为什么是 False？** —— Module 未定义该属性，`__getattr__` 找不到就抛 AttributeError，`hasattr` 捕获后返回 False
2. **怎么给某层单独设 wd？** —— 分成两个 param_group，BN 与 bias 那组设 `weight_decay=0`
3. **Adam 的 wd 与 AdamW 差在哪？** —— 前者把 wd 混进梯度被自适应缩放，后者解耦成独立衰减项

## 易错点

- 写 `nn.Linear(2, 1, weight_decay=0.01)`——`TypeError: __init__() got an unexpected keyword argument`
- 以为层里能读 wd——`hasattr` 为 False，打印出 `n/a` 就是本题答案
- 以为 L2 与 weight decay 等价——Adam 下不等价，这是 AdamW 的动机

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
