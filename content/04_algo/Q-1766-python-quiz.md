---
id: Q-1766
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 72 题）
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
torch.manual_seed(4)
m = torch.nn.Linear(1, 1)
opt = torch.optim.SGD(m.parameters(), lr=0.01)
xs = torch.Tensor([[1.0], [2.0], [3.0]])
ys = torch.Tensor([[2.0], [4.0], [6.0]])
crit = torch.nn.MSELoss(reduction="sum")
losses = []
for _ in range(50):
    loss = crit(m(xs), ys)
    opt.zero_grad()
    loss.backward()
    opt.step()
    losses.append(round(loss.item(), 4))
print(losses[0], losses[-1], losses[-1] < losses[0])
```

- **A.** 46.8943 0.1329 True
- **B.** (46.8943, 46.8943, False)
- **C.** (0.1329, 46.8943, False)
- **D.** (46.8943, 0.1329, False)

## 口述答案

答案是 **A. 46.8943 0.1329 True**，实际输出 `46.8943 0.1329 True`。

50 轮后损失从 46.89 降到 0.13，第三项 True 说明确实在下降。这是判断训练循环写对了的最直接证据。

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

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
