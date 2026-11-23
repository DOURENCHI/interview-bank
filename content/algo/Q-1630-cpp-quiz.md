---
id: Q-1630
title: 这段 C++ 代码输出什么？（11 类与对象 · 第 18 题）
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
class A { int x; };
int main() {
    A a;
    a.x = 1;
}
```

- **A.** 编译错误
- **B.** 什么都不输出
- **C.** 1
- **D.** 运行时崩溃

## 口述答案

答案是 **A. 编译错误**，实际输出 `编译错误`。

class 的成员默认是 private，类外不能访问；改成 struct 就可以。

## 讲深一层

class 的默认访问权限是 private，默认继承方式也是 private；struct 两者都是 public。所以类外写 a.x 直接编译失败，与运行期无关。加上 public: 就能通过，程序不输出任何东西。另外空类 sizeof 为 1，编译器要保证不同对象地址唯一。

## 高频追问

1. **为什么编译不过？** —— x 在 class 中默认 private，main 是类外代码，无权访问私有成员。
2. **改成 struct 呢？** —— 默认 public，a.x = 1 合法；程序没有输出语句，所以什么都不打印。
3. **class 和 struct 还有别的差别吗？** —— 只剩默认访问权限和默认继承权限；template<class T> 与 template<typename T> 完全等价。

## 易错点

- 以为能访问，答输出 1 选 C
- 以为只是未初始化，答运行时崩溃选 D
- 以为 class 成员默认 public，判程序正常

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 11 类与对象
