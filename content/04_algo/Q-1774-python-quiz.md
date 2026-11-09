---
id: Q-1774
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 80 题）
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
def order():
    out = []
    for xb in DataLoader(DS(5), batch_size=2, shuffle=True):
        out.extend(xb.reshape(-1).tolist())
    return out
torch.manual_seed(0)
a = order()
torch.manual_seed(0)
b = order()
print(a, b, a == b, len(DataLoader(DS(5), batch_size=2, shuffle=True)))
```

- **A.** [1.0, 4.0, 2.0, 3.0, 0.0] [1.0, 4.0, 2.0, 3.0, 0.0] True 3
- **B.** ([1.0, 4.0, 2.0, 3.0, 0.0], [0.0, 1.0, 2.0, 3.0, 4.0], False, 3)
- **C.** ([1.0, 4.0, 2.0, 3.0, 0.0], [1.0, 4.0, 2.0, 3.0, 0.0], True, 2)
- **D.** ([0.0, 1.0, 2.0, 3.0, 4.0], [0.0, 1.0, 2.0, 3.0, 4.0], True, 5)

## 口述答案

答案是 **A. [1.0, 4.0, 2.0, 3.0, 0.0] [1.0, 4.0, 2.0, 3.0, 0.0] True 3**，实际输出 `[1.0, 4.0, 2.0, 3.0, 0.0] [1.0, 4.0, 2.0, 3.0, 0.0] True 3`。

固定 seed 后两次遍历顺序完全一致（True），这是实验可复现的前提；5 个样本 batch_size=2 出 3 批（最后一批只有 1 个）。

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
