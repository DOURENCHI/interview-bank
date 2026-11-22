---
id: Q-1710
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 17 题）
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
print("abc".isalpha(), "123".isdigit(), "a1".isalnum())
```

- **A.** True True True
- **B.** True True False
- **C.** False True True
- **D.** True False True

## 口述答案

答案是 **A. True True True**，实际输出 `True True True`。

isalpha 只认字母、isdigit 只认数字、isalnum 字母数字都认，所以 "a1" 三个判断都成立。

## 讲深一层

讲深一层：三个方法都要求「非空且全部字符满足条件」，所以 "".isalpha() 是 False，不是空真。判定基于 Unicode 类别而不只是 ASCII：中文 "中".isalpha() 为 True。isalnum 等价于 isalpha 或 isdigit，空格、下划线、小数点都会让它返回 False，所以 "-1" 不算数字串。

## 高频追问

1. **怎么判断能否转 int？** —— 用 try: int(s) 更可靠，isdigit 不认负号。
2. **isdigit 和 isnumeric 区别？** —— isnumeric 范围最广含分数与圈码，isdecimal 最严只认十进制数字。
3. **空串为什么是 False？** —— 定义要求至少一个字符且全部满足。

## 易错点

- 以为 "a1".isalpha() 是 True：含数字，返回 False
- 用 isdigit 校验负数字符串："-1".isdigit() 为 False，误判成非法输入
- 以为空串 isalpha 为 True：实际 False

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
