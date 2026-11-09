---
id: Q-1658
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 46 题）
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
transform(v.begin(), v.end(), v.begin(),
  [](int x){ return x * 2; });
for (int x : v) cout << x;
```

- **A.** 246
- **B.** 123
- **C.** 235
- **D.** 2 4 6

## 口述答案

答案是 **A. 246**，实际输出 `246`。

transform 对每个元素应用一元操作并写到目标区间，这里就地翻倍成 2 4 6；输出时没有空格，所以连成 246。输入输出区间可以相同。

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

`教学文档/C++实验台/C++考点实验台.html` · 31 STL 算法
