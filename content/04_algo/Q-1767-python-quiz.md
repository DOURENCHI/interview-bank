---
id: Q-1767
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 74 题）
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
m = torch.nn.Linear(2, 2)
print(all(p.requires_grad for p in m.parameters()))
```

- **A.** True
- **B.** False
- **C.** None
- **D.** 0

## 口述答案

答案是 **A. True**，实际输出 `True`。

nn.Module 的参数默认 requires_grad=True，所以全部为真——这是梯度能自动回传的前提。

## 讲深一层

`nn.Parameter` 构造时默认 `requires_grad=True`，`nn.Linear` 的 weight/bias 都是 Parameter，所以全部为真。注意 `all()` 对空序列返回 True——无参数模块（如只有 ReLU）也会打印 True，这是逻辑上的坑。冻结只需把标志改 False，张量本身不变。

## 高频追问

1. **`all([])` 返回什么？** —— True，所以对无参数模块做这个判断会得到"全部可训练"的假象
2. **怎么只冻结第一层？** —— 遍历 `named_parameters()`，按前缀 `c1.` 匹配后 `requires_grad_(False)`
3. **冻结后还要传给 optimizer 吗？** —— 可以不传；传了也不会更新，但会多占一点状态内存

## 易错点

- 用 `any` 代替 `all`——本题两者都为 True 看不出差别，换到部分冻结的场景就答反了
- 以为 `requires_grad` 是张量里的数值——它是布尔标志，不参与计算
- 把 buffer 也纳入判断——BN 的 running_mean 没有 requires_grad 属性语义，容易抛 AttributeError

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
