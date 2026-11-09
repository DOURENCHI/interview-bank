---
id: Q-1753
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 60 题）
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
a = torch.tensor([1, 2])
b = torch.tensor([3, 4])
print(torch.cat([a, b]).tolist(), tuple(torch.stack([a, b]).shape))
```

- **A.** [1, 2, 3, 4] (2, 2)
- **B.** ([1, 2, 3, 4], (2,))
- **C.** ([1, 3, 2, 4], (2, 2))
- **D.** ([1, 2, 3, 4], (4,))

## 口述答案

答案是 **A. [1, 2, 3, 4] (2, 2)**，实际输出 `[1, 2, 3, 4] (2, 2)`。

cat 是拼接（形状变长），stack 是堆叠（新增一个维度），所以 stack 后是 (2,2)。

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
