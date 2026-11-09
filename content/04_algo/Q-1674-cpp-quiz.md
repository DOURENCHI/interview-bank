---
id: Q-1674
title: 这段 C++ 代码输出什么？（38 多线程与状态机 · 第 61 题）
module: 04_algo
sub: C++语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/C++实验台/C++考点实验台.html
verified_at: 2026-11-09
tags: [C++, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```cpp
atomic<int> s{0};
thread t1([&]{ s += 1; });
thread t2([&]{ s += 1; });
t1.join(); t2.join();
cout << s.load();
```

- **A.** 2
- **B.** 0
- **C.** 1
- **D.** 结果不确定

## 口述答案

答案是 **A. 2**，实际输出 `2`。

atomic 的 += 是原子操作，两个线程各加 1 后必为 2；若换成普通 int 并发自增，就是数据竞争，属于未定义行为。join 等待线程结束，detach 则要自己保证被捕获的变量还活着。

## 讲深一层

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 38 多线程与状态机
