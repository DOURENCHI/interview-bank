---
id: Q-1662
title: 这段 C++ 代码输出什么？（32 函数对象与谓词 · 第 50 题）
module: algo
sub: 模板与 STL
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/C++实验台/C++考点实验台.html
verified_at: 2026-11-21
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

greater<int> 是模板类，greater<int>() 构造临时对象，g(3,5) 调的是它的 operator()，语义就是 a > b。把它作为 sort 的第三参数即得降序。比较器必须满足严格弱序：comp(a,a) 必须为 false，所以不能写 >= 或 <=，否则划分逻辑失效。

## 高频追问

1. **为什么是 0 1？** —— 3 > 5 为假输出 0，5 > 3 为真输出 1。
2. **怎么用它降序排序？** —— sort(v.begin(), v.end(), greater<int>())，等价于传一个 a > b 的 lambda。
3. **为什么不能写 >=？** —— 违反严格弱序（comp(a,a) 为真），sort 内部划分可能越界或死循环。

## 易错点

- 把两次比较顺序看反，答 1 0 选 B
- 把 greater 当函数名而非模板类，漏写 ()
- 用 >= 作比较器导致运行时崩溃

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 32 函数对象与谓词
