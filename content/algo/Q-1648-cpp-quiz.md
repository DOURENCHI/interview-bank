---
id: Q-1648
title: 这段 C++ 代码输出什么？（28 迭代器与 string · 第 36 题）
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
cout << *v.begin() << " " << *(v.end()-1)
     << " " << (v.end()-v.begin());
```

- **A.** 1 3 3
- **B.** 1 3 4
- **C.** 1 2 3
- **D.** 0 3 3

## 口述答案

答案是 **A. 1 3 3**，实际输出 `1 3 3`。

begin 指向第一个元素，end 指向最后一个元素的下一个位置，构成左闭右开 [begin, end)；随机访问迭代器相减得到元素个数 3。

## 讲深一层

迭代器区间是左闭右开 [begin, end)，end 指向末元素之后，所以 *(end()-1) 才是最后一个元素。随机访问迭代器相减得到 difference_type（ptrdiff_t），正好是元素个数 3；list 的迭代器不支持相减，要用 std::distance。空容器 begin == end，此时解引用即未定义行为。

## 高频追问

1. **为什么 *(v.end()-1) 是 3？** —— end 是尾后位置，回退一个才是末元素，值 3。
2. **为什么相减得 3？** —— end 与 begin 的下标差就是元素个数，类型是有符号的 ptrdiff_t。
3. **能对 list 这么写吗？** —— 不能，双向迭代器没有 operator-，编译失败；改用 std::distance，复杂度 O(n)。

## 易错点

- 以为 end 指向末元素，答 1 3 4 选 B
- 把 end-1 当倒数第二个，答 1 2 3 选 C
- 对空 vector 写 *v.begin()，未定义行为

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 28 迭代器与 string
