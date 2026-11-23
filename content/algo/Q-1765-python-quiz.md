---
id: Q-1765
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 72 题）
module: algo
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

`losses` 记的是每次 `step` 之前的 loss（顺序 loss→zero_grad→backward→step），所以 `losses[-1]` 比训练结束时的真实 loss 略大。sum + lr=0.01 在 50 步内把 46.89 压到 0.13，方向与步长都对。

## 高频追问

1. **`losses[0]=46.8943` 怎么来的？** —— seed=4 的初始 w、b 随机，三个样本预测偏离真值，平方和累加得 46.89
2. **为什么记录的是 step 前的 loss？** —— 代码顺序决定，`loss` 在前向时算好，`step()` 在其后才改参数
3. **想更快收敛怎么办？** —— 换 Adam、标准化输入、适当调大 lr，或改用 `reduction="mean"` 统一量纲

## 易错点

- 把 `losses.append` 挪到 `step()` 之后——记录的是更新后的 loss，首值就对不上 46.8943
- 认为 loss 必须严格单调下降——换 mini-batch 后会抖动，全批才单调
- 混淆 sum 与 mean——mean 下首值约 15.63，选项全对不上

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
