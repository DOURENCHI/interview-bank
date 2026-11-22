---
id: Q-1802
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 109 题）
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
torch.manual_seed(10)
d = torch.nn.Dropout(0.5)
d.train()
out = d(torch.ones(1000))
print(round(float((out == 0).float().mean()), 4))
```

- **A.** 0.499
- **B.** 0.5, 
- **C.** 0.999
- **D.** 0.0

## 口述答案

答案是 **A. 0.499**，实际输出 `0.499`。

Dropout 在 train 模式按 p=0.5 随机置零，实测 1000 个里有 499 个是 0，接近 0.5。

## 讲深一层

每个元素独立伯努利 p=0.5，1000 次的零比例标准差是 `√(0.25/1000) ≈ 0.0158`，所以 0.499 完全正常，不是精确 0.5。固定 seed=10 让这个抽样可复现。保留下来的元素被放大到 2.0，这是 inverted dropout 的期望补偿。

## 高频追问

1. **为什么不是精确 0.5？** —— 有限样本的抽样波动，n 越大越贴近 p
2. **非零位置的数值是多少？** —— 2.0，即 `1/(1−0.5)` 的放大
3. **p=0.2 时零比例？** —— 约 0.2，同样带 ±0.013 量级的波动

## 易错点

- 答精确 0.5——那是期望值，实测是抽样结果（选项 B 的干扰）
- 认为剩下仍是 1.0——被放大成 2.0，否则输出期望会偏小一半
- 在 eval 模式下统计——得 0.0，因为 eval 直接关闭 dropout

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
