---
id: Q-1620
title: 这段 C++ 代码输出什么？（05 控制结构 · 第 8 题）
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
int i, c = 0;
for (i = 0; i < 10; i += 3) c++;
cout << c << " " << i;
```

- **A.** 3 9
- **B.** 4 10
- **C.** 4 12
- **D.** 3 12

## 口述答案

答案是 **C. 4 12**，实际输出 `4 12`。

i 依次取 0、3、6、9，共 4 次；之后 i 变成 12，条件不成立，循环结束。

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

`教学文档/C++实验台/C++考点实验台.html` · 05 控制结构
