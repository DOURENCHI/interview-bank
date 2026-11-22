---
id: Q-1768
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 75 题）
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
m = torch.nn.Linear(2, 2)
for p in m.parameters():
    p.requires_grad_(False)
print(any(p.requires_grad for p in m.parameters()))
```

- **A.** False
- **B.** True
- **C.** None
- **D.** 0

## 口述答案

答案是 **A. False**，实际输出 `False`。

requires_grad_(False) 冻结参数后，any 判断为 False。做迁移学习或只训部分层时就靠它。

## 讲深一层

`requires_grad_()` 是带下划线的原地方法，返回自身，把标志改成 False。冻结后反向不会为该参数分配 grad（保持 None），前向仍正常算，只是不建那段图，省显存。若输入 requires_grad=True，输出仍会是 True——输出标志看的是所有输入，不只参数。

## 高频追问

1. **冻结后 `p.grad` 是什么？** —— None，因为反向时直接跳过，不会写 0
2. **冻结与不传进 optimizer 的区别？** —— 前者连计算图都不建，省显存；后者照样建图只是不更新
3. **怎么恢复训练？** —— `p.requires_grad_(True)`，注意 optimizer 若当初没传该参数，需要重建

## 易错点

- 以为冻结会把 weight 置 0——参数值原样保留，只是不再更新
- 以为 `any` 返回 0——`any` 返回 bool，print 出 `False` 而不是 `0`
- 只改 `p.data.requires_grad`——`.data` 脱离 autograd，改它无效且危险

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
