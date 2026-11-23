---
id: Q-1658
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 46 题）
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

transform 的一元版本对 [first,last) 每个元素调用操作，把结果写到 result，返回输出区间的尾后迭代器。输入输出区间可以相同（就地修改），因为逐元素独立覆盖；但若两区间部分重叠且错位，行为未定义。二元版本另有第二个输入区间，共五个参数。

## 高频追问

1. **为什么输出连成 246？** —— 每个元素翻倍后没有输出分隔符，cout 连续打印成 246 而不是 2 4 6。
2. **就地修改合法吗？** —— 合法，result 等于 first 时逐个覆盖，读写的都是当前元素，互不干扰。
3. **想输出到新容器怎么办？** —— 用 back_inserter(v2) 作输出迭代器自动扩容；直接给空容器 begin() 会越界写。

## 易错点

- 以为有空格，答 2 4 6 选 D
- 以为写回自身会读到已翻倍的值，答 4 8 12
- 对空 vector 的 begin() 写入，未定义行为

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 31 STL 算法
