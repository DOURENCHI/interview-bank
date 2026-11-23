---
id: Q-1704
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 11 题）
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
a = [3, 1, 2]
print(a.sort(), sorted([3, 1, 2]))
```

- **A.** None [1, 2, 3]
- **B.** ([1, 2, 3], [1, 2, 3])
- **C.** ([3, 1, 2], [1, 2, 3])
- **D.** (None, None)

## 口述答案

答案是 **A. None [1, 2, 3]**，实际输出 `None [1, 2, 3]`。

list.sort() 是原地排序，返回 None；sorted() 返回新列表不改原对象。要「排序结果又拿新列表」就用 sorted。

## 讲深一层

讲深一层：list.sort() 原地排序并返回 None，这是刻意设计——让「有返回值」暗示「产生了新对象」。sorted() 接受任意可迭代对象并总是返回 list，所以 sorted("cba") 得 ['a','b','c'] 而不是 "abc"。两者都是稳定的 Timsort，key 对每个元素只算一次。

## 高频追问

1. **为什么 sort 返回 None？** —— 防止误以为拿到新列表，也避免同时存两份数据。
2. **怎么按多个键排？** —— `key=lambda x:(x[1],x[0])`，或分两次稳定排序。
3. **怎么降序又保持稳定？** —— `sorted(a,key=...,reverse=True)`，reverse 不会破坏相等元素的原有顺序。

## 易错点

- 写 `a = a.sort()`：a 变成 None，后续 a[0] 抛 TypeError
- 以为 sorted 会改原列表：原列表顺序不变，只是多了一个新列表
- 以为 sorted("cba") 返回字符串：返回 ['a','b','c']，要字符串得 "".join(...)

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
