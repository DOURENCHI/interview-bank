---
id: Q-1644
title: 这段 C++ 代码输出什么？（24 异常 · 第 32 题）
module: 04_algo
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
try {
    cout << "A";
    throw 1;
    cout << "B";
} catch (int) {
    cout << "C";
}
cout << "D";
```

- **A.** ACD
- **B.** ABCD
- **C.** AD
- **D.** ABD

## 口述答案

答案是 **A. ACD**，实际输出 `ACD`。

throw 之后的语句不再执行，直接跳到匹配的 catch；处理完继续往下走。

## 讲深一层

throw 是控制转移：抛出后本作用域剩余语句立即放弃执行，栈展开依次析构局部对象，再匹配 catch；catch 执行完从整个 try-catch 之后继续，而不是回到 throw 处。没有匹配的 catch 就调用 std::terminate。catch(...) 能兜底但拿不到异常对象，通常只用于清理和日志。

## 高频追问

1. **为什么没有 B？** —— cout << "B" 排在 throw 之后，控制流已跳出 try 块，永远不会执行。
2. **D 为什么还打印？** —— D 在 try-catch 结构之外，catch 处理完毕后顺序执行到它。
3. **抛自定义类型怎么接？** —— 按类型精确匹配，基类 catch 可接派生类异常（按值接会切片），建议用 const 引用；catch(...) 接全部。

## 易错点

- 以为 throw 后继续往下执行，答 ABCD 选 B
- 以为 catch 处理完就结束程序，答 AD 选 C
- 认为 throw 1 不匹配 catch(int)，实际类型完全一致

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 24 异常
