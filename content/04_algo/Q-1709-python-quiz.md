---
id: Q-1709
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 15 题）
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
