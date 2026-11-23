---
id: Q-1800
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 107 题）
module: algo
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

一步更新量是 `lr×grad`，量级 1e4×几十，w 直接跳到 1e5 以上；下一步 loss 含 w 的平方，放大到 1e10 再乘 lr 继续爆炸，几轮就超过 float32 上限 3.4e38 变 inf。inf 参与后续运算仍是 inf，不会自己回到有限值。`first` 是第一次 step 之前的 loss。

## 高频追问

1. **为什么是 inf 不是 nan？** —— nan 需要 `inf−inf` 或 `0×inf`，这里只有单向上溢
2. **怎么预防？** —— 梯度裁剪、lr warmup、输入标准化，并监控 `torch.isfinite`
3. **`first=48.404` 怎么来的？** —— seed=9 的初始参数，第一次更新前的 loss

## 易错点

- 说会收敛到 0——lr=1e4 是发散，方向完全相反
- 以为 inf 会被自动裁剪——PyTorch 不会，必须手动 `clip_grad_norm_`
- 把 `1e4` 读成 `1e-4`——差 8 个数量级，结论彻底反了

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
