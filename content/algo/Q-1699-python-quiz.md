---
id: Q-1699
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 6 题）
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
print((1, 2, 3)[1], [1, 2, 3][1], len("hello"))
```

- **A.** 2 2 5
- **B.** 1 1 5
- **C.** 2 2 4
- **D.** 3 3 5

## 口述答案

答案是 **A. 2 2 5**，实际输出 `2 2 5`。

下标从 0 起，元组和列表都取到第 1 个元素即 2；len("hello") 是 5 个字符（不是 6，Python 字符串没有结尾的 \0）。

## 讲深一层

讲深一层：下标 0 起、支持负数从尾部数，-1 是最后一个；但越界会抛 IndexError，切片越界反而自动截断不报错。len 对 str 数的是 Unicode 码点，len("中文")=2、len("🙂")=1，按 UTF-8 字节算则分别是 6 和 4。单元素元组必须写 (1,)，漏掉逗号的 (1) 只是加了括号的整数。

## 高频追问

1. **a[-1] 和 a[len(a)-1] 等价吗？** —— 等价，前者更 Pythonic。
2. **切片越界会怎样？** —— 不报错，自动夹到边界，a[1:100] 返回剩余部分。
3. **len 和 sys.getsizeof 区别？** —— len 是元素个数，getsizeof 是对象占用的字节数。

## 易错点

- 把下标当 1 起：(1,2,3)[1] 会答成 1，实际是 2
- 以为 len("hello") 含结尾 \0：答 6，Python 字符串没有 C 的终止符，是 5
- 写 (1) 当单元素元组：它是 int，参与索引或运算时报 TypeError

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
