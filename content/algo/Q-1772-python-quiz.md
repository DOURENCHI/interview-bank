---
id: Q-1772
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 79 题）
module: algo
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
    def __init__(self, n):
        self.x = torch.arange(n, dtype=torch.float32).reshape(-1, 1)
    def __len__(self):
        return len(self.x)
    def __getitem__(self, i):
        return self.x[i]
print([tuple(xb.shape) for xb in DataLoader(DS(10), batch_size=4, shuffle=False)])
```

- **A.** [(4, 1), (4, 1), (2, 1)]
- **B.** [(4, 1), (4, 1), (4, 1)]
- **C.** [(4, 1), (2, 1)]
- **D.** [(10, 1)]

## 口述答案

答案是 **A. [(4, 1), (4, 1), (2, 1)]**，实际输出 `[(4, 1), (4, 1), (2, 1)]`。

默认 drop_last=False，最后一批是 2 个样本，形状 (2,1)。训练时各批样本数不同是允许的。

## 讲深一层

列表推导逐批取 `shape`，默认 `drop_last=False` 所以是 `[(4,1),(4,1),(2,1)]`。DataLoader 是可迭代对象，每次 `iter()` 重建迭代器，所以能重复遍历；但 `it = iter(dl)` 得到的迭代器本身只能走一次。批形状的第一维是实际样本数，因此末批会变。

## 高频追问

1. **同一个 dl 能遍历两次吗？** —— 能，`for` 每次调 `__iter__` 新建迭代器；但缓存的 `iter(dl)` 走完就空
2. **为什么是 `(4,1)` 不是 `(4,)`？** —— 单样本是 `(1,)`，堆叠后多一个 batch 维
3. **想让各批形状统一怎么办？** —— `drop_last=True`，或自定义 `collate_fn` 做 padding

## 易错点

- 答三个 `(4,1)`——忽略末批只有 2 个样本
- 认为迭代器耗尽后 dl 也废了——dl 本身可反复 `iter`，只有迭代器一次性
- 把形状写成 `(4,)`——丢掉特征维，与 `reshape(-1,1)` 矛盾

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 06 Dataset 与 DataLoader
