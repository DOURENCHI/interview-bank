---
id: Q-1625
title: 这段 C++ 代码输出什么？（07 指针 · 第 13 题）
module: 04_algo
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
int a = 1, b = 2;
int * const p = &a;
p = &b;
cout << *p;
```

- **A.** 编译错误
- **B.** 2
- **C.** 1
- **D.** 运行时崩溃

## 口述答案

答案是 **A. 编译错误**，实际输出 `编译错误`。

int * const p 是指针常量：p 本身不能改指向。const 在星号右边，锁的是指针。

## 讲深一层

从变量名往外读：const 紧贴 p，锁的是指针本身——p 不能改指向，但 *p 可写。const int *p 与 int const *p 里 const 修饰的是 int，指针可改、所指不可写；const int * const p 两者都锁。指针常量必须在定义时初始化，不能先声明、之后再赋一个地址。

## 高频追问

1. **这句声明到底锁了什么？** —— int * const p 是常量指针，p 的指向不可变，*p 可读写；const 在星号右侧，修饰的是指针变量本身。
2. **换成 const int *p 呢？** —— 编译通过，p 可以改指 &b，输出 2；但 *p = 5 非法，因为所指对象被 const 修饰。
3. **为什么不能先声明后赋值？** —— const 对象必须在定义时初始化，p 没有默认值可填，漏写初始化就是编译错误。

## 易错点

- 把 const 位置看反，以为锁的是 *p，答 2 选 B
- 认为改指向只是逻辑错误，答运行时崩溃选 D
- 以为编译器只给警告，仍能生成可执行文件

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 07 指针
