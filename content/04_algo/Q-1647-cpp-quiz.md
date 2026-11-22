---
id: Q-1647
title: 这段 C++ 代码输出什么？（28 迭代器与 string · 第 35 题）
module: 04_algo
sub: 模板与 STL
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/C++实验台/C++考点实验台.html
verified_at: 2026-11-21
tags: [C++, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```cpp
string s = "abc";
cout << (s.find('x') == string::npos) << " " << s.rfind('b');
```

- **A.** 1 1
- **B.** 0 1
- **C.** 1 0
- **D.** 0 -1

## 口述答案

答案是 **A. 1 1**，实际输出 `1 1`。

find('x') 找不到返回 string::npos，与它比较得 true，输出 1；rfind('b') 从后往前找，返回的下标仍是 1。npos 不是 -1 的有效下标。

## 讲深一层

npos 是 size_t 的最大值（64 位下 18446744073709551615），必须与 find 的返回类型同类型比较，写 < 0 恒为假。rfind 从后往前搜，但返回的仍是正向下标，所以 'b' 得 1。把 npos 赋给 int 会得到 -1，容易被误当成「下标 -1 有效」，这是经典陷阱。

## 高频追问

1. **第一个 1 怎么来的？** —— find('x') 返回 npos，与 npos 相等为 true，bool 默认输出 1。
2. **rfind 为什么也是 1？** —— 从尾部向前找到下标 1 的 'b'，返回正向下标而非倒数序号。
3. **为什么不能写 find('x') < 0？** —— 返回值是无符号 size_t，与 0 比较永远为假，判不出未找到，必须用 == npos。

## 易错点

- 把 npos 当有效下标，答 0 1 选 B
- 以为 rfind 返回倒数位置 0，答 1 0 选 C
- 强转 int 后判断 -1，答 0 -1 选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 28 迭代器与 string
