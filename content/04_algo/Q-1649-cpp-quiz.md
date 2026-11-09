---
id: Q-1649
title: 这段 C++ 代码输出什么？（29 序列容器 · 第 37 题）
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
vector<int> v{1,2,3};
v.reserve(100);
cout << v.size() << " " << v.capacity();
```

- **A.** 3 100
- **B.** 100 100
- **C.** 3 3
- **D.** 100 3

## 口述答案

答案是 **A. 3 100**，实际输出 `3 100`。

reserve 只预留容量、不改变 size；提前知道元素个数可以避免多次扩容与迭代器失效。resize 才会改变 size。

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
