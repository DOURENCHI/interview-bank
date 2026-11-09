---
id: Q-1775
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 81 题）
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
