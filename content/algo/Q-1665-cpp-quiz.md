---
id: Q-1665
title: 这段 C++ 代码输出什么？（34 类型转换与模板 · 第 53 题）
module: algo
sub: 语法与陷阱
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
double d = 3.9;
cout << static_cast<int>(d) << " " << (int)d;
```

- **A.** 3 3
- **B.** 3 4
- **C.** 4 4
- **D.** 3.9 3

## 口述答案

答案是 **A. 3 3**，实际输出 `3 3`。

浮点转整型是截断、不是四舍五入，两者都得 3。static_cast 与 C 风格括号结果相同，但语义明确、便于搜索；向下转型做运行时检查要用 dynamic_cast。

## 讲深一层

浮点转整型向零截断，不是四舍五入：-3.9 得 -3 而非 -4；超出目标类型范围是未定义行为。static_cast 与 C 风格括号结果一致，但语义明确、可被检索。dynamic_cast 用于多态类型的向下转型并做运行时检查，指针失败得 nullptr、引用失败抛 bad_cast；reinterpret_cast 只重解释位模式。

## 高频追问

1. **为什么不是 4？** —— 转换规则是丢弃小数部分，不做任何舍入，3.9 直接截成 3。
2. **两种写法有区别吗？** —— 结果相同。static_cast 有编译期相关性检查且可搜索，C 风格会依次尝试 const_cast、static_cast、reinterpret_cast。
3. **负数怎么截？** —— 向零截断，-3.9 得 -3，不是 floor 的 -4；这点和取整函数容易混。

## 易错点

- 以为 C 风格括号会四舍五入，答 3 4 选 B
- 两种都当四舍五入，答 4 4 选 C
- 把超范围的 double 转 int，写成合法代码却触发 UB

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 34 类型转换与模板
