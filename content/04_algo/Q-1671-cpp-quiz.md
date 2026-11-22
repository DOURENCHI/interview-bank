---
id: Q-1671
title: 这段 C++ 代码输出什么？（37 流与字符串处理 · 第 59 题）
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
istringstream iss("1 2 3");
int x, sum = 0;
while (iss >> x) sum += x;
cout << sum;
```

- **A.** 6
- **B.** 123
- **C.** 3
- **D.** 1 2 3

## 口述答案

答案是 **A. 6**，实际输出 `6`。

用 while(iss >> x) 逐个读整数并累加；读取失败或到达末尾时表达式为假，循环自然结束。不要写 while(!iss.eof())，它会让最后一项多处理一次。

## 讲深一层

operator>> 返回流对象的引用，流有 explicit operator bool，读取成功为 true；while (iss >> x) 在解析失败或到达末尾时条件为假，循环自然结束且不会多处理一次。别写 while (!iss.eof())：eof 只在读失败后才置位，若末尾还有换行或空格，循环会再进一轮，把旧值又加一遍。

## 高频追问

1. **为什么是 6？** —— 依次读出 1、2、3 累加，第四次读取失败退出，得到 6。
2. **为什么不能写 !iss.eof()？** —— 读完 3 时若还没碰到末尾（例如后面有换行），eof 仍为假，循环再进一次，x 保持 3，和变成 9。
3. **遇到非数字会怎样？** —— operator>> 解析失败置 failbit，循环条件为假退出，非法字符留在缓冲里等下一次读。

## 易错点

- 把三个数当字符串拼起来，答 123 选 B
- 以为循环只读一次，答 3 选 C
- 用 while(!iss.eof()) 且输入带换行，多算一次得 9

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 37 流与字符串处理
