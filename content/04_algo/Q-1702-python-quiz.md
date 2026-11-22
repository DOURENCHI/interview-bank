---
id: Q-1702
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 9 题）
module: 04_algo
sub: 语法与类型
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
print(1 == 1.0, 1 == 1, [] == [], [] is [])
```

- **A.** True True True False
- **B.** True True True True
- **C.** True False True False
- **D.** False True False False

## 口述答案

答案是 **A. True True True False**，实际输出 `True True True False`。

== 比的是值，1 == 1.0 为真；两个空列表内容相等但不是同一个对象，所以 == 为 True、is 为 False——这是 Python 新手最常踩的坑之一。

## 讲深一层

讲深一层：== 调 __eq__ 比值，is 比 id() 即内存地址。CPython 缓存 -5~256 的小整数并驻留部分字符串，所以 a=256;b=256 时 a is b 常为 True，换成 257 就可能 False——这属于实现细节，不能依赖。同一对象 is 为真时 == 一般也为真，除非 __eq__ 被重写。判 None 用 is，判内容用 ==。

## 高频追问

1. **为什么判 None 要用 is？** —— None 是单例，is 不受 __eq__ 重写影响，也更快。
2. **1 is 1.0 是什么？** —— False，类型不同对象不同，但 1 == 1.0 是 True。
3. **字符串 is 为什么有时是 True？** —— 短标识符会被 intern 复用，运行时拼接的长串不保证。

## 易错点

- 用 is 比较数值：a=257;b=257 时 a is b 可能 False，输出与预期相反
- 以为 [] == [] 为 False：两个空列表内容相等，== 得 True
- 用 == 判 None：对象重写 __eq__ 返回真时会误判，应写 `x is None`

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
