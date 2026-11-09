---
id: Q-1643
title: 这段 C++ 代码输出什么？（23 流 · 第 31 题）
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 23 流
