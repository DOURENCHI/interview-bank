---
id: Q-1665
title: 这段 C++ 代码输出什么？（33 lambda 与绑定 · 第 52 题）
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
auto f = [](int a, int b){ return a > b ? a : b; };
cout << f(3, 7);
```

- **A.** 7
- **B.** 3
- **C.** 10
- **D.** 编译错误

## 口述答案

答案是 **A. 7**，实际输出 `7`。

lambda 的三段是 [] 捕获列表、() 参数、{} 函数体；这里返回两数较大者 7。[] 空捕获表示不使用外部局部变量。

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

`教学文档/C++实验台/C++考点实验台.html` · 33 lambda 与绑定
