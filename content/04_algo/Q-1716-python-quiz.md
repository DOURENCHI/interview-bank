---
id: Q-1716
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 23 题）
module: 04_algo
sub: 容器与切片
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-21
tags: [Python, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```python
print(int("ff", 16), int("101", 2), float("1e3"))
```

- **A.** 255 5 1000.0
- **B.** 15 5 1000.0
- **C.** 255 5 100.0
- **D.** 255 101 1000.0

## 口述答案

答案是 **A. 255 5 1000.0**，实际输出 `255 5 1000.0`。

int 带第二参数可按指定进制解析；float("1e3") 认科学计数法得 1000.0。

## 讲深一层

讲深一层：int(s, base) 的 base 取 2~36，字母大小写都认；带前缀的串只在 base 匹配或 base=0 时合法，int("0x1f",16) 和 int("0x1f",0) 都行，int("0x1f",10) 抛 ValueError。int("1e3") 也不行，科学计数法只有 float 认；int 对 float 向零截断。

## 高频追问

1. **int("0b11",2) 可以吗？** —— 可以，base 与前缀一致时允许带前缀。
2. **base=0 有什么用？** —— 让 Python 按字面量前缀自动判进制。
3. **怎么解析 "1_000"？** —— int("1_000") 合法，下划线可作数字分隔符。

## 易错点

- 写 int("ff") 想得 255：缺 base 按十进制解析，抛 ValueError
- 用 int("1e3") 得 1000：int 不认科学计数法，抛 ValueError
- 以为 int(-3.9) 是 -4：向零截断，实际 -3

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
