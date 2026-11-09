---
id: Q-1751
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 58 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
