---
id: Q-1619
title: 这段 C++ 代码输出什么？（03 类型 · 第 6 题）
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
cout << 012 + 0x1F;
```

- **A.** 43
- **B.** 41
- **C.** 12
- **D.** 13

## 口述答案

答案是 **B. 41**，实际输出 `41`。

0 开头是八进制：012 = 10；0x1F = 31；和为 41。

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

`教学文档/C++实验台/C++考点实验台.html` · 03 类型
