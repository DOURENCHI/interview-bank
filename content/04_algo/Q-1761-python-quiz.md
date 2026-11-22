---
id: Q-1761
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 68 题）
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
m = torch.nn.Linear(3, 2)
print(tuple(m.weight.shape), tuple(m.bias.shape), m.weight.shape[0] * m.weight.shape[1] + 2)
```

- **A.** (2, 3) (2,) 8
- **B.** ((3, 2), (3,), 8)
- **C.** ((2, 3), (2,), 6)
- **D.** ((2, 3), (2,), 2)

## 口述答案

答案是 **A. (2, 3) (2,) 8**，实际输出 `(2, 3) (2,) 8`。

Linear(3,2) 是「3 个输入 → 2 个输出」，权重形状 (out, in) = (2,3)、偏置 2 个，共 2×3+2 = 8 个参数。

## 讲深一层

`nn.Linear` 的 weight 是 `(out, in)`，与数学写法 `W(in, out)` 互为转置，前向为 `y = x·Wᵀ + b`。这样与 `Conv2d` 的 out-first 约定统一。参数量 = `out×in + out`，`Linear(3,2)` 即 6+2=8。

## 高频追问

1. **为什么 weight 不是 `(3, 2)`？** —— 为了直接 `x @ W.t()`，且与卷积 out-first 的约定统一，`F.linear` 内部就是这么算的
2. **输入 `(5, 3)` 时输出形状？** —— `(5, 2)`，只有最后一维被 in_features 吃掉，前面几维都是 batch
3. **这个层的 FLOPs 怎么估？** —— 约 `2 × batch × in × out`（乘、加各一次），bias 另加

## 易错点

- 把 weight 当 `(in, out)`——参数量仍算 6，但 bias 只加 3 个，总数错成 9
- 忘记 bias——得 2×3=6，正好是选项 C 的坑
- 把 `shape[0]*shape[1]+2` 里的 2 当输入维——那是 bias 个数，等于 out_features

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
