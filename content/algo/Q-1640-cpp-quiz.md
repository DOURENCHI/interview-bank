---
id: Q-1640
title: 这段 C++ 代码输出什么？（21 STL 容器 · 第 28 题）
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
vector<int> v = {3, 1, 4};
v.pop_back();
v.push_back(9);
cout << v.size() << v[2];
```

- **A.** 39
- **B.** 34
- **C.** 49
- **D.** 24

## 口述答案

答案是 **A. 39**，实际输出 `39`。

pop_back 删掉 4，push_back 在末尾加上 9：v = {3, 1, 9}。

## 讲深一层

pop_back 只销毁末尾元素，不改 capacity；push_back 在尾部追加，仅在容量不足时按倍数重新分配并搬移全部元素，那会让所有迭代器和引用失效。size 是元素个数，capacity 是已分配容量，两者不同。v[2] 是不做越界检查的下标访问。这里最终是 {3, 1, 9}。

## 高频追问

1. **v 最后装了什么？** —— pop_back 删掉 4 得 {3,1}，push_back(9) 追加成 {3,1,9}。
2. **size 为什么是 3？** —— 先减一后加一，元素个数回到 3。
3. **capacity 会变吗？** —— pop_back 不缩容；push_back 时若容量已满通常翻倍（实现相关），此前保存的迭代器全部失效。

## 易错点

- 以为 pop_back 删的是首元素，答 34 选 B
- 以为 push_back 后下标从 0 重排，答 24
- 以为 pop_back 会返回被删的值，写成 int x = v.pop_back()

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 21 STL 容器
