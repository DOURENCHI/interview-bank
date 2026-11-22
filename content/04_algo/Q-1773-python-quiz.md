---
id: Q-1773
title: 这段 Python 代码输出什么？（06 Dataset 与 DataLoader · 第 80 题）
module: 04_algo
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

没给 `generator` 时 `RandomSampler` 用全局 RNG，`manual_seed(0)` 能复现同一排列 `[1,4,2,3,0]`；显式传 generator 就与全局隔离，seed 失效。批数 `ceil(5/2)=3`，末批 1 个样本。多 worker 还要 `worker_init_fn`。

## 高频追问

1. **为什么两次结果完全一样？** —— 全局 RNG 状态被 `manual_seed(0)` 重置，采样序列从头重放
2. **多进程 dataloader 还能复现吗？** —— 要设 `worker_init_fn` 和 `base_seed`，否则每个 worker 的种子不同
3. **`len(...)` 为什么是 3？** —— 5 个样本、批大小 2，`ceil(5/2)=3`，末批只有 1 个

## 易错点

- 认为 shuffle 不可复现——固定 seed 后可复现，这是实验可复现的前提
- 传了 `generator` 还指望 `manual_seed` 生效——独立随机源，两者互不影响
- 把批数算成 2——`5//2=2` 漏掉尾批

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 06 Dataset 与 DataLoader
