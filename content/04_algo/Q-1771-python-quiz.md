---
id: Q-1771
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 78 题）
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
