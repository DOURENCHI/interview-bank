---
id: Q-1634
title: 这段 C++ 代码输出什么？（16 继承 · 第 22 题）
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
struct B { B() { cout << "B"; } ~B() { cout << "b"; } };
struct M { M() { cout << "M"; } ~M() { cout << "m"; } };
struct D : B {
    M m;
    D() { cout << "D"; }
    ~D() { cout << "d"; }
};
int main() { D d; }
```

- **A.** BMDdmb
- **B.** DMBbmd
- **C.** MBDdbm
- **D.** BMDbmd

## 口述答案

答案是 **A. BMDdmb**，实际输出 `BMDdmb`。

构造：基类 → 成员 → 自己；析构顺序正好相反。

## 讲深一层

构造顺序固定为：基类 → 成员 → 自身，其中成员严格按声明顺序，与初始化列表的书写顺序无关；析构顺序完全相反。有虚基类时虚基类最先构造。所以这里 B、M、D 依次输出，销毁时 d、m、b 依次输出。初始化列表顺序写反只触发 -Wreorder 警告，不改变实际顺序。

## 高频追问

1. **构造顺序是什么？** —— B（基类）→ M（成员 m）→ D（自身构造体），输出 BMD。
2. **析构顺序呢？** —— d → m → b，即 ~D、~M、~B，输出 dmb。
3. **初始化列表写反有影响吗？** —— 没有，成员始终按类内声明顺序构造；但书写顺序与声明不一致时编译器会警告，容易误导读者。

## 易错点

- 以为派生类构造体先跑，答 DMB 选 B
- 析构按正序写，答 BMDbmd 选 D
- 认为成员按初始化列表顺序构造，多成员时会排错

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 16 继承
