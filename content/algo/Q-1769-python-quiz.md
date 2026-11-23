---
id: Q-1769
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 76 题）
module: algo
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
from torch.utils.data import Dataset, DataLoader
class DS(Dataset):
    def __init__(self, n):
        self.x = torch.arange(n, dtype=torch.float32).reshape(-1, 1)
    def __len__(self):
        return len(self.x)
    def __getitem__(self, i):
        return self.x[i]
ds = DS(10)
dl = DataLoader(ds, batch_size=4, shuffle=False)
print(len(ds), len(dl))
```

- **A.** 10 3
- **B.** (10, 4)
- **C.** (10, 2)
- **D.** (4, 3)

## 口述答案

答案是 **A. 10 3**，实际输出 `10 3`。

数据集有 10 个样本，batch_size=4 整除 10？不能整除，最后一批是 2 个，所以 ceil(10/4) = 3 批。

## 讲深一层

`len(ds)` 来自 `__len__` 返回 10；`len(dl)` 是 `ceil(N/batch_size)`，`drop_last=True` 时变 floor。DataLoader 的长度依赖 sampler，`IterableDataset` 无长度会抛 TypeError。余数必须单独成批，不能整除取整了事。

## 高频追问

1. **`drop_last=True` 时 `len(dl)` 是多少？** —— 2，10//4=2，尾部 2 个样本被丢弃
2. **`batch_size` 大于 N 呢？** —— 1 批，形状 `(10, 1)`，不会报错也不会补齐
3. **`len(ds)` 是谁提供的？** —— 必须自己实现 `__len__`，否则 `len(ds)` 直接 TypeError

## 易错点

- 用整除算成 2——忘了余数要单独成一批，正确是 3
- 以为最后一批会补零到 4——默认不补，形状是 `(2,1)`
- 忘了写 `__len__`——`len(ds)` 报 `TypeError: object of type 'DS' has no len()`

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 06 Dataset 与 DataLoader
