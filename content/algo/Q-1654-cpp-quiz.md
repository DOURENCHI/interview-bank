---
id: Q-1654
title: 这段 C++ 代码输出什么？（30 关联容器与适配器 · 第 42 题）
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
map<string,int> m;
cout << m["x"] << " " << m.size();
```

- **A.** 0 1
- **B.** 0 0
- **C.** 随机值 1
- **D.** 编译错误

## 口述答案

答案是 **A. 0 1**，实际输出 `0 1`。

用 [] 访问不存在的键会自动插入一个值初始化的默认值（int 得 0），size 从 0 变 1。只读判断键是否存在应改用 find() 或 at()。

## 讲深一层

map 的 operator[] 是非 const 成员，键不存在就插入一个值初始化的元素（int 得 0、指针得 nullptr、类调默认构造），size 因此从 0 变成 1。所以 const map 不能用 []。只读查询用 find、count 或 at——at 在键不存在时抛 out_of_range 而不是静默插入。

## 高频追问

1. **为什么 size 变成 1？** —— m["x"] 对不存在的键执行了插入，容器里真的多了一个 x=0 的条目。
2. **只想读不想插怎么办？** —— 用 find 判 != end()，或 at()（缺失抛异常），C++20 还可用 contains。
3. **const map 为什么不能用 []？** —— operator[] 可能插入，属于修改操作，没有 const 重载。

## 易错点

- 忽略插入副作用，答 0 0 选 B
- 以为默认值不确定，答随机值 1 选 C
- 以为 [] 对缺失键会报错或抛异常

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 30 关联容器与适配器
