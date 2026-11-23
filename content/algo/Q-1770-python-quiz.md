---
id: Q-1770
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 77 题）
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
for xb in DataLoader(DS(10), batch_size=4, shuffle=False):
    print(tuple(xb.shape), xb.reshape(-1).tolist())
```

- **A.** (4, 1) [0.0, 1.0, 2.0, 3.0]
(4, 1) [4.0, 5.0, 6.0, 7.0]
(2, 1) [8.0, 9.0]
- **B.** ((4, 1), [0.0, 1.0, 2.0, 3.0]) ((4, 1), [4.0, 5.0, 6.0, 7.0]) ((2, 1), [8.0, 9.0, 0.0, 0.0])
- **C.** ((10, 1), [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
- **D.** ((4, 1), [0.0, 1.0, 2.0, 3.0]) ((4, 1), [4.0, 5.0, 6.0, 7.0]) ((2, 1), [8.0, 9.0]) 

## 口述答案

答案是 **A. (4, 1) [0.0, 1.0, 2.0, 3.0]
(4, 1) [4.0, 5.0, 6.0, 7.0]
(2, 1) [8.0, 9.0]**，实际输出 `(4, 1) [0.0, 1.0, 2.0, 3.0]
(4, 1) [4.0, 5.0, 6.0, 7.0]
(2, 1) [8.0, 9.0]`。

DataLoader 默认把每个样本的 tensor 堆叠成批，形状是 (batch, 特征数)；最后一批不满 4 但不会被补零。

## 讲深一层

默认 collate 把样本沿新维 stack，`(1,)` 堆成 `(B,1)`，末批 B=2 不补齐。`shuffle=False` 时顺序就是索引 0..9。若 `__getitem__` 返回 dict，collate 按 key 分别堆叠成 dict of tensors。

## 高频追问

1. **最后一批会补零吗？** —— 不会，`(2,1)` 就是 2 个样本，补零要自己写 collate_fn
2. **想要固定形状怎么办？** —— `drop_last=True` 丢掉尾批，或自定义 sampler/collate 补齐
3. **batch 内样本顺序由谁决定？** —— sampler，`shuffle=False` 时是 `SequentialSampler`，严格按索引

## 易错点

- 认为末批补零成 `(4,1)`——即选项 B，实际只有 `(2,1)`
- 把 `(2,1)` 写成 `(2,)`——样本本身是 `(1,)`，堆叠后必是二维
- 把 `len(dl)=3` 与批形状混淆——批数不等于批大小

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 06 Dataset 与 DataLoader
