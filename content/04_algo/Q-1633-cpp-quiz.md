---
id: Q-1633
title: 这段 C++ 代码输出什么？（14 静态成员 · 第 21 题）
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
struct S {
    static int n;
    S() { n++; }
    ~S() { n--; }
};
int S::n = 0;
int main() {
    S a;
    { S b, c; cout << S::n; }
    cout << S::n;
}
```

- **A.** 31
- **B.** 33
- **C.** 11
- **D.** 32

## 口述答案

答案是 **A. 31**，实际输出 `31`。

静态成员 n 所有对象共享：块内有 3 个对象；块结束 b、c 析构后剩 1 个。

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

`教学文档/C++实验台/C++考点实验台.html` · 14 静态成员
