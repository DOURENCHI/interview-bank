---
id: Q-1673
title: 这段 C++ 代码输出什么？（37 流与字符串处理 · 第 60 题）
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
cout << setw(6) << setfill('0') << 42
     << " " << fixed << setprecision(2) << 3.14159;
```

- **A.** 000042 3.14
- **B.** 42 3.14
- **C.** 000042 3.14159
- **D.** 00042 3.14

## 口述答案

答案是 **A. 000042 3.14**，实际输出 `000042 3.14`。

setw(6) + setfill('0') 补成 6 位得 000042；fixed 配合 setprecision(2) 是小数点后 2 位，得 3.14（不加 fixed 则是 2 位有效数字 3.1）。setw 只对下一项有效，setfill / fixed / precision 持续有效。

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

`教学文档/C++实验台/C++考点实验台.html` · 37 流与字符串处理
