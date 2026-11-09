---
id: Q-1758
title: 这段 Python 代码输出什么？（04 线性模型与梯度下降 · 第 64 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
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
torch.manual_seed(1)
x = torch.Tensor([[1.0], [2.0], [3.0]])
y = torch.Tensor([[2.0], [4.0], [6.0]])
model = torch.nn.Linear(1, 1)
crit = torch.nn.MSELoss(reduction="sum")
opt = torch.optim.SGD(model.parameters(), lr=0.01)
for _ in range(100):
    pred = model(x)
    loss = crit(pred, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
print(round(model.weight.item(), 4), round(model.bias.item(), 4), round(model(torch.Tensor([[4.0]])).item(), 4))
```

- **A.** 1.9622 0.086 7.9346
- **B.** (2.0, 0.0, 8.0)
- **C.** (1.9622, 0.086, 8.0)
- **D.** (2.0, 0.0, 7.9346)

## 口述答案

答案是 **A. 1.9622 0.086 7.9346**，实际输出 `1.9622 0.086 7.9346`。

真实关系是 y=2x，但 100 轮 + lr=0.01 还没收敛到位，所以权重是 1.9622 而不是精确的 2.0。实测输出必须认准这个「未完全收敛」的现实。

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

`教学文档/Python实验台/Python考点实验台.html` · 04 线性模型与梯度下降
