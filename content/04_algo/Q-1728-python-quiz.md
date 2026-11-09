---
id: Q-1728
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 34 题）
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
counter = {"n": 0}
def bump():
    counter["n"] += 1
    return counter["n"]
print(bump(), bump(), counter["n"])
```

- **A.** 1 2 2
- **B.** 1 1 1
- **C.** 1 2 3
- **D.** 0 1 1

## 口述答案

答案是 **A. 1 2 2**，实际输出 `1 2 2`。

可变对象作为全局变量时函数内的修改会生效，字典内容被就地累加；第三次打印仍是 2，因为 counter 里存的就是 2。

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
