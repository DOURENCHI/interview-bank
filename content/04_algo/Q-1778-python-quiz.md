---
id: Q-1778
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 84 题）
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
p = torch.tensor([0.2, 0.7, 0.1])
print(round(float(torch.argmax(p)), 6), float(p[1]))
```

- **A.** 1.0 0.699999988079071
- **B.** (0.0, 0.2)
- **C.** (2.0, 0.1)
- **D.** (1.0, 0.7)

## 口述答案

答案是 **A. 1.0 0.699999988079071**，实际输出 `1.0 0.699999988079071`。

argmax 给下标 1；float32 张量里 0.7 的实际值是 0.699999988079071——这就是为什么打印要用 .6f 之类取整，别直接比相等。

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
