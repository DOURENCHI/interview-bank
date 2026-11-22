---
id: Q-1796
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 103 题）
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
emb = torch.nn.Embedding(100, 16)
print(tuple(emb(torch.tensor([1, 2, 3])).shape), emb.weight.shape)
```

- **A.** (3, 16) torch.Size([100, 16])
- **B.** ((100, 16), torch.Size([100, 16]))
- **C.** ((3, 100), torch.Size([100, 16]))
- **D.** ((16, 3), torch.Size([100, 16]))

## 口述答案

答案是 **A. (3, 16) torch.Size([100, 16])**，实际输出 `(3, 16) torch.Size([100, 16])`。

Embedding 把 3 个下标各查成 16 维向量，输出 (3,16)；权重表是 (词表100, 维度16)。

## 讲深一层

Embedding 是一张 `(num_embeddings, dim)` 的查找表，输入必须是 long 索引，输出形状 = 输入形状 + `(dim,)`，所以 3 个下标变 `(3,16)`。它等价于 one-hot 乘权重矩阵，但省掉了 one-hot 的存储。`padding_idx` 指定某行恒为零且不更新梯度。

## 高频追问

1. **输入 float 会怎样？** —— `RuntimeError: Expected tensor for argument 'indices' to have scalar type Long`
2. **索引越界呢？** —— `IndexError: index out of range in self`，词表只有 0..99
3. **`padding_idx` 有什么用？** —— 该行输出固定为零向量且梯度不更新，用于变长序列对齐

## 易错点

- 答 `(100,16)`——把权重形状当输出，选项 B 的坑
- 用 float 索引——直接报错，必须先 `.long()`
- 以为 embedding 不可训练——weight 是 Parameter，会随训练更新

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
