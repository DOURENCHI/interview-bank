---
id: Q-1635
title: 这段 C++ 代码输出什么？（17 虚基类 · 第 23 题）
module: algo
sub: 对象与继承
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
struct F { F(int x = 0) { cout << x; } };
struct S : virtual F { S() : F(1) {} };
struct T : virtual F { T() : F(2) {} };
struct ST : S, T { ST() : F(9) {} };
int main() { ST st; }
```

- **A.** 9
- **B.** 12
- **C.** 129
- **D.** 912

## 口述答案

答案是 **A. 9**，实际输出 `9`。

虚基类由最终派生类 ST 直接构造，且只构造一次；S、T 初始化列表里的 F(1)、F(2) 被忽略。

## 讲深一层

虚基类由最派生类直接构造，中间类 S、T 的 mem-initializer 里对 F 的初始化被忽略，且全程只构造一次。ST 写了 F(9)，所以只输出 9。若 ST 不写，则调用 F 的默认实参 F(0) 输出 0，这正说明最终派生类必须负责虚基类初始化。F 只保留一份子对象，避免了菱形继承的二义。

## 高频追问

1. **为什么不是 12 或 129？** —— 虚基类只由最派生类 ST 构造一次，S 的 F(1)、T 的 F(2) 都被忽略，不会输出。
2. **ST 不写 F(9) 会怎样？** —— 走 F 的默认实参 F(int x = 0)，输出 0；中间类的实参同样无效。
3. **去掉 virtual 呢？** —— F 不再是 ST 的直接基类，ST 的初始化列表写 F(9) 直接编译报错；同时 F 会出现两份子对象，访问产生二义。

## 易错点

- 认为 S、T 各构造一次 F，答 12 选 B
- 以为 ST 的 9 排在最后，答 129 选 C
- 以为虚基类构造两次但只显示一次，答 912 选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 17 虚基类
