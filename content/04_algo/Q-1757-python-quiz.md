---
id: Q-1757
title: 这段 Python 代码输出什么？（04 线性模型与梯度下降 · 第 64 题）
module: 04_algo
sub: 容器与切片
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

`MSELoss(reduction="sum")` 不除样本数，梯度是 mean 版的 3 倍，等价于把 lr 放大到 0.03。该问题 Hessian 的两个特征值是 33.3 与 0.72，慢方向每步只衰减 0.7%，`0.9928^100 ≈ 0.49`，所以 w 停在 1.9622、b 停在 0.086，预测 4 得 7.9346 而不是 8.0。

## 高频追问

1. **为什么不是精确的 2.0 / 0.0？** —— 100 轮远未收敛，b 方向曲率极小（特征值 0.72），是最慢的方向
2. **换成 `reduction="mean"` 会怎样？** —— 梯度小 3 倍，同样 100 轮离 2.0 更远，说明 reduction 会改变有效学习率
3. **想收敛到 2.0 怎么办？** —— 加轮数、调大 lr（上限受最大特征值 33.3 约束，lr<0.06）或先标准化输入

## 易错点

- 直接答 2.0 / 0.0 / 8.0（选项 B）——把"应该收敛到"当成"实际算出来"
- 认为 sum 与 mean 只差常数不影响训练——梯度差 3 倍，100 轮后的 w 完全不同
- 把 weight 当标量——`Linear(1,1)` 的 weight 形状是 `(1,1)`，要 `.item()` 才能取数

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 04 线性模型与梯度下降
