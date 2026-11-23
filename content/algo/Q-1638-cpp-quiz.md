---
id: Q-1638
title: 这段 C++ 代码输出什么？（18 虚析构 · 第 26 题）
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
struct B { ~B() { cout << "~B"; } };
struct D : B { ~D() { cout << "~D"; } };
int main() {
    B *p = new D;
    delete p;
}
```

- **A.** ~B
- **B.** ~D~B
- **C.** ~B~D
- **D.** ~D

## 口述答案

答案是 **A. ~B**，实际输出 `~B`。

基类析构函数不是虚函数，通过基类指针 delete 只调用 ~B，~D 没执行。改成 virtual ~B() 才会输出 ~D~B。

## 讲深一层

基类析构不是虚函数，delete p 只按静态类型 B* 调 ~B，D 的析构根本不执行，派生类持有的资源泄漏，标准上这属未定义行为。加上 virtual ~B() 才会输出 ~D~B。规则很硬：类只要可能被基类指针多态 delete，析构就必须 virtual。纯虚析构同样要写函数体。

## 高频追问

1. **为什么只输出 ~B？** —— delete 依据指针的静态类型选析构函数，B 的析构非虚，编译器直接定址 ~B，不查 vtable。
2. **改成 virtual 呢？** —— 输出 ~D~B，先析构派生部分再析构基类部分，顺序与构造相反。
3. **纯虚析构怎么写？** —— 声明 virtual ~B() = 0; 但必须给出类外定义 ~B() {}，否则链接期报未定义符号。

## 易错点

- 以为 delete 会自动识别真实类型，答 ~D~B 选 B
- 认为先析构基类，答 ~B~D 选 C
- 以为析构非虚只影响性能，答 ~D 选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 18 虚析构
