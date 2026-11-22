---
id: Q-1636
title: 这段 C++ 代码输出什么？（18 虚函数 · 第 24 题）
module: 04_algo
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
struct A {
    void f() { cout << "A"; }
    virtual void g() { cout << "A"; }
};
struct B : A {
    void f() { cout << "B"; }
    void g() { cout << "B"; }
};
int main() {
    B b;
    A *p = &b;
    p->f(); p->g();
}
```

- **A.** AA
- **B.** AB
- **C.** BA
- **D.** BB

## 口述答案

答案是 **B. AB**，实际输出 `AB`。

f 不是虚函数，按指针类型 A* 调用；g 是虚函数，按对象的真实类型 B 调用。

## 讲深一层

非虚函数静态绑定，按指针或引用的静态类型选函数；虚函数动态绑定，按对象的真实类型选。这里 p 是 A*，p->f() 调 A::f，p->g() 走 vtable 调 B::g。注意名字隐藏：B::f 会遮蔽 A::f 的所有重载，通过 B 对象也只能看到 B::f。给 f 加 virtual 就输出 BB。

## 高频追问

1. **为什么 f 输出 A？** —— f 不是虚函数，编译器按 p 的静态类型 A* 直接定址 A::f，与对象真实类型无关。
2. **为什么 g 输出 B？** —— g 是虚函数，通过 vptr 在运行时查到 B::g，即使指针类型是 A*。
3. **如果 B 里再加一个 f(int) 呢？** —— 会遮蔽 A::f()，b.f() 报参数不匹配；要保留基类重载得写 using A::f;。

## 易错点

- 以为都按真实类型调用，答 BB 选 D
- 以为都按指针类型调用，答 AA 选 A
- 混淆覆盖与重载，认为参数不同也算 override

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 18 虚函数
