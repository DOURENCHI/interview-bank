---
id: Q-1774
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 81 题）
module: 04_algo
sub: 并发与性能
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
from torch.utils.data import Dataset, DataLoader
class DS(Dataset):
    def __init__(self):
        self.x = torch.tensor([1.0, 2.0, 3.0])
    def __len__(self):
        return 3
    def __getitem__(self, i):
        return self.x[i] * 10, self.x[i]
print([xb.tolist() for xb, _ in DataLoader(DS(), batch_size=3)])
```

- **A.** [[10.0, 20.0, 30.0]]
- **B.** [[1.0, 2.0, 3.0]]
- **C.** [[10.0], [20.0], [30.0]]
- **D.** [[30.0, 20.0, 10.0]]

## 口述答案

答案是 **A. [[10.0, 20.0, 30.0]]**，实际输出 `[[10.0, 20.0, 30.0]]`。

__getitem__ 返回 (输入, 标签) 二元组时 DataLoader 才能默认成对堆叠；返回单值时 collate 会把单个元素当序列处理，形状会变成 (3,) 而不是 (1,3)。

## 讲深一层

默认 `collate_fn` 遇到 tuple 会按位置转置：先取所有样本的第 0 个元素 stack 成 `(3,)`，再取第 1 个。所以解包 `for xb, _ in ...` 拿到的 xb 是 `[10,20,30]`。若 `__getitem__` 只返回单值，堆叠后是 `(3,)` 少一维；各样本字段数不一致会直接报错。

## 高频追问

1. **返回单值会怎样？** —— 得到 `(3,)` 而不是 `(1,3)`，后面接 Linear 时维度对不上
2. **返回 dict 呢？** —— 按 key 分别堆叠，得到 `{"x": tensor(...), "y": tensor(...)}`
3. **为什么只有一批？** —— `batch_size=3` 等于样本总数 3，正好一批

## 易错点

- 以为输出是 `[[10],[20],[30]]`——那是按样本分组，实际是按字段分组
- 以为 tuple 需要自定义 collate——默认实现已按位置处理，不用写
- 把 `_` 当成丢弃后形状变化——解包不影响堆叠结果

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 06 Dataset 与 DataLoader
