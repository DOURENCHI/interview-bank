---
id: Q-1616
title: 这段 C++ 代码输出什么？（03 类型 · 第 4 题）
module: algo
sub: 语法与陷阱
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
cout << sizeof('a') << sizeof("a");
```

- **A.** 11
- **B.** 12
- **C.** 22
- **D.** 14

## 口述答案

答案是 **B. 12**，实际输出 `12`。

'a' 是 char，占 1 字节；"a" 是字符串，末尾还有 '\0'，占 2 字节。

## 讲深一层

sizeof 是编译期运算符、不求值：'a' 在 C++ 里类型是 char（1 字节），"a" 是 char[2]（含结尾 '\0'）。换到 C 就不同——C 的字符常量类型是 int，sizeof('a')=4，输出 42；换 L'a' 是 wchar_t，宽度由平台定（Windows 2、Linux 4 字节）。

## 高频追问

1. **为什么 "a" 是 2 字节？** —— 字符串字面量是字符数组，编译器自动在末尾补一个 '\0'，所以 char[2]；strlen("a") 仍然只数到 1。
2. **C 里结果一样吗？** —— 不一样。C 的 'a' 是 int 类型，sizeof 得 4，输出 42；这是 C 与 C++ 在字符常量类型上的经典差异。
3. **sizeof 和 strlen 怎么选？** —— sizeof 编译期求数组总字节，含 '\0'；strlen 运行期数到 '\0'，不含它。传参退化成指针后 sizeof 只剩 8。

## 易错点

- 把 'a' 当字符串算成 2 字节，答 22，选成 C
- 忘记 '\0' 占位，答 11，选成 A
- 把 C 的规则套过来，答 42 或 14

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 03 类型
