---
id: Q-1651
title: 这段 C++ 代码输出什么？（29 序列容器 · 第 38 题）
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
vector<int> v(5);
v.reserve(100);
vector<int>(v).swap(v);
cout << v.size() << " " << v.capacity();
```

- **A.** 5 5
- **B.** 5 100
- **C.** 100 5
- **D.** 0 0

## 口述答案

答案是 **A. 5 5**，实际输出 `5 5`。

用拷贝构造出的临时 vector（容量紧贴 size）与原容器交换，临时对象析构时带走那块大内存；size 仍是 5，容量收缩到 5。C++11 起也可写 v.shrink_to_fit()，但只是非强制建议。

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

`教学文档/C++实验台/C++考点实验台.html` · 29 序列容器
