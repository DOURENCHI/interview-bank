---
id: Q-1825
title: 端到端：训练 + 评估 + 存权重一条龙 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: draft
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
import os
import tempfile

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset


class Toy(Dataset):
    def __init__(self, n):
        self.x = torch.arange(n, dtype=torch.float32).reshape(-1, 1) / n
        self.y = self.x * 2

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return self.x[i], self.y[i]


torch.manual_seed(7)
model = nn.Linear(1, 1)
opt = torch.optim.Adam(model.parameters(), lr=0.05)
crit = nn.MSELoss()
dl = DataLoader(Toy(64), batch_size=16, shuffle=True)

model.train()
for epoch in range(30):
    total = 0.0
    for xb, yb in dl:
        opt.zero_grad()
        loss = crit(model(xb), yb)
        loss.backward()
        opt.step()
        total += loss.item()
    if epoch % 10 == 0:
        print(f"Epoch {epoch}: 平均损失 {total / len(dl):.5f}")

model.eval()
with torch.inference_mode():
    preds = model(torch.tensor([[0.5]]))
print("eval 预测 x=0.5 ->", round(float(preds), 4), "（真实值 1.0）")

path = os.path.join(tempfile.gettempdir(), "_py_lab_e2e.pt")
torch.save(model.state_dict(), path)
print("权重已保存，字节数", os.path.getsize(path))
os.remove(path)
```

输出样例：

```
Epoch 0: 平均损失 2.37330
Epoch 10: 平均损失 0.08115
Epoch 20: 平均损失 0.02413
eval 预测 x=0.5 -> 1.0126 （真实值 1.0）
权重已保存，字节数 1925
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

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
