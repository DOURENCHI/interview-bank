---
id: Q-1642
title: 这段 C++ 代码输出什么？（21 STL 容器 · 第 29 题）
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
map<string, int> m;
m["b"] = 2;
m["a"] = 1;
int z = m["c"];
for (auto &p : m) cout << p.first;
```

- **A.** ba
- **B.** ab
- **C.** abc
- **D.** bac

## 口述答案

答案是 **C. abc**，实际输出 `abc`。

map 按键排序；用 [] 读一个不存在的键会自动插入它（值为 0）。

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

`教学文档/C++实验台/C++考点实验台.html` · 21 STL 容器
