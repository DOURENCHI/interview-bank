---
id: Q-1626
title: 这段 C++ 代码输出什么？（08 引用 · 第 14 题）
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
void f(int x, int &y) { x = 9; y = 9; }
int main() {
    int a = 1, b = 1;
    f(a, b);
    cout << a << b;
}
```

- **A.** 11
- **B.** 19
- **C.** 91
- **D.** 99

## 口述答案

答案是 **B. 19**，实际输出 `19`。

按值传参改的是副本，a 不变；按引用传参改的就是 b 本身。

## 讲深一层

引用是已存在对象的别名，不产生拷贝，函数内改的就是实参；值传递拷贝副本，改副本不影响调用方。指针版 void f(int*, int&) 效果相同，只是要多写解引用。注意 f(int) 与 f(int&) 无法共存出可用重载——对非 const 左值调用会产生二义；非 const 引用也不能绑字面量。

## 高频追问

1. **a 为什么不变？** —— 形参 x 是 a 的副本，x=9 只改栈上那份拷贝，函数返回即销毁。
2. **b 为什么变成 9？** —— y 是 int&，绑定到 b 本身，对 y 赋值就是对 b 赋值，没有副本参与。
3. **f(1, 2) 能调用吗？** —— 不能，非 const 引用不能绑定字面量这类右值；改成 const int& 才能接收，但那样也改不了实参。

## 易错点

- 认为引用也拷贝一份，答 99 选 D
- 只记住值传递，答 11 选 A
- 把参数顺序搞反，答 91 选 C

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 08 引用
