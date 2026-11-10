---
id: Q-1815
title: 自定义 Dataset 与 DataLoader 分批 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: indexed
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 Python 程序对应的读入与输出写法是什么？

```python
import torch
from torch.utils.data import Dataset, DataLoader


class ToyDataset(Dataset):
    def __init__(self, n):
        self.x = torch.arange(n, dtype=torch.float32).reshape(-1, 1)
        self.y = self.x * 2

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return self.x[i], self.y[i]


ds = ToyDataset(10)
dl = DataLoader(ds, batch_size=4, shuffle=False)
print("样本数", len(ds), "批数", len(dl))
for xb, yb in dl:
    print("x", xb.reshape(-1).tolist(), "y", yb.reshape(-1).tolist())

print("drop_last=True 后批数", len(DataLoader(ds, batch_size=4, drop_last=True)))

torch.manual_seed(0)
seen = []
for xb, _ in DataLoader(ds, batch_size=2, shuffle=True):
    seen.extend(xb.reshape(-1).tolist())
print("shuffle 后顺序", seen)
```

输出样例：

```
样本数 10 批数 3
x [0.0, 1.0, 2.0, 3.0] y [0.0, 2.0, 4.0, 6.0]
x [4.0, 5.0, 6.0, 7.0] y [8.0, 10.0, 12.0, 14.0]
x [8.0, 9.0] y [16.0, 18.0]
drop_last=True 后批数 2
shuffle 后顺序 [6.0, 7.0, 1.0, 4.0, 2.0, 0.0, 9.0, 8.0, 3.0, 5.0]
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 06 Dataset 与 DataLoader
