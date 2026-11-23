---
id: Q-1653
title: 这段 C++ 代码输出什么？（30 关联容器与适配器 · 第 41 题）
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
set<int> s{3,1,2,1};
for (int x : s) cout << x;
```

- **A.** 123
- **B.** 3121
- **C.** 312
- **D.** 1213

## 口述答案

答案是 **A. 123**，实际输出 `123`。

set 底层是红黑树：自动按键排序并去重，重复插入的 1 被忽略，遍历得升序 123。要保留重复键用 multiset。

## 讲深一层

set 底层是红黑树，插入时自动按 operator< 排序并去重，重复的 1 被直接丢弃；遍历是中序遍历，得升序 123。元素在容器内是 const 的，不能通过迭代器修改（会破坏树序），要改只能 erase 后重插。multiset 保留重复键，unordered_set 无序但平均 O(1)。

## 高频追问

1. **重复的 1 去哪了？** —— set 键唯一，第二次 insert 返回 pair<iterator,false>，元素不插入。
2. **为什么是升序？** —— 红黑树中序遍历天然按比较器递增输出，与插入顺序无关。
3. **能修改元素值吗？** —— 不能，set 的 iterator 实际是 const_iterator；要改只能先删再插。

## 易错点

- 当普通数组处理，答 3121 选 B
- 只去重不排序，答 312 选 C
- 用 s[0] 下标访问 set，编译错误

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 30 关联容器与适配器
