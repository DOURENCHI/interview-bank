---
id: Q-1674
title: 这段 C++ 代码输出什么？（38 多线程与状态机 · 第 62 题）
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
int st = 0; string in = "abab", out;
for (char c : in) {
  if (st == 0) { out += toupper(c); st = 1; }
  else { out += c; st = 0; }
}
cout << out;
```

- **A.** AbAb
- **B.** ABAB
- **C.** aBaB
- **D.** abab

## 口述答案

答案是 **A. AbAb**，实际输出 `AbAb`。

两个状态交替：状态 0 把字符转大写并切到 1，状态 1 原样输出并切回 0，所以 a→A、b→b、a→A、b→b。状态机题的关键是把「当前状态 + 输入 → 次状态」列清楚再推。

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
