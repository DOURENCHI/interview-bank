---
id: Q-1643
title: 这段 C++ 代码输出什么？（23 流 · 第 31 题）
module: algo
sub: 语法与陷阱
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
cout << fixed << setprecision(2) << 3.14159 << " ";
cout << setw(4) << setfill('*') << 7 << 7;
```

- **A.** 3.14 ***77
- **B.** 3.14 ***7***7
- **C.** 3.1 ***77
- **D.** 3.14 7***7

## 口述答案

答案是 **A. 3.14 ***77**，实际输出 `3.14 ***77`。

fixed 下 setprecision(2) 是两位小数；setw 只对紧跟的下一项有效，所以第二个 7 不再补齐。

## 讲深一层

setw 只作用于紧随其后的一个输出项，且只补不截：内容比宽度长就原样输出。setfill 一旦设置就持续有效，默认填充空格、默认右对齐。fixed 加 setprecision(2) 表示小数点后两位；不带 fixed 时 precision 是有效数字总位数。所以第二个 7 没有星号，直接接在后面。

## 高频追问

1. **为什么第二个 7 没被补齐？** —— setw 是一次性的，只对下一个 7 生效，之后恢复默认宽度。
2. **fixed 起什么作用？** —— 让 setprecision 的语义从「有效数字位数」变成「小数点后位数」，3.14159 才稳定得 3.14。
3. **想两个都补齐怎么写？** —— 每个数前都写一次 setw(4)，例如 setw(4) << 7 << setw(4) << 7。

## 易错点

- 以为 setw 持续生效，答 ***7***7 选 B
- 不带 fixed 只用 setprecision(2)，答 3.1 选 C
- 以为默认左对齐，答 7***7 选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 23 流
