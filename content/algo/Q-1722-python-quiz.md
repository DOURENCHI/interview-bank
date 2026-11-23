---
id: Q-1722
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 29 题）
module: algo
sub: 函数与异常
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
print(min([3, 1, 2]), max("a", "b"), sorted("cba"))
```

- **A.** 1 b ['a', 'b', 'c']
- **B.** 1 a ['a', 'b', 'c']
- **C.** 1 b ['c', 'b', 'a']
- **D.** 3 b ['a', 'b', 'c']

## 口述答案

答案是 **A. 1 b ['a', 'b', 'c']**，实际输出 `1 b ['a', 'b', 'c']`。

max 对字符串按字符码比较，"b" > "a"；sorted 返回列表不是字符串，sorted("cba") 得 ['a','b','c']。

## 讲深一层

讲深一层：max 有两种形态——传多个位置参数比这些值，或传一个可迭代对象比其元素，所以 max("a","b") 得 "b"，max("ab") 也是 "b"（逐字符比）。字符串按码点字典序，'Z'(90)<'a'(97)。sorted 对字符串返回字符列表，要还原成串得 "".join()。

## 高频追问

1. **max("ab") 和 max("a","b") 结果一样吗？** —— 都是 "b"，但前者比字符、后者比两个串。
2. **怎么按长度取最长串？** —— `max(words, key=len)`。
3. **怎么忽略大小写比较？** —— `key=str.lower`。

## 易错点

- 以为 sorted("cba") 返回 "abc"：返回 ['a','b','c'] 列表
- 按字母表直觉认为 'Z' > 'a'：码点 90<97，实际 'a' 更大
- 对空序列调 min/max：抛 ValueError，需给 default

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
