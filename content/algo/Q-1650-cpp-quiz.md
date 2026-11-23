---
id: Q-1650
title: 这段 C++ 代码输出什么？（29 序列容器 · 第 38 题）
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
vector<int> v(5);
v.reserve(100);
vector<int>(v).swap(v);
cout << v.size() << " " << v.capacity();
```

- **A.** 5 5
- **B.** 5 100
- **C.** 100 5
- **D.** 0 0

## 口述答案

答案是 **A. 5 5**，实际输出 `5 5`。

用拷贝构造出的临时 vector（容量紧贴 size）与原容器交换，临时对象析构时带走那块大内存；size 仍是 5，容量收缩到 5。C++11 起也可写 v.shrink_to_fit()，但只是非强制建议。

## 讲深一层

vector<int>(v) 用拷贝构造出一个临时对象，容量紧贴 size（通常恰好 5）；swap 只交换指针与 size/capacity 这组三元组，O(1)、不搬元素；临时对象析构时带走原来那块 100 的缓冲。C++11 的 shrink_to_fit 只是非强制请求，实现可以忽略。这就是经典的 shrink-to-fit 惯用法。

## 高频追问

1. **容量为什么缩到 5？** —— 临时对象按 size 精确分配，交换后 v 拿到这块小缓冲，大缓冲随临时对象析构释放。
2. **swap 为什么是 O(1)？** —— 只交换三个指针/整数字段，元素一个都不搬；allocator 相同时还是 noexcept。
3. **shrink_to_fit 一定生效吗？** —— 不保证，标准只说「可能」减少容量；要确定性效果就用 swap 惯用法。

## 易错点

- 以为 reserve 的容量会保留，答 5 100 选 B
- 把 size 和 capacity 顺序看反，答 100 5 选 C
- 以为 v 被换成了空容器，答 0 0 选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 29 序列容器
