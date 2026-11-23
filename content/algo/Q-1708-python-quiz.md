---
id: Q-1708
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 15 题）
module: algo
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
print(all([1, 1]), any([0, 0]), sum([1, 2, 3]), max([1, 5, 3]))
```

- **A.** True False 6 5
- **B.** True False 6 3
- **C.** False False 6 5
- **D.** True True 6 5

## 口述答案

答案是 **A. True False 6 5**，实际输出 `True False 6 5`。

all 对空集合返回 True、any 返回 False，这里 all([1,1]) 因为两个 1 都为真所以 True；max 取最大值 5。

## 讲深一层

讲深一层：全称量词在空集上为真，所以 all([]) 是 True；存在量词在空集上为假，any([]) 是 False，这两个默认值最常被记反。两者都短路。sum 默认起点是 0，所以 sum(["a","b"]) 抛 TypeError，要指定 start=""；max([]) 抛 ValueError，需给 default。

## 高频追问

1. **all([]) 为什么是 True？** —— 没有反例即真，逻辑上的空真。
2. **sum 能拼字符串吗？** —— 不能，用 "".join(list)。
3. **max 怎么处理空列表？** —— `max(a, default=0)` 或先判空。

## 易错点

- 把 any([]) 记成 True：空集无真元素，实际 False
- 用 sum 求平均：忘了除以 len，得到 6 而不是均值
- 对空列表直接 max：抛 ValueError: max() arg is an empty sequence

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
