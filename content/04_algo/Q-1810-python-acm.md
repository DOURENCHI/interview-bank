---
id: Q-1810
title: 语言地基自测：类型、容器、作用域 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: draft
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 Python 程序对应的读入与输出写法是什么？

```python
import sys


def show(label, value):
    print(f"{label} = {value}")


show("type(3)", type(3))
show("type(3.0)", type(3.0))
show("7 // 2, 7 / 2, -7 // 2", (7 // 2, 7 / 2, -7 // 2))
show("7 % 3, -7 % 3", (7 % 3, -7 % 3))
show("round(2.675, 2)", round(2.675, 2))
show("[1,2,3][1:4]", [1, 2, 3][1:4])
show("[1,2,3][::-1]", [1, 2, 3][::-1])

a = [3, 1, 2]
print("sort() 返回", a.sort(), "排序后 a =", a)
print("sorted() 返回", sorted([3, 1, 2]))

counter = {"n": 0}


def bump():
    counter["n"] += 1
    return counter["n"]


print("连续调用", bump(), bump(), "计数器", counter)

print("版本", sys.version.split()[0])
```

输出样例：

```
type(3) = <class 'int'>
type(3.0) = <class 'float'>
7 // 2, 7 / 2, -7 // 2 = (3, 3.5, -4)
7 % 3, -7 % 3 = (1, 2)
round(2.675, 2) = 2.67
[1,2,3][1:4] = [2, 3]
[1,2,3][::-1] = [3, 2, 1]
sort() 返回 None 排序后 a = [1, 2, 3]
sorted() 返回 [1, 2, 3]
连续调用 1 2 计数器 {'n': 2}
版本 3.13.14
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
