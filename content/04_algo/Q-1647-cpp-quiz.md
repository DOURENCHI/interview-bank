---
id: Q-1647
title: 这段 C++ 代码输出什么？（28 迭代器与 string · 第 34 题）
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
string s = "hello@sina.com";
cout << s.substr(0, s.find('@'));
```

- **A.** hello
- **B.** hello@
- **C.** hello@sina.com
- **D.** 编译错误

## 口述答案

答案是 **A. hello**，实际输出 `hello`。

find 返回 '@' 的下标 5；substr(0, 5) 的第二个参数是长度、不是结束下标，所以取前 5 个字符。find 找不到时返回 string::npos，不能当下标用。

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

`教学文档/C++实验台/C++考点实验台.html` · 28 迭代器与 string
