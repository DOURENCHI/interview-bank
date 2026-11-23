---
id: Q-1660
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 48 题）
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
int a[4] = {3,1,4,2};
sort(a, a+4);
cout << binary_search(a,a+4,3) << " "
     << binary_search(a,a+4,5);
```

- **A.** 1 0
- **B.** 0 1
- **C.** 1 1
- **D.** 0 0

## 口述答案

答案是 **A. 1 0**，实际输出 `1 0`。

binary_search 只回答「是否存在」，返回 bool（输出 1 / 0），不返回位置；必须先排序，否则结果无意义。要位置用 lower_bound。

## 讲深一层

binary_search 只回答「是否存在」，返回 bool，内部用 lower_bound 判等，拿不到任何位置信息。必须先按同一比较器有序，否则结果未定义——不是稳定地返回 0。要位置用 lower_bound 或 equal_range，要个数用上界减下界。复杂度是对数级比较次数。

## 高频追问

1. **为什么是 1 0？** —— sort 后为 1 2 3 4，3 存在得 true 输出 1，5 不存在得 false 输出 0。
2. **能拿到下标吗？** —— 不能，binary_search 只返回 bool；要下标就 lower_bound(a, a+4, 3) - a。
3. **不排序会怎样？** —— 未定义行为，可能把存在的值判成不存在，不能当兜底手段。

## 易错点

- 以为找不到返回 -1，转 bool 为真，答 1 1 选 C
- 忘记先排序，答 0 0 选 D
- 把返回值当下标用，直接越界访问

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 31 STL 算法
