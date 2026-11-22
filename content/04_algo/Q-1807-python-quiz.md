---
id: Q-1807
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 114 题）
module: 04_algo
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
m = torch.nn.Linear(2, 1)
with torch.inference_mode():
    out = m(torch.ones(1, 2))
print(out.requires_grad)
```

- **A.** False
- **B.** True
- **C.** None
- **D.** 0

## 口述答案

答案是 **A. False**，实际输出 `False`。

inference_mode 比 no_grad 更彻底，连版本计数都不记，推理首选；no_grad 也能达到不建图的效果。

## 讲深一层

`inference_mode` 除禁用梯度外还禁用 version counter（版本计数），张量更轻、开销更小。代价是这些张量之后不能参与需要 autograd 记录的计算，否则报错；`no_grad` 只关梯度，退出后张量还能重新入图。所以纯推理用前者，推理后还要训的用后者。

## 高频追问

1. **与 `no_grad` 的区别？** —— 更彻底，连版本计数都不记，并禁止后续参与 autograd
2. **输出能 backward 吗？** —— 不能，报 `Inference tensors cannot be saved for backward`
3. **什么时候只能用 `no_grad`？** —— 推理结果还要接着求导/训练的流水线

## 易错点

- 认为两者完全等价——`inference_mode` 更严格也更快
- 在 `inference_mode` 里建要训的张量——后续 backward 直接报错
- 以为 `requires_grad` 变 None——是 False，不是 None

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
