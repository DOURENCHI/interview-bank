---
id: Q-1771
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 78 题）
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
from torch.utils.data import Dataset, DataLoader
class DS(Dataset):
    def __init__(self, n):
        self.x = torch.arange(n, dtype=torch.float32).reshape(-1, 1)
    def __len__(self):
        return len(self.x)
    def __getitem__(self, i):
        return self.x[i]
print(len(DataLoader(DS(10), batch_size=4, shuffle=False, drop_last=True)))
```

- **A.** 2
- **B.** 3
- **C.** 4
- **D.** 10

## 口述答案

答案是 **A. 2**，实际输出 `2`。

drop_last=True 把不满一批的尾部丢掉，10 个样本只出 2 个满批（8 个样本），最后 2 个被丢弃。

## 讲深一层

`drop_last=True` 丢弃不足一批的尾部，`10//4=2`，出 2 个满批共 8 个样本，剩 2 个被丢。这个开关主要防 BN 在单样本批上方差为 0（或直接报错），以及保证各批形状一致好做静态图编译。代价是每 epoch 有样本不参与训练，shuffle 下相当于随机丢。

## 高频追问

1. **被丢掉的数据怎么办？** —— 每个 epoch 因 shuffle 顺序不同而不同，等价于随机丢弃，量小可接受
2. **什么时候必须开？** —— 末批只剩 1 个样本且网络里有 BatchNorm 时，必须开，否则 BN 报错
3. **N=8 时是多少？** —— 2 批，正好整除，`drop_last` 不丢任何样本

## 易错点

- 算成 3——那是 `drop_last=False` 的结果
- 以为 `drop_last` 会把尾批补齐——它是丢弃，不是填充
- N=8 时仍答 1——整除时两种设置结果相同，都是 2

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 06 Dataset 与 DataLoader
