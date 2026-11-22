---
id: Q-1779
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 86 题）
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
logits = torch.tensor([2.0, -2.0])
y = torch.tensor([1.0, 0.0])
a = float(torch.nn.BCELoss()(torch.sigmoid(logits), y))
b = float(torch.nn.BCEWithLogitsLoss()(logits, y))
print([round(v, 6) for v in torch.sigmoid(logits).tolist()], round(a, 6), round(b, 6))
```

- **A.** [0.880797, 0.119203] 0.126928 0.126928
- **B.** ([0.880797, 0.119203], 0.126928, 0.693147)
- **C.** ([0.119203, 0.880797], 0.126928, 0.126928)
- **D.** ([0.880797, 0.119203], 0.0, 0.693147)

## 口述答案

答案是 **A. [0.880797, 0.119203] 0.126928 0.126928**，实际输出 `[0.880797, 0.119203] 0.126928 0.126928`。

BCEWithLogitsLoss 把 sigmoid 和 BCELoss 融合成一个数值稳定的操作，结果与手动两步完全相同（0.126928）。数值大时别先 sigmoid。

## 讲深一层

`BCEWithLogitsLoss` 用 log-sum-exp 恒等式 `max(x,0) − x·y + log(1+e^{−|x|})` 计算，数学上等于 sigmoid + BCE，但不会显式算出 0 或 1 再取 log，因此不会溢出。这里两种写法都得 0.126928，是数值稳定的等价实现；logits 到 ±20 以上时手动版就会炸。

## 高频追问

1. **为什么数值更稳？** —— 不显式算 sigmoid，避免 `log(0)` 与 `exp` 上溢，全程在同一对数域内合并
2. **`logits=[20,−20]` 时手动版会怎样？** —— sigmoid 饱和到 1 和 0，`log(0)` 得 inf；融合版仍是有限值
3. **多标签怎么用？** —— 直接对 C 维 logits 用，target 同形状且为 float，逐元素独立算 BCE

## 易错点

- 认为融合版结果会不同——数学等价，只差浮点误差
- 对已 sigmoid 的输出再用 `BCEWithLogitsLoss`——等于做了两次 sigmoid，值偏小且梯度错
- target 传 int——报 dtype 不匹配，BCE 要求 float

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
