---
id: Q-1792
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 99 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```python
import torch
lstm = torch.nn.LSTM(4, 5, batch_first=True)
print(tuple(lstm(torch.randn(2, 7, 4))[0].shape))
```

- **A.** (2, 7, 5)
- **B.** ((2, 4, 7),)
- **C.** ((1, 2, 5),)
- **D.** ((2, 7, 4),)

## 口述答案

答案是 **A. (2, 7, 5)**，实际输出 `(2, 7, 5)`。

LSTM 与 RNN 输出形状相同 (批, 序列长, 隐层)，区别在于内部多了门控与细胞状态。

## 讲深一层

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
