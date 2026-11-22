---
id: Q-1781
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 88 题）
module: 04_algo
sub: 函数与异常
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
logits = torch.tensor([2.0, 1.0, 0.1])
lp = torch.log_softmax(logits, dim=0)
print([round(v, 6) for v in lp.tolist()], round(float(torch.nn.NLLLoss()(lp, torch.tensor([0]))), 6))
```

- **A.** [-0.41703, -1.41703, -2.31703] 0.41703
- **B.** ([0.665241, 0.244728, 0.090031], 0.41703)
- **C.** ([-0.41703, -1.41703, -2.31703], 1.41703)
- **D.** ([2.0, 1.0, 0.1], 0.41703)

## 口述答案

答案是 **A. [-0.41703, -1.41703, -2.31703] 0.41703**，实际输出 `[-0.41703, -1.41703, -2.31703] 0.41703`。

log_softmax 输出对数概率（都是负数），NLLLoss 取负对数似然作损失，与 CrossEntropyLoss 完全等价。

## 讲深一层

`log_softmax = logits − logsumexp(logits)`，输出全负；`NLLLoss` 取 target 位置的负值求平均，与 `CrossEntropyLoss` 完全等价。拆开写便于加权、ignore_index 与蒸馏。注意 NLLLoss 只认 log 概率，给概率会得负 loss。

## 高频追问

1. **与 `CrossEntropyLoss` 数值关系？** —— 完全相等，前者就是后者的两步展开
2. **为什么要拆开写？** —— 需要类别加权、忽略某类、或对 log 概率做额外运算时更灵活
3. **`NLLLoss` 能给概率吗？** —— 不能，它直接取负号，给概率会得负数 loss，属于静默错误

## 易错点

- 把 `log_softmax` 当 softmax——输出应为负数，写成正的概率值（选项 B）
- 对 log 概率再取一次 log——数值彻底错，还可能出 nan
- 忘记 NLLLoss 内部取负——会以为 loss 是 −0.41703

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
