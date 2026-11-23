---
id: Q-1782
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 89 题）
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
logits = torch.tensor([0.5, -0.5, 1.5])
y = torch.tensor([1.0, 0.0, 1.0])
a = float(torch.nn.BCELoss()(torch.sigmoid(logits), y))
b = float(torch.nn.BCEWithLogitsLoss()(logits, y))
print(round(a, 6), round(b, 6))
```

- **A.** 0.383189 0.383189
- **B.** (0.383189, 0.693147)
- **C.** (0.5, 0.5)
- **D.** (0.0, 0.0)

## 口述答案

答案是 **A. 0.383189 0.383189**，实际输出 `0.383189 0.383189`。

两种写法数值完全一致（0.383189），这是 BCEWithLogitsLoss 存在的意义：省一次 sigmoid，且数值更稳。

## 讲深一层

logits `[0.5,−0.5,1.5]` 经 sigmoid 得 `[0.6225,0.3775,0.8176]`，BCE 逐元素算完平均，三项都等于 `−log0.6225`，得 0.383189。融合版是对数域同式，结果相同，只差稳定性与计算量。

## 高频追问

1. **两者什么时候会不同？** —— logits 极大时手动版 sigmoid 饱和，`log(0)` 得 inf；融合版仍有限
2. **哪个更快？** —— 融合版少一次 sigmoid 和一次 log，反向也更简洁
3. **为什么三项 loss 相同？** —— 每个样本的预测概率与标签"匹配度"恰好一致，都是 0.6225

## 易错点

- 算成 0.693147——那是全预测 0.5 时的 BCE，说明漏算了 sigmoid
- 把 mean 当 sum——得 1.149567，是 3 倍关系
- target 用 int——报 dtype 错，BCE 系列要求 float

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
