---
id: Q-1804
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 110 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
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
import torch
torch.manual_seed(10)
d = torch.nn.Dropout(0.5)
d.eval()
print(round(float(d(torch.ones(10)).sum()), 4))
```

- **A.** 10.0
- **B.** 0.0
- **C.** 5.0
- **D.** 1.0

## 口述答案

答案是 **A. 10.0**，实际输出 `10.0`。

eval 模式关闭 Dropout，10 个 1 原样通过，和是 10.0。推理时忘了 model.eval() 是最常见的线上事故。

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

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
