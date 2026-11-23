---
id: Q-1659
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 47 题）
module: algo
sub: 模板与 STL
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
vector<int> v{1,3,3,3,5};
cout << lower_bound(v.begin(),v.end(),3)-v.begin()
     << " " << upper_bound(v.begin(),v.end(),3)-v.begin();
```

- **A.** 1 4
- **B.** 1 3
- **C.** 2 4
- **D.** 3 4

## 口述答案

答案是 **A. 1 4**，实际输出 `1 4`。

lower_bound 返回第一个「不小于 3」的位置 1，upper_bound 返回第一个「大于 3」的位置 4；相减就是相等元素个数 3。前提是区间已排序，复杂度 O(log n)。

## 讲深一层

lower_bound 返回第一个不小于 x 的位置（>=），upper_bound 返回第一个大于 x 的位置（>），二者夹出的 [lb, ub) 正好是所有等于 x 的元素，相减即个数 3。前提是区间已按同一比较器有序，否则结果无意义。对随机访问迭代器是 O(log n) 次比较，对 forward 迭代器会退化成 O(n) 次移动。

## 高频追问

1. **为什么是 1 和 4？** —— 3 从下标 1 开始连续出现到下标 3，第一个大于 3 的是下标 4 的 5。
2. **相减得到什么？** —— 3，即等于 3 的元素个数；equal_range 一次就能拿到这对边界。
3. **没排序会怎样？** —— 二分的前提被破坏，返回值未定义，可能落在任意位置。

## 易错点

- 把 upper_bound 当最后一个相等元素，答 1 3 选 B
- 以为 lower_bound 返回「等于」的位置，答 3 4 选 D
- 对未排序区间调用，结果时对时错却以为稳定

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 31 STL 算法
