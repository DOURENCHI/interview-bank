---
id: Q-1766
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 73 题）
module: 04_algo
sub: 语法与类型
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
torch.manual_seed(5)
m = torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.Dropout(0.5))
m.train()
a = float(m(torch.ones(1, 4)).sum().detach())
m.eval()
b = float(m(torch.ones(1, 4)).sum().detach())
print(round(a, 4), round(b, 4))
```

- **A.** 3.4002 1.4552
- **B.** (3.4002, 3.4002)
- **C.** (1.4552, 3.4002)
- **D.** (3.4002, 1.4552)

## 口述答案

答案是 **A. 3.4002 1.4552**，实际输出 `3.4002 1.4552`。

train() 下 Dropout 随机置零一半神经元，输出被放大（除以 1-p）；eval() 下关闭 Dropout，输出确定。同一份权重两种模式输出不同。

## 讲深一层

train 模式按 p 置零，并把保留值除以 `1-p`（inverted dropout），保证输出期望不变；eval 模式既不置零也不缩放。所以 train 得 3.4002（本次采样的随机结果），eval 得 1.4552（确定的 Linear 输出）。同一份权重、同一输入，两种模式结果不同，这是模式标志而不是权重差异。

## 高频追问

1. **为什么要除以 `1-p`？** —— 保持训练与推理的期望一致，推理时就不必再乘 `(1-p)` 做补偿
2. **train 模式连跑两次结果一样吗？** —— 不一样，每次前向重新采样 mask；本题能复现是因为之前固定了 seed
3. **eval 后忘了切回 train 会怎样？** —— 训练时 Dropout 失效、BN 用运行统计量，正则消失且统计量不再更新

## 易错点

- 认为 eval 输出 = train 输出 × 0.5——inverted dropout 下 eval 完全不缩放，直接是 1.4552
- 以为 Dropout 有权重参数——它没有可学参数，只有 p 与 training 标志
- 只调子模块 `.eval()` 而父模块仍 train——父模块的 `train()` 会递归覆盖子模块状态

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
