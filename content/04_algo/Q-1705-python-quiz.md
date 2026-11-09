---
id: Q-1705
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 12 题）
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
d = {"a": 1}
print(d.get("b", 0), d.get("a"), len(d))
```

- **A.** 0 1 1
- **B.** None 1 1
- **C.** 0 1 2
- **D.** 1 1 1

## 口述答案

答案是 **A. 0 1 1**，实际输出 `0 1 1`。

get 找不到键返回默认值（这里是 0），不会像 d["b"] 那样抛 KeyError；len(d) 是键的个数，此时仍是 1（get 不会插入键）。

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
