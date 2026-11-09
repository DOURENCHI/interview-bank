---
id: Q-1741
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 47 题）
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
f = np.array([3.7, -2.2, 5.0])
print(np.round(f, 1).tolist(), np.clip(f, -2, 4).tolist())
```

- **A.** [3.7, -2.2, 5.0] [3.7, -2.0, 4.0]
- **B.** [3.7, -2.2, 5.0] [-2.0, 4.0, 4.0]
- **C.** [3.7, -2.2, 5.0] [-2.2, 4.0, 5.0]
- **D.** [3.7, -2.2, 5.0] [3.7, -2.0, 5.0]

## 口述答案

答案是 **A. [3.7, -2.2, 5.0] [3.7, -2.0, 4.0]**，实际输出 `[3.7, -2.2, 5.0] [3.7, -2.0, 4.0]`。

np.round 是四舍五入（与内置 round 的银行家舍入不同），一位小数下 3.7/5.0 不变；clip 把值限制在 [-2, 4]，-2.2 被抬到 -2、5.0 被压到 4。

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
