---
id: Q-1667
title: 这段 C++ 代码输出什么？（35 chrono 与时间 · 第 55 题）
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
auto d = chrono::milliseconds(1500);
cout << chrono::duration_cast<chrono::seconds>(d).count()
     << " " << d.count();
```

- **A.** 1 1500
- **B.** 1.5 1500
- **C.** 2 1500
- **D.** 1500 1

## 口述答案

答案是 **A. 1 1500**，实际输出 `1 1500`。

duration_cast 从细粒度向粗粒度转换时向零截断，1500ms 变 1 秒；原 duration 的 count() 仍以毫秒为单位，是 1500。类型里带着单位，不会把秒和毫秒混用。

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

`教学文档/C++实验台/C++考点实验台.html` · 35 chrono 与时间
