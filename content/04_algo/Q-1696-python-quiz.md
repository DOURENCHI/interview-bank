---
id: Q-1696
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 2 题）
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
print(7 // 2, 7 / 2, -7 // 2, 7 % 3, -7 % 3)
```

- **A.** 3 3.5 -4 1 2
- **B.** 3 3.5 -3 1 2
- **C.** 3 3.5 -4 1 -1
- **D.** 4 3.5 -3 2 2

## 口述答案

答案是 **A. 3 3.5 -4 1 2**，实际输出 `3 3.5 -4 1 2`。

// 是向下取整除法（向负无穷取整），所以 -7 // 2 = -4 而不是 -3；/ 永远得到 float；% 的结果符号跟除数，这里 -7 % 3 = 2。

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

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
