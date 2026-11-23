---
id: Q-1720
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 27 题）
module: algo
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
print(1 == 1.0, 1 == 1.0, [1, 2] == [1.0, 2.0])
```

- **A.** True True True
- **B.** True False True
- **C.** False True True
- **D.** True True False

## 口述答案

答案是 **A. True True True**，实际输出 `True True True`。

数值比较跨类型按值判定，1 == 1.0 为真；列表比较逐元素比，1 == 1.0 也为真，所以整个列表相等。

## 讲深一层

讲深一层：数值比较跨类型时按数学值比，int 与 float 会先转换再比，所以 1==1.0 为真；但超过 2^53 的整数与 float 比较会因精度丢失出现反直觉结果。序列比较先比长度再逐元素 ==，[1,2]==[1.0,2.0] 逐位相等故为真，而 [1,2]==(1,2) 因类型不同直接 False。

## 高频追问

1. **为什么 [1,2]==[1.0,2.0] 是 True？** —— 列表逐元素用 == 比较，数值跨类型相等。
2. **[1,2] 和 (1,2) 相等吗？** —— 不相等，list 与 tuple 类型不同。
3. **大整数和 float 比较有坑吗？** —— 有，超过 2^53 精度丢失，结果可能反直觉。

## 易错点

- 以为 int 和 float 永不相等：1==1.0 为 True，会漏判
- 以为列表比较看类型：[1,2]==[1.0,2.0] 为 True，类型不参与逐元素判定
- 用 == 比较浮点计算结果：0.1+0.2==0.3 为 False，应改用 math.isclose

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
