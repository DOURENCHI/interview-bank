---
id: Q-1649
title: 这段 C++ 代码输出什么？（29 序列容器 · 第 37 题）
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

reserve 只改 capacity、不构造元素，size 仍由实际元素决定；它保证 capacity 不小于 n，传比当前小的值时不会缩容。提前 reserve 能避免多次重新分配搬移，也让迭代器在容量范围内保持有效。resize 才真正改变 size 并对新增元素值初始化；shrink_to_fit 才是收缩请求。

## 高频追问

1. **为什么 size 还是 3？** —— reserve 只申请内存，不添加元素，size 统计的是已构造元素个数。
2. **capacity 怎么到 100 的？** —— reserve(100) 一次分配至少容纳 100 个 int 的缓冲，capacity 变成 100。
3. **reserve 和 resize 差在哪？** —— reserve 不动 size，v[50] 仍是越界 UB；resize(100) 会把 size 改成 100 并补 0，可直接下标访问。

## 易错点

- 把 reserve 当 resize，答 100 100 选 B
- 以为 reserve 无效，答 3 3 选 C
- reserve 后直接访问 v[50]，越界未定义行为

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 29 序列容器
