---
id: Q-1778
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 85 题）
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
p = torch.tensor([0.8, 0.2])
y = torch.tensor([1.0, 0.0])
print(round(float(torch.nn.BCELoss()(p, y)), 6))
```

- **A.** 0.223144
- **B.** 0.5
- **C.** 0.8
- **D.** 0.0

## 口述答案

答案是 **A. 0.223144**，实际输出 `0.223144`。

BCELoss = -[y·log(p) + (1-y)·log(1-p)]，代入得 -(1×log0.8 + log0.8) = -2×log0.8 = 0.223144。

## 讲深一层

BCE 为 `−[y·log p+(1−y)·log(1−p)]`，默认取 mean。p=`[0.8,0.2]`、y=`[1,0]` 时两项都是 `−log0.8`，平均仍是 0.223144。若标签反过来 `[0,1]`，得 `−log0.2 = 1.609`。

## 高频追问

1. **`reduction="sum"` 是多少？** —— 0.446287，等于 mean 乘 2；训练时 sum 会让梯度随批大小放大
2. **p 里出现 0 或 1 会怎样？** —— `log(0)` 得 inf，梯度变 nan，所以要先 clamp 或改用 `BCEWithLogitsLoss`
3. **为什么平均后仍等于 `−log0.8`？** —— 两项数值相同，均值等于其中任一项

## 易错点

- 忘了 mean 要除以 2——得 0.446287，正好是 sum 的结果
- 把 log 当 log10——得 0.0969 量级，与所有选项都对不上
- 直接把 logits 喂给 BCELoss——不报错但语义错，值也是错的（应先 sigmoid）

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
