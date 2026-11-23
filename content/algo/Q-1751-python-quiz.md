---
id: Q-1751
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 58 题）
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
m = torch.arange(6).reshape(2, 3)
print(tuple(m.shape), m[0].tolist(), m[:, 1].tolist())
```

- **A.** (2, 3) [0, 1, 2] [1, 4]
- **B.** ((2, 3), [0, 3], [1, 4])
- **C.** ((3, 2), [0, 1, 2], [1, 4])
- **D.** ((2, 3), [0, 1, 2], [0, 3])

## 口述答案

答案是 **A. (2, 3) [0, 1, 2] [1, 4]**，实际输出 `(2, 3) [0, 1, 2] [1, 4]`。

arange(6) 得 0..5，reshape(2,3) 按行填成 [[0,1,2],[3,4,5]]；m[:,1] 取每行的第 1 列即 1 和 4。

## 讲深一层

`m.shape` 是 `torch.Size`（tuple 子类），print 显示 `torch.Size([2, 3])`，套 `tuple()` 才得 `(2, 3)`。`reshape` 行优先填充，0..5 排成两行。`m[0]` 与 `m[:,1]` 都是视图。改成 `reshape(3,2)` 则 `m[:,1]` 得 `[1,3]`。

## 高频追问

1. **`print(m.shape)` 和 `print(tuple(m.shape))` 一样吗？** —— 不一样，前者 `torch.Size([2, 3])`，后者 `(2, 3)`；选项里写 `(2, 3)` 是显式转过类型
2. **`m[0]` 和 `m[0, :]` 有区别吗？** —— 没有，省略的维默认取全部，两者都是第 0 行的视图
3. **改成 `reshape(3, 2)` 结果怎么变？** —— 矩阵变 `[[0,1],[2,3],[4,5]]`，`m[0].tolist()` 得 `[0, 1]`，`m[:,1].tolist()` 得 `[1, 3]`

## 易错点

- 把 `m.shape` 直接当元组答——实际打印带 `torch.Size([...])` 外壳，选项 C/D 就是把外壳与内容搞混
- 按列优先理解 `reshape`——会算成 `[[0,3],[1,4],[2,5]]`，`m[:,1]` 写错成 `[3, 5]`
- 认为切片是拷贝——`m[0] += 100` 会改掉原张量，调试时容易怀疑是 bug

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
