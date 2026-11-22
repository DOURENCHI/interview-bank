---
id: Q-1790
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 97 题）
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
rnn = torch.nn.RNN(4, 5, batch_first=True)
out, h = rnn(torch.randn(2, 7, 4))
print(tuple(out.shape), tuple(h.shape))
```

- **A.** (2, 7, 5) (1, 2, 5)
- **B.** ((2, 4, 7), (2, 5, 1))
- **C.** ((2, 7, 5), (2, 5))
- **D.** ((1, 2, 5), (2, 7, 5))

## 口述答案

答案是 **A. (2, 7, 5) (1, 2, 5)**，实际输出 `(2, 7, 5) (1, 2, 5)`。

batch_first=True 时输入 (批, 序列长, 特征)，输出 (2,7,5)；h 是最后隐状态 (层数1, 批2, 隐层5)。

## 讲深一层

输入 `(B,T,in)`、输出 `(B,T,hidden)`、`h_n` 是 `(num_layers,B,hidden)`。`batch_first` 只改输入输出的前两维布局，不改 `h_n`——h 永远层数在前。多层时 out 只给最后一层所有时刻，中间层结果不外露，所以取 out 直接接分类头即可。

## 高频追问

1. **`batch_first=False` 时形状？** —— 输入 `(7,2,4)`、输出 `(7,2,5)`，`h` 仍是 `(1,2,5)`
2. **`h` 与 `out` 什么关系？** —— 单层时 `h[0]` 等于 `out[:, -1, :]`，就是最后时刻的隐状态
3. **`num_layers=2` 时 h 形状？** —— `(2,2,5)`，每层一个终态

## 易错点

- 把 h 写成 `(2,5)`——那是 batch_first 思维，h 恒为三维
- 输出写成 `(2,4,7)`——把特征维与时间维调换了
- 以为 h 含所有时刻——它只存最后一步，全序列在 out 里

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
