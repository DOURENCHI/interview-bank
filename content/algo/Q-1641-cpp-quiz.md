---
id: Q-1641
title: 这段 C++ 代码输出什么？（21 STL 容器 · 第 29 题）
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
map<string, int> m;
m["b"] = 2;
m["a"] = 1;
int z = m["c"];
for (auto &p : m) cout << p.first;
```

- **A.** ba
- **B.** ab
- **C.** abc
- **D.** bac

## 口述答案

答案是 **C. abc**，实际输出 `abc`。

map 按键排序；用 [] 读一个不存在的键会自动插入它（值为 0）。

## 讲深一层

map 底层是红黑树，按键的 operator< 保持有序，遍历得升序 ab；unordered_map 是哈希表，遍历顺序不确定，不能依赖。m["c"] 用的是非 const 的 operator[]，键不存在就插入一个值初始化的 0，所以 c 也被打印。只想查询应改用 find、at 或 count。

## 高频追问

1. **为什么 c 也会被打印？** —— int z = m["c"] 触发了插入，map 里多了键 c（值 0），遍历自然是 abc。
2. **换成 unordered_map 呢？** —— 输出顺序由哈希和桶决定，可能是 bac、cba 等，同一程序不同版本都可能不同。
3. **怎么只查不插入？** —— 用 m.find("c") != m.end()，或 m.count()，或 m.at()（不存在抛 out_of_range）。

## 易错点

- 漏掉 [] 的插入副作用，答 ba 选 A
- 以为按插入顺序遍历，答 bac 选 D
- 用 m.at("c") 读不存在的键，抛异常而不是插入 0

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 21 STL 容器
