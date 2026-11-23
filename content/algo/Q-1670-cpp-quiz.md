---
id: Q-1670
title: 这段 C++ 代码输出什么？（36 智能指针与移动语义 · 第 58 题）
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
string s = "hello";
string t = std::move(s);
cout << t.size() << " " << s.size();
```

- **A.** 5 0
- **B.** 5 5
- **C.** 0 5
- **D.** 编译错误

## 口述答案

答案是 **A. 5 0**，实际输出 `5 0`。

std::move 只做类型转换、不移动任何东西；移动构造把资源转给 t。被 move 后的 s 处于「有效但未指定」状态，本机 libstdc++ 实测 size() 为 0，其他实现可能不同——不要再读它的值，但可以重新赋值或析构。

## 讲深一层

std::move 只是把左值 static_cast 成右值引用，本身一个字节都不搬；真正的转移发生在移动构造里，string 通常直接接管内部指针，源被置空。标准只保证被移动后「有效但未指定」，size() 为 0 是 libstdc++ 的实现行为，其他库可能不同。可以重新赋值或析构，但不要读它的值。

## 高频追问

1. **t 为什么是 5？** —— 移动构造把 s 的缓冲区指针直接交给 t，t 接管了原内容。
2. **s 为什么是 0？** —— 资源被偷走后 s 被置成空串，这是 libstdc++ 的实现；标准不保证具体值。
3. **move 真的会移动吗？** —— 不会，它只是类型转换。对 int 这类平凡类型，移动构造等同拷贝，源值不变。

## 易错点

- 以为 move 是拷贝，答 5 5 选 B
- 把 t 和 s 的输出顺序看反，答 0 5 选 C
- 依赖 s.size() == 0 写跨平台逻辑，换实现就错

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 36 智能指针与移动语义
