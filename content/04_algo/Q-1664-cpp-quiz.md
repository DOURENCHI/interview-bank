---
id: Q-1664
title: 这段 C++ 代码输出什么？（33 lambda 与绑定 · 第 52 题）
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
auto f = [](int a, int b){ return a > b ? a : b; };
cout << f(3, 7);
```

- **A.** 7
- **B.** 3
- **C.** 10
- **D.** 编译错误

## 口述答案

答案是 **A. 7**，实际输出 `7`。

lambda 的三段是 [] 捕获列表、() 参数、{} 函数体；这里返回两数较大者 7。[] 空捕获表示不使用外部局部变量。

## 讲深一层

lambda 的结构是 [捕获列表](参数) mutable -> 返回类型 { 函数体 }，除捕获列表外都可省略。这里无捕获，闭包还能隐式转成函数指针 int(*)(int,int)。每个 lambda 都有独一无二的闭包类型，两个写法相同的 lambda 之间不能互相赋值，只能用 auto 或 std::function 承接。

## 高频追问

1. **为什么是 7？** —— 三目运算符 a > b 为假，返回 b，即 7。
2. **能存进函数指针吗？** —— 可以，无捕获 lambda 有到函数指针的隐式转换；一旦有捕获就不行，只能用 std::function。
3. **返回类型要写吗？** —— 单条 return 可自动推导；多条 return 且类型不一致时，必须显式写 -> T 统一。

## 易错点

- 把 a > b ? a : b 看成取小，答 3 选 B
- 以为是求和，答 10 选 C
- 以为 lambda 必须写返回类型，判成编译错误选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 33 lambda 与绑定
