---
id: Q-1657
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 45 题）
module: 04_algo
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
vector<int> v{1,2,3,4};
cout << count_if(v.begin(), v.end(),
  [](int x){ return x % 2 == 0; });
```

- **A.** 2
- **B.** 3
- **C.** 1
- **D.** 4

## 口述答案

答案是 **A. 2**，实际输出 `2`。

count_if 统计使谓词为 true 的元素：1 2 3 4 里偶数只有 2 和 4，共 2 个。谓词可以是 lambda、函数对象或普通函数。

## 讲深一层

count_if(区间, 一元谓词) 统计谓词为真的元素个数，谓词按值拷贝一份持有，所以带状态的函数对象改的是副本。谓词应当无副作用，并对每个元素返回可转 bool 的值。普通 count 只能做等值统计，凡是按条件筛选就必须用 count_if。二者返回的都是 difference_type。

## 高频追问

1. **数出来是哪几个？** —— 2 和 4 满足偶数条件，1 和 3 是奇数被排除，共 2 个。
2. **谓词能带状态吗？** —— 能，但会被拷贝；想回传计数需用 std::ref 包装，或改用 for_each 在外部累加。
3. **count 和 count_if 怎么选？** —— 判断「等于某个值」用 count，判断「满足条件」用 count_if。

## 易错点

- 谓词写成 x % 2 == 1，数出 3
- 以为谓词副本能改外部计数器，结果仍是 0
- 谓词返回 int 且取值非 0/1，误以为被截断

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 31 STL 算法
