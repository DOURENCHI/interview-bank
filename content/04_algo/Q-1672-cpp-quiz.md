---
id: Q-1672
title: 这段 C++ 代码输出什么？（37 流与字符串处理 · 第 59 题）
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 37 流与字符串处理
