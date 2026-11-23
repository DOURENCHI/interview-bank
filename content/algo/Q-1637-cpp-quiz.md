---
id: Q-1637
title: 这段 C++ 代码输出什么？（18 虚函数 · 第 25 题）
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
struct A { virtual void g() { cout << "A"; } };
struct B : A { void g() { cout << "B"; } };
int main() {
    B b;
    A a = b;
    A &r = b;
    a.g(); r.g();
}
```

- **A.** AA
- **B.** AB
- **C.** BA
- **D.** BB

## 口述答案

答案是 **B. AB**，实际输出 `AB`。

A a = b 发生对象切片，a 就是一个 A；引用 r 绑定的仍是 B 对象，虚函数按真实类型调用。

## 讲深一层

A a = b 发生对象切片：只把 b 的基类子对象拷进 a，a 的 vptr 是 A 的，虚调用落到 A::g。引用 r 不拷贝，仍绑定 b 本体，虚调用按真实类型走 B::g。值传递 void f(A a) 同样会切片；用 A& 或 A* 传参才能保住多态。切片是 C++ 里最隐蔽的多态失效方式。

## 高频追问

1. **为什么 a.g() 输出 A？** —— a 是独立构造的 A 对象，切片后连虚表指针都是 A 的，动态类型就是 A。
2. **为什么 r.g() 输出 B？** —— 引用只是别名，没有产生新对象，r 的动态类型仍是 B。
3. **怎么避免切片？** —— 多态传参用 A& 或 A*，容器存 unique_ptr<A>；禁止按值传递带虚函数的基类。

## 易错点

- 认为 a 仍指向 b 的数据，答 BB 选 D
- 把引用也当拷贝，答 AA 选 A
- 以为切片只丢派生类成员、虚函数仍生效

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 18 虚函数
