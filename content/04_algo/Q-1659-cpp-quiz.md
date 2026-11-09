---
id: Q-1659
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 47 题）
module: 04_algo
sub: C++语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/C++实验台/C++考点实验台.html
verified_at: 2026-11-09
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 31 STL 算法
