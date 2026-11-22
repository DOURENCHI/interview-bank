---
id: Q-1712
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 19 题）
module: 04_algo
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
print([1, 2, 3].__class__.__name__, (1,).__class__.__name__, {1: 2}.__class__.__name__)
```

- **A.** list tuple dict
- **B.** list int dict
- **C.** list tuple set
- **D.** List Tuple Dict

## 口述答案

答案是 **A. list tuple dict**，实际输出 `list tuple dict`。

三种括号对应 list / tuple / dict，类名首字母小写——这是 Python 官方风格，与 Java 的 List / Map 相反。

## 讲深一层

讲深一层：__class__ 指向类型对象，__name__ 取其短名，等价写法是 type(x).__name__。类名小写是内置类型的命名约定，与 Java 的 List/Map 相反；但用户自定义类通常用大驼峰，别把「小写」当普遍规律。花括号要分清：{1:2} 是 dict，{1,2} 是 set，空 {} 是 dict 而不是 set。

## 高频追问

1. **怎么判断是不是 dict？** —— isinstance(x, dict)，或 type(x) is dict。
2. **{1,2} 的类名是什么？** —— set；空集合只能用 set() 构造。
3. **__class__ 和 type() 有区别吗？** —— 一般等价，老式代理对象上 __class__ 可能被重写。

## 易错点

- 把 (1,).__class__ 写成 int：逗号才构成元组，漏逗号的 (1) 就是 int
- 把 {1:2} 当 set：带冒号是 dict，输出 dict 不是 set
- 答成 List/Tuple/Dict：首字母大写是 Java 风格，Python 全小写

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
