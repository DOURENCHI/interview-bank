---
id: Q-1657
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 44 题）
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
int a[5] = {5,2,9,1,6};
cout << accumulate(a, a+5, 0);
```

- **A.** 23
- **B.** 22
- **C.** 24
- **D.** 编译错误

## 口述答案

答案是 **A. 23**，实际输出 `23`。

accumulate 在 <numeric> 里，按左闭右开区间从初值 0 开始累加，得 23。初值写成 0.0 就会按 double 累加，类型由初值决定。

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
