---
id: Q-1661
title: 这段 C++ 代码输出什么？（32 函数对象与谓词 · 第 49 题）
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
struct Odd {
  bool operator()(int x) const { return x % 2 != 0; }
};
vector<int> v{1,2,3,4,5};
cout << count_if(v.begin(), v.end(), Odd());
```

- **A.** 3
- **B.** 2
- **C.** 5
- **D.** 编译错误

## 口述答案

答案是 **A. 3**，实际输出 `3`。

函数对象（仿函数）是重载了 operator() 的类实例，count_if 对每个元素调用它；1 3 5 为奇数共 3 个。相比普通函数，它可以带状态。

## 讲深一层

函数对象是重载了 operator() 的类实例，count_if 对每个元素调用它；1、3、5 共 3 个奇数。相比普通函数，它能携带成员状态（如计数），作为模板参数时类型已知、易内联，比 std::function 快。lambda 本质就是编译器生成的函数对象；operator() 记得加 const，否则 const 上下文调用失败。

## 高频追问

1. **数了哪几个？** —— 1、3、5 满足奇数条件，共 3 个；2 和 4 被排除。
2. **比普通函数强在哪？** —— 可带状态、可被模板内联；std::function 存它要做类型擦除，多一次间接调用。
3. **operator() 为什么加 const？** —— 算法按值持有谓词，常以 const 对象调用，非 const 版本会编译失败。

## 易错点

- 把奇数当偶数数，答 2 选 B
- 漏写 const 修饰 operator()，编译报错却以为语法不支持
- 把 Odd() 写成 Odd 传参，编译错误

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 32 函数对象与谓词
