---
id: Q-1783
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 90 题）
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

`(y==p).float().mean()` 是逐元素准确率：90 个负类全对、10 个正类全错，得 0.9。accuracy 对类别不平衡完全不敏感，全预测多数类就能拿高分，但正类召回率是 0。所以不平衡数据要看 per-class precision/recall/F1 或 AUC-PR，而不是单看 accuracy。

## 高频追问

1. **该看什么指标？** —— 正类的 precision/recall/F1、AUC-PR；本场景 recall=0 会立刻暴露问题
2. **为什么 AUC 更稳？** —— 它衡量排序质量，与阈值和类别先验无关，不受多数类淹没
3. **若全预测 1 呢？** —— accuracy 变 0.1，同样说明单看 accuracy 会被先验带着走

## 易错点

- 认为 0.9 说明模型不错——正类一个没抓到，实际不可用
- 去掉 `.float()` 直接 `mean()`——bool 张量求均值报 `could not infer output dtype`
- 用 `==` 比较浮点概率——只有 p 恰好是 0.0 才成立，一般要用阈值二值化

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
