---
id: Q-1803
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 110 题）
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
torch.manual_seed(10)
d = torch.nn.Dropout(0.5)
d.eval()
print(round(float(d(torch.ones(10)).sum()), 4))
```

- **A.** 10.0
- **B.** 0.0
- **C.** 5.0
- **D.** 1.0

## 口述答案

答案是 **A. 10.0**，实际输出 `10.0`。

eval 模式关闭 Dropout，10 个 1 原样通过，和是 10.0。推理时忘了 model.eval() 是最常见的线上事故。

## 讲深一层

eval 模式 Dropout 退化成恒等映射，既不置零也不缩放——因为缩放已在 train 阶段做进数值里（inverted dropout）。所以 10 个 1 原样通过，和是 10.0。若换成经典 dropout（train 不缩放、推理乘 1−p），才会得 5.0，这是两种实现的根本差别。

## 高频追问

1. **什么情况下 eval 要做缩放？** —— 经典 dropout 实现；PyTorch 用 inverted 版本，推理不需要
2. **忘了 `eval()` 的后果？** —— 输出随机、线上指标抖动，是最常见的上线事故
3. **与 `no_grad()` 的区别？** —— 前者控制层行为，后者控制建图，两件独立的事

## 易错点

- 答 5.0——以为推理要乘 `(1−p)`（选项 C）
- 认为 eval 会把输出清零——恰恰相反，eval 是全部保留
- 只给 Dropout 调 eval 忘了 BN——BN 仍用批统计，结果不稳定

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
