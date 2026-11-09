---
id: Q-1788
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 94 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```python
print((28 - 3) // 2 + 1, (32 - 3) // 2 + 1)
```

- **A.** 13 15
- **B.** (14, 16)
- **C.** (12, 14)
- **D.** (13, 14)

## 口述答案

答案是 **A. 13 15**，实际输出 `13 15`。

卷积输出 = (输入 - 核 + 1) // 步长，池化再取一半：28→26→13，32→30→15。

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

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
