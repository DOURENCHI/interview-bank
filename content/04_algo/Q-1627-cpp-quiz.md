---
id: Q-1627
title: 这段 C++ 代码输出什么？（08 引用 · 第 14 题）
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
void f(int x, int &y) { x = 9; y = 9; }
int main() {
    int a = 1, b = 1;
    f(a, b);
    cout << a << b;
}
```

- **A.** 11
- **B.** 19
- **C.** 91
- **D.** 99

## 口述答案

答案是 **B. 19**，实际输出 `19`。

按值传参改的是副本，a 不变；按引用传参改的就是 b 本身。

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

`教学文档/C++实验台/C++考点实验台.html` · 08 引用
