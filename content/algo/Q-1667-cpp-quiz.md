---
id: Q-1667
title: 这段 C++ 代码输出什么？（35 chrono 与时间 · 第 55 题）
module: algo
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
auto d = chrono::milliseconds(1500);
cout << chrono::duration_cast<chrono::seconds>(d).count()
     << " " << d.count();
```

- **A.** 1 1500
- **B.** 1.5 1500
- **C.** 2 1500
- **D.** 1500 1

## 口述答案

答案是 **A. 1 1500**，实际输出 `1 1500`。

duration_cast 从细粒度向粗粒度转换时向零截断，1500ms 变 1 秒；原 duration 的 count() 仍以毫秒为单位，是 1500。类型里带着单位，不会把秒和毫秒混用。

## 讲深一层

duration_cast 是显式转换，向粗粒度走时按整数除法截断（向零），1500ms 得 1s、丢掉 500ms；count() 返回 Rep 的裸数值，单位由类型携带，不会替你换算。想保留小数就转成 duration<double>，此时 count() 给 1.5。原对象 d 不会被转换修改。

## 高频追问

1. **为什么是 1 不是 1.5？** —— 目标类型 seconds 的 Rep 是整型 long long，1500/1000 整除得 1，余数被丢弃。
2. **第二个为什么还是 1500？** —— duration_cast 返回新对象，d 本身不变，count() 仍按毫秒给出原值。
3. **怎么拿到 1.5？** —— 转成 duration<double>(d).count()，或用 duration<double, milli> 保留毫秒精度。

## 易错点

- 以为 duration_cast 保留小数，答 1.5 1500 选 B
- 以为会四舍五入到 2，答 2 1500 选 C
- 以为 d 被就地转换，答 1 1

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 35 chrono 与时间
