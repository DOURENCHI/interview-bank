---
id: Q-1670
title: 这段 C++ 代码输出什么？（36 智能指针与移动语义 · 第 58 题）
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
string s = "hello";
string t = std::move(s);
cout << t.size() << " " << s.size();
```

- **A.** 5 0
- **B.** 5 5
- **C.** 0 5
- **D.** 编译错误

## 口述答案

答案是 **A. 5 0**，实际输出 `5 0`。

std::move 只做类型转换、不移动任何东西；移动构造把资源转给 t。被 move 后的 s 处于「有效但未指定」状态，本机 libstdc++ 实测 size() 为 0，其他实现可能不同——不要再读它的值，但可以重新赋值或析构。

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

`教学文档/C++实验台/C++考点实验台.html` · 36 智能指针与移动语义
