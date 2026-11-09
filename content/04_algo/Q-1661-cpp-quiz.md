---
id: Q-1661
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 48 题）
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
