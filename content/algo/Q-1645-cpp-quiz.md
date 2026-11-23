---
id: Q-1645
title: 这段 C++ 代码输出什么？（25 智能指针 · 第 33 题）
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
auto a = make_shared<int>(1);
auto b = a;
{
    auto c = b;
    cout << a.use_count();
}
cout << a.use_count();
```

- **A.** 32
- **B.** 33
- **C.** 22
- **D.** 31

## 口述答案

答案是 **A. 32**，实际输出 `32`。

a、b、c 共享同一个对象，计数是 3；c 离开作用域后减为 2。

## 讲深一层

拷贝 shared_ptr 让强引用计数原子递增：a、b、c 三个持有者，计数为 3；c 出作用域析构，减到 2。计数归零才真正 delete 对象。use_count 只适合调试，多线程下读到的是瞬时值。make_shared 把控制块和对象一次分配，比 shared_ptr<T>(new T) 少一次分配，且异常安全。

## 高频追问

1. **为什么块内是 3？** —— a、b、c 三个 shared_ptr 指向同一控制块，每个持有者各贡献 1 个强引用。
2. **为什么块外是 2？** —— c 析构时计数减 1，a、b 仍在作用域内，剩 2；两者都销毁才归零释放。
3. **use_count 能拿来做逻辑判断吗？** —— 不建议，它只是观测值，多线程下随时变化；判断是否唯一持有应用 use_count()==1 之外的显式设计。

## 易错点

- 漏算 b 这个拷贝，答 22 选 C
- 以为出块不释放，答 33 选 B
- 认为 use_count 返回字节数或对象大小

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 25 智能指针
