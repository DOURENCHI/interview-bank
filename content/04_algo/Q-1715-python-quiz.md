---
id: Q-1715
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 22 题）
module: 04_algo
sub: 语法与类型
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
print(bin(10), oct(10), hex(255), abs(-3))
```

- **A.** 0b1010 0o12 0xff 3
- **B.** 1010 12 ff 3
- **C.** 0b1010 0o12 0xff -3
- **D.** 0b1010 0o12 0xFF -3

## 口述答案

答案是 **A. 0b1010 0o12 0xff 3**，实际输出 `0b1010 0o12 0xff 3`。

bin/oct/hex 都带前缀（0b / 0o / 0x），hex 输出小写；abs(-3) 是 3。

## 讲深一层

讲深一层：bin/oct/hex 返回的是带前缀的字符串（0b/0o/0x），字母一律小写，负数把负号放最前如 -0xff。只要数字不要前缀就用 format(n,"b") 或 f"{n:x}"。反向解析用 int(s,0) 让解释器按前缀自动识别进制，int("0x1f",16) 也成立。abs 对复数返回的是模长而非实部。

## 高频追问

1. **怎么去掉 0x 前缀？** —— `format(255,"x")` 得 'ff'，或切片 [2:]。
2. **hex 能输出大写吗？** —— `format(255,"X")` 或对结果 .upper()。
3. **怎么把 0b1010 转回数字？** —— `int("0b1010",2)` 或 `int("0b1010",0)`。

## 易错点

- 以为 hex(255) 是 'FF'：默认小写，输出 0xff
- 以为 bin() 返回 int：返回字符串，不能直接参与算术
- 用 int("ff") 解析十六进制：缺 base 抛 ValueError，要写 int("ff",16)

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
