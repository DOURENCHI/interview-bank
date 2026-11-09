---
id: Q-1670
title: 这段 C++ 代码输出什么？（36 智能指针与移动语义 · 第 57 题）
module: 04_algo
sub: C++语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 36 智能指针与移动语义
