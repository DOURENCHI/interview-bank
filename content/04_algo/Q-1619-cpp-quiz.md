---
id: Q-1619
title: 这段 C++ 代码输出什么？（05 控制结构 · 第 7 题）
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
int x = 2;
switch (x) {
    case 1: cout << "A";
    case 2: cout << "B";
    case 3: cout << "C";
    default: cout << "D";
}
```

- **A.** B
- **B.** BC
- **C.** BCD
- **D.** BD

## 口述答案

答案是 **C. BCD**，实际输出 `BCD`。

没有 break 会贯穿：从 case 2 进入，一路执行到 switch 结束。

## 讲深一层

switch 只做一次跳转，不自动阻断，break 才是出口。没有 break 就从匹配的 case 一路贯穿到 switch 末尾，所以这里走 case 2、3、default。若 case 2 后加 break 就只输出 B。case 标签必须是整型常量表达式，变量、字符串、浮点都不合法；建议开 -Wimplicit-fallthrough 抓漏写。

## 高频追问

1. **为什么会输出三个字母？** —— x=2 跳到 case 2，之后没有 break，控制流顺序贯穿 case 3 和 default，三段都执行。
2. **加一个 break 会怎样？** —— 在 case 2 的语句后加 break，输出 B 后立即跳出，结果是 B。
3. **case 能写变量或字符串吗？** —— 不能，必须是编译期整型常量表达式；字符串要用 if-else 或 map 分派。

## 易错点

- 以为 switch 只执行匹配的那一个分支，答 B，选成 A
- 漏看 default 也会被贯穿，答 BC，选成 B
- 把贯穿当成编译器 bug，认为应当编译报错

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 05 控制结构
