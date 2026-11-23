---
id: Q-1621
title: 这段 C++ 代码输出什么？（06 数组与字符串 · 第 9 题）
module: algo
sub: 指针与内存
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
char s[] = "hello";
cout << sizeof(s) << " " << strlen(s);
```

- **A.** 5 5
- **B.** 6 5
- **C.** 6 6
- **D.** 5 6

## 口述答案

答案是 **B. 6 5**，实际输出 `6 5`。

sizeof 算整个数组，包括末尾的 '\0'；strlen 数到 '\0' 为止。

## 讲深一层

sizeof 是编译期算出的字节数，char s[] = "hello" 声明为 6 字节数组，含末尾 '\0'；strlen 运行期数到 '\0'，得 5。同一个 s 传进函数后退化为 char*，sizeof 变成指针大小（64 位下 8），这是最常见的失分点。若写成 char *s = "hello"，sizeof 同样是 8。

## 高频追问

1. **为什么 sizeof 是 6？** —— 字符串字面量初始化字符数组时连 '\0' 一起拷进去，数组长度是 5 个字符加 1 个终止符。
2. **传进函数还是 6 吗？** —— 不是。数组形参退化为指针，sizeof 得 8（64 位），要传长度或改用数组引用模板。
3. **strlen 有坑吗？** —— 它逐字节扫到 '\0'，数组未终止就越界读；复杂度 O(n)，循环里反复调用会拖慢。

## 易错点

- 认为 sizeof 不含 '\0'，答 5 5，选成 A
- 把 strlen 也算终止符，答 6 6，选成 C
- 在函数内对形参写 sizeof 求数组长度，得 8 而不是 6

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 06 数组与字符串
