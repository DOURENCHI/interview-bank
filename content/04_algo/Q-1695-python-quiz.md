---
id: Q-1695
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 1 题）
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
print(type(3), type(3.0), type("a"), type([1]))
```

- **A.** <class 'int'> <class 'float'> <class 'str'> <class 'list'>
- **B.** <class 'int'> <class 'float'> <class 'str'> <class 'tuple'>
- **C.** <class 'int'> <class 'double'> <class 'str'> <class 'list'>
- **D.** <class 'number'> <class 'float'> <class 'str'> <class 'array'>

## 口述答案

答案是 **A. <class 'int'> <class 'float'> <class 'str'> <class 'list'>**，实际输出 `<class 'int'> <class 'float'> <class 'str'> <class 'list'>`。

Python 里 int / float / str / list 都是内置类型，浮点数只有一种 float（没有 double），列表是 list，元组才是 tuple。

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
