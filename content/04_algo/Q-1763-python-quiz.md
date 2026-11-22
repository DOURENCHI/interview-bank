---
id: Q-1763
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 70 题）
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
m = torch.nn.Sequential(torch.nn.Linear(4, 8), torch.nn.ReLU(), torch.nn.Linear(8, 1))
print(sum(p.numel() for p in m.parameters()))
```

- **A.** 49
- **B.** 41
- **C.** 37
- **D.** 56

## 口述答案

答案是 **A. 49**，实际输出 `49`。

第一层 4×8+8 = 40，第二层 8×1+1 = 9，ReLU 无参数，合计 49。这是判断模型复杂度的第一个数字。

## 讲深一层

每层参数 = `out×in + out`（有 bias 时）。4→8 是 32+8=40，8→1 是 8+1=9，合计 49。ReLU 无参数，`Sequential` 本身也不额外产生参数。把第一层改成 `bias=False` 则 32+8=40；把 ReLU 换成 `BatchNorm1d(8)` 会多 16 个仿射参数（8 个 γ、8 个 β）。

## 高频追问

1. **`parameters()` 和 `state_dict()` 差在哪？** —— BN 的 `running_mean/var` 是 buffer，进 state_dict 但不进 parameters，所以参数量统计会漏掉它们
2. **冻结的参数算不算 numel？** —— 算，`numel()` 只看元素个数，与是否需要梯度无关
3. **换成 `Conv2d(1, 8, 3)` 参数量多少？** —— `8×1×3×3 + 8 = 80`，卷积核在空间维上共享权重

## 易错点

- 忘加 bias——得 32+8=40，正好落在选项 B 上
- 把 ReLU 当有参数——多算 0 个还好，若把它当 Linear 会多算 8×8
- 用 `len(list(m.parameters()))` 当参数量——得 4（4 个张量），不是 49

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
