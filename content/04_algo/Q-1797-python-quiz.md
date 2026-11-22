---
id: Q-1797
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 104 题）
module: 04_algo
sub: 并发与性能
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
m = torch.nn.Linear(2, 1)
opt = torch.optim.SGD(m.parameters(), lr=0.1, momentum=0.9)
print(opt.param_groups[0]["lr"], opt.param_groups[0]["momentum"])
```

- **A.** 0.1 0.9
- **B.** (0.01, 0.9)
- **C.** (0.1, 0.0)
- **D.** (0.9, 0.1)

## 口述答案

答案是 **A. 0.1 0.9**，实际输出 `0.1 0.9`。

SGD 的 lr 是学习率、momentum 是动量系数；param_groups[0] 里存着超参，可以随时改。

## 讲深一层

优化器把参数分成若干 param_group，每组一份超参副本，构造时的 `defaults` 只是建组模板。所以 lr、momentum 挂在优化器而非模型上。微调时给不同层不同 lr 就是传多个 dict；scheduler 改的也是 group 里的 lr，不动模型。

## 高频追问

1. **怎么给不同层不同 lr？** —— `SGD([{"params": backbone, "lr": 1e-4}, {"params": head, "lr": 1e-2}], lr=1e-3)`
2. **scheduler 改的是哪个值？** —— `param_groups[i]["lr"]`，所以改完立刻对下一步生效
3. **momentum 的物理意义？** —— 累积历史梯度方向，抑制震荡、加速沿一致方向前进

## 易错点

- 用 `opt.lr` 访问——AttributeError，必须 `opt.param_groups[0]["lr"]`
- 以为 lr 存在模型上——模型只有参数，超参在优化器
- 认为 momentum 默认是 0.9——默认 0，本题 0.9 是显式传的

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
