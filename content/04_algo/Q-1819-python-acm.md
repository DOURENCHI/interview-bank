---
id: Q-1819
title: 优化器、超参与发散排查 的 ACM 输入输出怎么写？
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
import torch.nn as nn

torch.manual_seed(1)
m = torch.nn.Linear(2, 1)
sgd = torch.optim.SGD(m.parameters(), lr=0.1, momentum=0.9)
print("SGD 超参 lr =", sgd.param_groups[0]["lr"], "momentum =", sgd.param_groups[0]["momentum"])

adam = torch.optim.Adam(m.parameters(), lr=0.01)
m(torch.randn(4, 2)).sum().backward()
adam.step()
print("Adam 状态键", tuple(adam.state[m.weight].keys()))

m(torch.ones(1, 2)).sum().backward()
g = float(m.weight.grad.sum())
m.zero_grad()
print("清零前梯度", round(g, 6), "| 清零后", m.weight.grad)

torch.manual_seed(9)
big = torch.nn.Linear(1, 1)
opt = torch.optim.SGD(big.parameters(), lr=1e4)
xs = torch.Tensor([[1.0], [2.0], [3.0]])
ys = torch.Tensor([[2.0], [4.0], [6.0]])
crit = nn.MSELoss(reduction="sum")
first = None
for _ in range(5):
    loss = crit(big(xs), ys)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if first is None:
        first = loss.item()
print(f"lr=1e4 首轮 loss {first:.4f} -> 末轮 {loss.item():.4f}（发散）")
```

输出样例：

```
SGD 超参 lr = 0.1 momentum = 0.9
Adam 状态键 ('step', 'exp_avg', 'exp_avg_sq')
清零前梯度 0.769743 | 清零后 None
lr=1e4 首轮 loss 48.4040 -> 末轮 inf（发散）
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
