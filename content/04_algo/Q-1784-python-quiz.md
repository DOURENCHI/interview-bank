---
id: Q-1784
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 90 题）
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
y = torch.tensor([0.0] * 90 + [1.0] * 10)
p = torch.tensor([0.0] * 100)
print(round(float((y == p).float().mean()), 6))
```

- **A.** 0.9
- **B.** 0.1
- **C.** 1.0
- **D.** 0.0

## 口述答案

答案是 **A. 0.9**，实际输出 `0.9`。

全预测 0 就有 90% 准确率——类别不平衡时 accuracy 会骗人，这就是要用精确率/召回率/F1 或 AUC 的原因。

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
