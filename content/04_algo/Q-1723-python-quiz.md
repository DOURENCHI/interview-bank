---
id: Q-1723
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 30 题）
module: 04_algo
sub: 语法与类型
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-21
tags: [Python, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```python
print(str([1, 2]), repr("a"), str(1.0), repr(1.0))
```

- **A.** [1, 2] 'a' 1.0 1.0
- **B.** [1, 2] a 1.0 1.0
- **C.** [1, 2] 'a' 1.0 1
- **D.** '[1, 2]' a 1.0 1.0

## 口述答案

答案是 **A. [1, 2] 'a' 1.0 1.0**，实际输出 `[1, 2] 'a' 1.0 1.0`。

str 给用户看、repr 给开发者看（repr 会带引号）；但浮点数 repr 与 str 相同都是 1.0，浮点没有那层额外引号差异。

## 讲深一层

讲深一层：str 面向用户、repr 面向调试，对字符串差别最大——repr("a") 得 'a' 带引号且转义换行，str("a") 就是 a。容器统一用元素 repr 拼装，所以 str([1,"a"]) 显示 [1, 'a']。Python 3 起 float 的 str 与 repr 统一为最短往返表示，1.0 两者都是 1.0。

## 高频追问

1. **为什么 print([1,"a"]) 带引号？** —— 容器内部用 repr 显示元素。
2. **自定义类怎么控制显示？** —— 实现 __str__ 管 print，__repr__ 管调试与容器内显示。
3. **repr 能还原对象吗？** —— 对内置类型常可 eval 回去，但不保证通用。

## 易错点

- 以为 print 字符串会带引号：直接 print("a") 输出 a，不带引号
- 以为 str 和 repr 对 float 不同：本题两者都是 1.0，写成 1 就错
- 把 repr 当 str 用于用户提示：会把引号和转义符一起显示出来

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
