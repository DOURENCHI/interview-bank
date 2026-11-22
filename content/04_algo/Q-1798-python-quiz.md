---
id: Q-1798
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 105 题）
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
m(torch.ones(1, 2)).sum().backward()
g = float(m.weight.grad.sum())
m.zero_grad()
print(round(g, 6), m.weight.grad)
```

- **A.** 2.0 None
- **B.** (2.0, 0.0)
- **C.** (None, None)
- **D.** (1.0, 1.0)

## 口述答案

答案是 **A. 2.0 None**，实际输出 `2.0 None`。

zero_grad 之后梯度变成 None（不是 0），因为 PyTorch 用 None 表示「没有梯度」以节省内存；这是判断有没有清零成功的标志。

## 讲深一层

PyTorch 2.x 的 `zero_grad()` 默认 `set_to_none=True`，把 grad 置 None 而非填 0，省一次显存写入，也让"没算过"与"梯度恰为 0"可区分。要得到 0 张量需显式传 `set_to_none=False`。`g` 是 backward 后用 `float()` 提前拷出的数值，所以打印仍是 2.0。

## 高频追问

1. **为什么 None 比 0 好？** —— 省写显存，backward 时按需新分配，语义也更准确
2. **旧版本是什么行为？** —— 1.x 默认填 0 张量，所以老代码里 grad 不会是 None
3. **对优化器有影响吗？** —— 无，None 参数在 `step()` 里被跳过

## 易错点

- 答 0.0——默认 `set_to_none=True`，实际是 None（选项 B）
- 用 `if p.grad:` 判断有没有梯度——零张量也为假，语义混淆
- 以为 `zero_grad()` 会删掉参数——它只清梯度，参数原样保留

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
