---
id: Q-1729
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 36 题）
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
import numpy as np
a = np.array([[1, 2], [3, 4]])
print(a[0, 1], a[1], a[:, 0], a[0, :])
```

- **A.** 2 [3 4] [1 3] [1 2]
- **B.** 1 [3 4] [1 3] [1 2]
- **C.** 2 [3 4] [1 3] [3 4]
- **D.** 2 [3 4] [3 1] [1 2]

## 口述答案

答案是 **A. 2 [3 4] [1 3] [1 2]**，实际输出 `2 [3 4] [1 3] [1 2]`。

a[0,1] 取第 0 行第 1 列；a[1] 取整行；a[:,0] 取所有行的第 0 列；a[0,:] 取第 0 行全部。

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

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
