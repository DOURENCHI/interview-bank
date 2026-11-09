---
id: Q-1734
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 40 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
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
print(np.arange(0, 10, 2).tolist(), np.linspace(0, 1, 3).tolist())
```

- **A.** [0, 2, 4, 6, 8] [0.0, 0.5, 1.0]
- **B.** [0, 2, 4, 6, 8] [0.0, 0.3333333333333333, 0.6666666666666666, 1.0]
- **C.** [2, 4, 6, 8] [0.0, 0.5, 1.0]
- **D.** [0, 2, 4, 6, 8, 10] [0.0, 0.5, 1.0]

## 口述答案

答案是 **A. [0, 2, 4, 6, 8] [0.0, 0.5, 1.0]**，实际输出 `[0, 2, 4, 6, 8] [0.0, 0.5, 1.0]`。

arange 左闭右开；linspace(0,1,3) 是「含端点、均分 3 份」得 0/0.5/1，注意它是按个数取点不是按步长。

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
