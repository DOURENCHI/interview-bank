---
id: Q-1751
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 57 题）
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
import torch
t = torch.tensor([1.0, 2.0])
print(t.sum().item(), type(t.sum().item()).__name__, t.sum())
```

- **A.** 3.0 float tensor(3.)
- **B.** 3 int tensor(3.)
- **C.** 3.0 int tensor(3.)
- **D.** 3.0 float 3.0

## 口述答案

答案是 **A. 3.0 float tensor(3.)**，实际输出 `3.0 float tensor(3.)`。

item() 把标量张量转成 Python 数字（这里是 float）；不调 item() 直接 print 得到的是 tensor(3.) 这种张量表示。

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

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
