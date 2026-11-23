---
id: Q-1652
title: 这段 C++ 代码输出什么？（29 序列容器 · 第 40 题）
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
deque<int> d{2,3};
d.push_front(1); d.push_back(4);
for (int x : d) cout << x;
```

- **A.** 1234
- **B.** 2134
- **C.** 2341
- **D.** 1324

## 口述答案

答案是 **A. 1234**，实际输出 `1234`。

deque 两头插入都是 O(1)：push_front(1) 放到最前，push_back(4) 追加到最后，遍历得 1234。vector 没有 push_front。

## 讲深一层

deque 是分段连续缓冲加中控数组，两端插入都是 O(1)，且不需要像 vector 那样整体搬移；头插不会让已有元素的引用失效（迭代器会失效）。vector 根本没有 push_front，头插只能 insert(begin(), x)，代价 O(n)。deque 的短板是中间插入比 vector 慢，随机访问多一次间接寻址。

## 高频追问

1. **为什么是 1234？** —— push_front(1) 放到最前，push_back(4) 追加到最后，原顺序 2、3 不动。
2. **deque 和 vector 怎么选？** —— 需要两端进出用 deque；只在尾部增长、要求连续内存和最快随机访问用 vector。
3. **还有 O(1) 头插的容器吗？** —— list 和 forward_list 也可以，但失去随机访问，遍历缓存不友好；实践中多选 deque。

## 易错点

- 以为 push_front 会追加到末尾，答 2134 选 B
- 把 push_front 当成覆盖首元素，答 1324
- 对 vector 写 push_front，编译报无此成员

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 29 序列容器
