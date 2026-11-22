---
id: Q-1785
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 92 题）
module: 04_algo
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
p = torch.nn.MaxPool2d(2)
x = torch.tensor([[[[1.0, 2.0], [3.0, 4.0]]]])
print(tuple(p(x).shape), p(x).reshape(-1).tolist())
```

- **A.** (1, 1, 1, 1) [4.0]
- **B.** ((1, 1, 2, 2), [1.0, 2.0, 3.0, 4.0])
- **C.** ((1, 1, 1, 1), [1.0])
- **D.** ((1, 1, 2, 2), [4.0])

## 口述答案

答案是 **A. (1, 1, 1, 1) [4.0]**，实际输出 `(1, 1, 1, 1) [4.0]`。

2×2 池化把 2×2 缩成 1×1，取窗口最大值 4.0。池化没有可学参数。

## 讲深一层

`MaxPool2d(2)` 的 stride 默认等于 kernel_size，2×2 输入正好一窗，输出 `(1,1,1,1)` 取最大值 4.0。池化没有可学参数，反向只把梯度传给窗口内最大值那个位置，其余为 0。若输入奇数边长如 3×3，`floor((3−2)/2+1)=1`，最后一行一列会被直接丢弃。

## 高频追问

1. **换成 `AvgPool2d(2)` 是多少？** —— 2.5，四个数平均；这说明池化类型改变的是聚合方式而非形状
2. **反向传播怎么走？** —— 梯度只回传到 argmax 位置，其余位置梯度为 0
3. **输入 3×3 会怎样？** —— 输出 1×1，边界一行一列被丢弃，不补零

## 易错点

- 认为池化有参数——它没有权重，只有 kernel/stride/padding 超参
- 形状写成 `(1,1,2,2)`——池化是降采样，尺寸只会变小
- 以为会补零保持尺寸——池化不 padding，除非显式传 `padding`

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
