---
id: Q-1714
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 21 题）
module: algo
sub: 函数与异常
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
a = [1, 2, 3]
print(a.index(2), a.count(1))
```

- **A.** 1 1
- **B.** 2 1
- **C.** 1 2
- **D.** 0 1

## 口述答案

答案是 **A. 1 1**，实际输出 `1 1`。

index 返回下标不是值，2 在下标 1 处；count 统计出现次数，1 出现 1 次。

## 讲深一层

讲深一层：index 返回「第一个」匹配元素的下标，找不到抛 ValueError 而不是 -1（这点和 str.find 相反）；可传 start/end 限定区间，仍是左闭右开。count 用 == 统计出现次数，1 和 True 会被算作同一个值。两者都是 O(n) 线性扫描，循环里反复调用会退化成 O(n²)。

## 高频追问

1. **找不到会怎样？** —— 抛 ValueError，安全写法是先 in 判断或 try。
2. **str 的 find 和 index 区别？** —— find 找不到返回 -1，index 抛 ValueError。
3. **怎么找所有出现位置？** —— `[i for i,x in enumerate(a) if x==v]`。

## 易错点

- 把 index 的返回值当元素值：a.index(2) 输出 1 不是 2
- 以为找不到返回 -1：实际抛 ValueError，输出变成异常
- 用 count 统计含布尔的列表：True 会被计入 1 的次数

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
