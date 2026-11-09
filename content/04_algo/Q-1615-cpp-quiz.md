---
id: Q-1615
title: 这段 C++ 代码输出什么？（04 运算符 · 第 2 题）
module: 04_algo
sub: C++语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
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
int x = 5;
int y = x++ * 2;
cout << y << " " << x;
```

- **A.** 10 6
- **B.** 12 6
- **C.** 10 5
- **D.** 12 5

## 口述答案

答案是 **A. 10 6**，实际输出 `10 6`。

后置 ++ 先用旧值 5 参与运算，再把 x 加到 6。

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

`教学文档/C++实验台/C++考点实验台.html` · 04 运算符
