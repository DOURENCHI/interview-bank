---
id: Q-1642
title: 这段 C++ 代码输出什么？（22 lambda · 第 30 题）
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
int x = 1;
auto f = [x] { return x; };
auto g = [&x] { return x; };
x = 5;
cout << f() << g();
```

- **A.** 15
- **B.** 55
- **C.** 11
- **D.** 51

## 口述答案

答案是 **A. 15**，实际输出 `15`。

[x] 在创建 lambda 时拷贝一份 x（当时是 1）；[&x] 引用外面的 x，调用时已经是 5。

## 讲深一层

捕获列表在 lambda 创建那一刻求值：[x] 立刻拷贝当时的 1，之后 x 改成 5 与 f 无关；[&x] 只保存引用，调用时才去读，得 5。按值捕获的副本在 lambda 内默认只读，要修改必须加 mutable，且改的只是副本。引用捕获要保证 lambda 不会活过被捕获变量。

## 高频追问

1. **为什么 f() 是 1？** —— 按值捕获在定义时就复制了 x 的当前值 1，之后外部赋 5 不影响这份副本。
2. **为什么 g() 是 5？** —— 按引用捕获不复制，g 执行时读到的就是已经改成 5 的 x。
3. **mutable 有什么用？** —— 允许在 lambda 体内修改按值捕获的副本，但外部 x 不变，下次调用仍是上次改后的副本值。

## 易错点

- 以为按值捕获也跟随外部修改，答 55 选 B
- 以为 [&x] 也在定义时取值，答 11 选 C
- 把 [x] 和 [&x] 的输出顺序看反，答 51 选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 22 lambda
