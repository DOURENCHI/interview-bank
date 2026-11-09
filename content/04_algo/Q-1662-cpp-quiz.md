---
id: Q-1662
title: 这段 C++ 代码输出什么？（32 函数对象与谓词 · 第 50 题）
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
greater<int> g;
cout << g(3,5) << " " << g(5,3);
```

- **A.** 0 1
- **B.** 1 0
- **C.** 1 1
- **D.** 0 0

## 口述答案

答案是 **A. 0 1**，实际输出 `0 1`。

greater<int>()(a,b) 等价于 a > b：3>5 为假输出 0，5>3 为真输出 1。把它作为第三参数传给 sort 就是降序。谓词比较函数必须满足严格弱序，不能写 >=。

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

`教学文档/C++实验台/C++考点实验台.html` · 32 函数对象与谓词
