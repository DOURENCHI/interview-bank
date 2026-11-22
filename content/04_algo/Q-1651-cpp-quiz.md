---
id: Q-1651
title: 这段 C++ 代码输出什么？（29 序列容器 · 第 39 题）
module: 04_algo
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
try { cout << v.at(5); }
catch (const out_of_range&) { cout << "E"; }
```

- **A.** E
- **B.** 0
- **C.** 3
- **D.** 运行崩溃

## 口述答案

答案是 **A. E**，实际输出 `E`。

at() 会检查越界并抛 std::out_of_range，异常被 catch 住所以输出 E；operator[] 不检查越界，是未定义行为（可能读到垃圾值，也可能崩溃）。

## 讲深一层

at 会做边界检查，越界抛 std::out_of_range（继承自 logic_error），被 catch(const out_of_range&) 接住，所以输出 E。operator[] 完全不检查，越界是未定义行为——可能读到垃圾值，也可能段错误，不能指望它抛异常。标准库序列容器里只有 at 提供这种检查。

## 高频追问

1. **为什么输出 E 而不是崩溃？** —— at(5) 发现 5 >= size()，抛出异常，控制流跳到匹配的 catch 块。
2. **换成 v[5] 呢？** —— 未定义行为，可能打印栈上残留值，也可能直接崩溃，结果不可依赖。
3. **catch 为什么用 const 引用？** —— 避免按值拷贝和对象切片，还能接住 out_of_range 的派生异常。

## 易错点

- 以为 at 越界返回 0，答 0 选 B
- 以为 at 只断言不抛异常，答运行崩溃选 D
- 用 catch(out_of_range e) 按值捕获，多一次拷贝

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 29 序列容器
