---
id: Q-1669
title: 这段 C++ 代码输出什么？（36 智能指针与移动语义 · 第 57 题）
module: algo
sub: 指针与内存
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
auto a = make_shared<int>(7);
{ auto b = a; cout << a.use_count() << " "; }
cout << a.use_count();
```

- **A.** 2 1
- **B.** 1 1
- **C.** 2 2
- **D.** 1 0

## 口述答案

答案是 **A. 2 1**，实际输出 `2 1`。

拷贝 shared_ptr 使引用计数从 1 增到 2；离开内层作用域析构 b 后减回 1。计数归零才真正 delete 对象；互持有 shared_ptr 会造成循环引用，需要 weak_ptr 打破。

## 讲深一层

拷贝 shared_ptr 让强引用计数原子递增，出作用域析构递减，归零才 delete 对象。use_count 只在单线程调试时有参考价值，多线程下只是瞬时快照。make_shared 把对象和控制块一次分配，少一次 new 且异常安全。互相持有 shared_ptr 会成环、计数永不归零，需要用 weak_ptr 打破。

## 高频追问

1. **块内为什么是 2？** —— a 与块内的 b 两个持有者指向同一对象，拷贝构造使计数从 1 增到 2。
2. **块外为什么回到 1？** —— b 析构时计数递减，只剩 a 持有，对象尚未销毁。
3. **循环引用怎么破？** —— 把其中一端的成员改成 weak_ptr，不增加强计数，访问时用 lock() 临时提升。

## 易错点

- 以为拷贝不计数，答 1 1 选 B
- 以为出块不释放，答 2 2 选 C
- 以为 a 也被销毁，答 1 0 选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 36 智能指针与移动语义
