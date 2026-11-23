---
id: Q-1673
title: 这段 C++ 代码输出什么？（38 多线程与状态机 · 第 61 题）
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

讲深一层：atomic 保证「单个读-改-写不可分割」，不是「整条语句原子」。写成 `s = s + 1` 时先 load 再 store，中间可被切走，仍会丢更新；`+=`、`++`、fetch_add 才是原子 RMW。默认 seq_cst 最严格，relaxed 只保原子性不保顺序。换成普通 int 并发自增是数据竞争，属未定义行为。

## 高频追问

1. **atomic 和 mutex 怎么选？** —— 单个计数器用 atomic 无锁更快；要保护多个变量之间的一致性（如队列头尾）必须用 mutex。
2. **i++ 和 ++i 对 atomic 有区别吗？** —— 作为独立语句没区别，都是 fetch_add(1)；但 `cout<<s++` 输出旧值、`cout<<++s` 输出新值。
3. **一个线程写一个线程读，读到的一定是新值吗？** —— seq_cst 下顺序一致；relaxed 只保证不撕裂，读到旧值合法。

## 易错点

- 写 `s = s + 1` 以为原子：拆成 load+store，两个线程可能都读到 0，最终输出 1 而不是 2
- 换成普通 int 还断言一定得 2：数据竞争是 UB，实际常看到 1，但不能作为确定答案
- 忘记 join 就打印：主线程可能在子线程写入前读取，甚至线程析构时直接 terminate

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 38 多线程与状态机
