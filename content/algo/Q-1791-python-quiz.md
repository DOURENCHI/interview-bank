---
id: Q-1791
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 98 题）
module: algo
sub: 容器与切片
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
cell = torch.nn.RNNCell(4, 5)
h = torch.zeros(2, 5)
shapes = []
for _ in range(3):
    h = cell(torch.randn(2, 4), h)
    shapes.append(tuple(h.shape))
print(shapes)
```

- **A.** [(2, 5), (2, 5), (2, 5)]
- **B.** [(2, 4), (2, 4), (2, 4)]
- **C.** [(2, 6), (2, 6), (2, 6)]
- **D.** [(5, 2), (5, 2), (5, 2)]

## 口述答案

答案是 **A. [(2, 5), (2, 5), (2, 5)]**，实际输出 `[(2, 5), (2, 5), (2, 5)]`。

RNNCell 一次处理一个时间步，输入 (批, 输入特征4)、隐状态 (批, 隐层5)，输出隐状态形状恒为 (2,5)。

## 讲深一层

RNNCell 只跑一个时间步：输入 `(B,in)`、隐状态 `(B,hidden)`，返回新的 `(B,hidden)`，没有 out。处理序列要自己写循环并逐步传递 h。参数与单层 RNN 相同：`W_ih(5,4)`、`W_hh(5,5)` 加两个 bias，共 `20+25+5+5 = 55`。

## 高频追问

1. **与 `RNN` 的区别？** —— 没有时间维，不会自动展开，需手动循环
2. **参数量多少？** —— 55，`5×4 + 5×5 + 5 + 5`
3. **想拿整段输出？** —— 循环里收集每步 h 再 `torch.stack` 成 `(T,B,H)`

## 易错点

- 期望输出 `(2,3,5)`——把 Cell 当 RNN，凭空多一个时间维
- 初始 h 写成 `(5,2)`——形状反了，直接报维度错
- 以为 Cell 自动展开序列——它只处理一步，3 次循环才走 3 步

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
