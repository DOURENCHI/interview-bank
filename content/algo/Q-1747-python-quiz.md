---
id: Q-1747
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 54 题）
module: algo
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
w = torch.tensor([1.0, 2.0], requires_grad=True)
loss = (3 * w).sum()
loss.backward()
print(w.grad.tolist())
```

- **A.** [3.0, 3.0]
- **B.** [1.0, 2.0]
- **C.** [3.0, 6.0]
- **D.** [6.0, 6.0]

## 口述答案

答案是 **A. [3.0, 3.0]**，实际输出 `[3.0, 3.0]`。

loss = 3w 之和，每个 w 的梯度都是 3。乘法把标量梯度「广播」到每个元素。

## 讲深一层

讲深一层：loss=(3w).sum() 中 sum 把标量 1 广播回每个元素，3 作为常数系数在反向时原样保留，所以每个 w 的梯度都是 3，与 w 的取值无关。若系数改成张量（如 w*a），梯度就变成 a 的对应元素；若把 sum 换成 mean，则再除以元素个数 2，得 1.5。

## 高频追问

1. **系数是张量时梯度怎么变？** —— 对 w 的梯度就是该张量对应元素。
2. **换成 mean 后是多少？** —— 3/2=1.5。
3. **为什么是 3 不是 6？** —— 6 是 w=2 时的函数值 3w，不是导数。

## 易错点

- 把 [3,6] 当梯度：那是 3w 的值，导数是常数 3
- 以为每个元素梯度不同：线性缩放，全部相同
- 忘记 sum 的作用：没有 sum 时向量不能直接 backward

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
