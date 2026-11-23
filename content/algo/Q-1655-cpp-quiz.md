---
id: Q-1655
title: 这段 C++ 代码输出什么？（30 关联容器与适配器 · 第 43 题）
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
stack<int> st;
st.push(1); st.push(2);
cout << st.top(); st.pop(); cout << st.top();
```

- **A.** 21
- **B.** 12
- **C.** 22
- **D.** 11

## 口述答案

答案是 **A. 21**，实际输出 `21`。

stack 是容器适配器，后进先出：压入 1、2 后 top 是 2；pop 只移除不返回，之后 top 回到 1。queue 则相反（先进先出）。

## 讲深一层

stack 是容器适配器，默认用 deque 承载，只暴露 push/pop/top，严格后进先出。pop 返回 void，只移除不返回元素，想取值必须先 top 再 pop。queue 是先进先出（front/back），priority_queue 默认是大顶堆。空栈调 top 或 pop 都是未定义行为，必须先判 empty。

## 高频追问

1. **为什么先输出 2？** —— 压入顺序是 1、2，栈顶是最后进的 2。
2. **pop 有返回值吗？** —— 没有，返回 void；标准写法是 int v = st.top(); st.pop()。
3. **空栈 top 会怎样？** —— 未定义行为，可能读到越界内存或崩溃，使用前必须 if (!st.empty())。

## 易错点

- 当成队列，答 12 选 B
- 写 int x = st.pop(); 编译错误
- pop 后继续用之前 top 返回的引用，引用已悬垂

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 30 关联容器与适配器
