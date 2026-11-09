---
id: Q-1654
title: 这段 C++ 代码输出什么？（30 关联容器与适配器 · 第 42 题）
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
map<string,int> m;
cout << m["x"] << " " << m.size();
```

- **A.** 0 1
- **B.** 0 0
- **C.** 随机值 1
- **D.** 编译错误

## 口述答案

答案是 **A. 0 1**，实际输出 `0 1`。

用 [] 访问不存在的键会自动插入一个值初始化的默认值（int 得 0），size 从 0 变 1。只读判断键是否存在应改用 find() 或 at()。

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

`教学文档/C++实验台/C++考点实验台.html` · 30 关联容器与适配器
