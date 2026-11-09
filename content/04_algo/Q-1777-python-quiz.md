---
id: Q-1777
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 83 题）
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
sm = torch.softmax(torch.tensor([1.0, 2.0, 3.0]), dim=0)
print([round(v, 6) for v in sm.tolist()], round(float(sm.sum()), 6))
```

- **A.** [0.090031, 0.244728, 0.665241] 1.0
- **B.** ([0.665241, 0.244728, 0.090031], 1.0)
- **C.** ([0.090031, 0.244728, 0.665241], 3.0)
- **D.** ([0.333333, 0.333333, 0.333333], 1.0)

## 口述答案

答案是 **A. [0.090031, 0.244728, 0.665241] 1.0**，实际输出 `[0.090031, 0.244728, 0.665241] 1.0`。

softmax 把一组数变成概率分布，sum 恒为 1；数值最大的 3.0 拿到最大概率 0.665。dim 必须指定，否则会按全局算。

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

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
