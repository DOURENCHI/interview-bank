---
id: Q-1632
title: 这段 C++ 代码输出什么？（13 拷贝构造 · 第 20 题）
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
struct P {
    P() {}
    P(const P &) { cout << "K"; }
};
void f(P p) {}
int main() {
    P a;
    P b = a;
    f(a);
    b = a;
    cout << "|";
}
```

- **A.** KK|
- **B.** KKK|
- **C.** K|
- **D.** KKKK|

## 口述答案

答案是 **A. KK|**，实际输出 `KK|`。

P b = a 和按值传参各调用一次拷贝构造；b = a 是赋值运算符，不是拷贝构造。

## 讲深一层

拷贝构造只在「用已有对象初始化新对象」时调用；b = a 时 b 已构造完成，走的是拷贝赋值 operator=，隐式版本逐成员赋值、不打印 K。按值传参 f(a) 会再拷贝一次。若把 f 改成 f(P&)，就只剩 P b = a 这一次，输出 K|；返回值还可能被 RVO 省略掉一次拷贝。

## 高频追问

1. **哪两处调了拷贝构造？** —— P b = a 的初始化，以及 f(a) 的按值传参，各触发一次，输出两个 K。
2. **为什么 b = a 不算？** —— b 早已构造完成，这是赋值运算，调用隐式 operator=，它不打印任何东西。
3. **加个移动构造会变吗？** —— f(a) 传的是左值，仍走拷贝构造；只有 f(std::move(a)) 才会匹配 P(P&&)。

## 易错点

- 把赋值也算成拷贝构造，答 KKK| 选 B
- 认为传参是引用，答 K| 选 C
- 把 P b = a 当赋值，答 K|

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 13 拷贝构造
