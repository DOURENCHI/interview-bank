---
id: Q-1664
title: 这段 C++ 代码输出什么？（33 lambda 与绑定 · 第 51 题）
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
int x = 1;
auto f = [x]{ return x; };
auto g = [&x]{ return x; };
x = 9;
cout << f() << " " << g();
```

- **A.** 1 9
- **B.** 9 9
- **C.** 1 1
- **D.** 9 1

## 口述答案

答案是 **A. 1 9**，实际输出 `1 9`。

[x] 按值捕获，在创建时拷贝一份，之后 x 改成 9 也不影响 f；[&x] 按引用捕获，g 看到的是修改后的 9。按引用捕获要保证 lambda 执行时变量还活着。

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
