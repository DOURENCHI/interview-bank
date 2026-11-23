---
id: Q-1656
title: 这段 C++ 代码输出什么？（31 STL 算法 · 第 44 题）
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
int a[5] = {5,2,9,1,6};
cout << accumulate(a, a+5, 0);
```

- **A.** 23
- **B.** 22
- **C.** 24
- **D.** 编译错误

## 口述答案

答案是 **A. 23**，实际输出 `23`。

accumulate 在 <numeric> 里，按左闭右开区间从初值 0 开始累加，得 23。初值写成 0.0 就会按 double 累加，类型由初值决定。

## 讲深一层

accumulate 声明在 <numeric> 而非 <algorithm>；第三参数既是初值也决定累加变量和返回值的类型：0 得 int，0.0 得 double，0LL 得 long long。区间左闭右开。第四个参数可传自定义二元操作，如 std::multiplies<> 变成连乘。初值类型给错会静默截断，累加大数时容易溢出。

## 高频追问

1. **结果怎么算出来的？** —— 从初值 0 开始依次加 5、2、9、1、6，得 23。
2. **初值写 0.0 会怎样？** —— 按 double 累加，值仍是 23，但返回类型变成 double；cout 默认不显示 .0。
3. **只 include algorithm 行吗？** —— 不行，accumulate 在 <numeric>，会报未声明标识符。

## 易错点

- 把区间当闭区间，多数一个元素
- 用 int 初值累加十亿级数据，溢出成负数
- 把 accumulate 记成在 <algorithm> 里，编译失败

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 31 STL 算法
