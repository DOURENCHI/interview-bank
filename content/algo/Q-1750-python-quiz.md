---
id: Q-1750
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 57 题）
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
t = torch.tensor([1.0, 2.0])
print(t.sum().item(), type(t.sum().item()).__name__, t.sum())
```

- **A.** 3.0 float tensor(3.)
- **B.** 3 int tensor(3.)
- **C.** 3.0 int tensor(3.)
- **D.** 3.0 float 3.0

## 口述答案

答案是 **A. 3.0 float tensor(3.)**，实际输出 `3.0 float tensor(3.)`。

item() 把标量张量转成 Python 数字（这里是 float）；不调 item() 直接 print 得到的是 tensor(3.) 这种张量表示。

## 讲深一层

`item()` 只接受单元素张量，返回 Python 标量，类型随 dtype：float32 → float，int64 → int；多元素调用抛 RuntimeError。不调它拿到 0 维张量，print 走 repr 得 `tensor(3.)`，还能 backward；调了就脱离计算图。若 t 是整型张量，会输出 `3 int`，即选项 B。

## 高频追问

1. **多元素张量调用 `item()` 会怎样？** —— 抛 `RuntimeError: a Tensor with 2 elements cannot be converted to Scalar`，只能先 `.sum()` 或索引到单个元素
2. **为什么 D 不对？** —— D 假设 print 张量输出 `3.0`，实际走 `__repr__` 打印 `tensor(3.)`；要打印纯数字必须 `.item()`
3. **`item()` 之后还能反向传播吗？** —— 不能，返回的是 Python float 已脱离计算图；要保留梯度得用 `.sum()` 这类张量运算

## 易错点

- 把 `type(...).__name__` 记成 `int`——`torch.tensor([1.0, 2.0])` 是 float32，`item()` 返回 float，写成 int 就选了 B
- 以为 `t.sum()` 返回 Python 数——它是 0 维张量，直接 print 得 `tensor(3.)` 而不是 `3.0`
- 对多元素张量写 `.item()`——整行直接报错，这题一分拿不到

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
