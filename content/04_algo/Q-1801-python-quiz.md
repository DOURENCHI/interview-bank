---
id: Q-1801
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 107 题）
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
torch.manual_seed(9)
m = torch.nn.Linear(1, 1)
opt = torch.optim.SGD(m.parameters(), lr=1e4)
xs = torch.Tensor([[1.0], [2.0], [3.0]])
ys = torch.Tensor([[2.0], [4.0], [6.0]])
crit = torch.nn.MSELoss(reduction="sum")
first = None
for _ in range(5):
    loss = crit(m(xs), ys)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if first is None:
        first = loss.item()
print(round(first, 4), round(loss.item(), 4), loss.item() > first)
```

- **A.** 48.404 inf True
- **B.** (48.404, 0.0, False)
- **C.** (0.0, 48.404, True)
- **D.** (48.404, 48.404, False)

## 口述答案

答案是 **A. 48.404 inf True**，实际输出 `48.404 inf True`。

学习率 1e4 太大，一步就冲过头，损失变成 inf（溢出）。看到 inf/nan 先怀疑学习率。

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

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
