---
id: Q-1771
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 77 题）
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 06 Dataset 与 DataLoader
