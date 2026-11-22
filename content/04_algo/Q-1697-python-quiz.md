---
id: Q-1697
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 4 题）
module: 04_algo
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
print(int("42"), float("3.5"), str(3.5), bool(""), bool("0"))
```

- **A.** 42 3.5 3.5 False True
- **B.** 42 3.5 3.5 False False
- **C.** 42 3.5 '3.5' False False
- **D.** 42 3.5 3.5 True True

## 口述答案

答案是 **A. 42 3.5 3.5 False True**，实际输出 `42 3.5 3.5 False True`。

bool 的判定规则是「非空即真」，不看内容是不是 0：空字符串是 False，但字符串 "0" 非空所以是 True。

## 讲深一层

讲深一层：真值判定只看「空不空、零不零」，不看内容含义：""、[]、{}、0、0.0、None、False 为假，而 "0"、" "、[0]、[[]] 都为真。print 对字符串不加引号，所以 str(3.5) 显示成 3.5，看输出分不清它是 str 还是 float，用 repr 才带引号。bool 是 int 子类，True+True 得 2。

## 高频追问

1. **怎么判断字符串非空更明确？** —— `if s:` 即可；要排除纯空白用 `s.strip()`。
2. **bool("False") 是什么？** —— True，非空字符串，不看字面含义。
3. **print 里怎么看出是字符串？** —— 用 repr() 或 f"{x!r}"，会补上引号。

## 易错点

- 认为 bool("0") 是 False：非空即真，实际输出 True
- 把 str(3.5) 的输出当 float：它是字符串，`== 3.5` 得 False
- 用 `if x == True` 判真值：应写 `if x`，且 1==True 也成立，容易混

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
