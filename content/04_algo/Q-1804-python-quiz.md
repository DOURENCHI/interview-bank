---
id: Q-1804
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 111 题）
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
torch.manual_seed(11)
m = torch.nn.Linear(2, 1)
sd = {k: v.clone() for k, v in m.state_dict().items()}
m(torch.randn(2, 2)).sum().backward()
m2 = torch.nn.Linear(2, 1)
m2.load_state_dict(sd)
print(tuple(m.state_dict().keys()), bool(torch.equal(m.weight, m2.weight)), bool(torch.equal(m.bias, m2.bias)))
```

- **A.** ('weight', 'bias') True True
- **B.** ('weight', 'bias') False True
- **C.** ('param',) True True
- **D.** ('weight', 'bias') True False

## 口述答案

答案是 **A. ('weight', 'bias') True True**，实际输出 `('weight', 'bias') True True`。

state_dict 是有序字典，键为 weight/bias；load_state_dict 把保存的值装回新模型，两个布尔都为 True。

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
