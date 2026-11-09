---
id: Q-1817
title: 分类：sigmoid、softmax 与三种交叉熵 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: draft
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 Python 程序对应的读入与输出写法是什么？

```python
import torch
import torch.nn as nn

logits_b = torch.tensor([2.0, -2.0])
y_b = torch.tensor([1.0, 0.0])
print("sigmoid", [round(v, 6) for v in torch.sigmoid(logits_b).tolist()])
print("BCELoss          ", round(float(nn.BCELoss()(torch.sigmoid(logits_b), y_b)), 6))
print("BCEWithLogitsLoss", round(float(nn.BCEWithLogitsLoss()(logits_b, y_b)), 6))

logits_m = torch.tensor([2.0, 1.0, 0.1])
sm = torch.softmax(logits_m, dim=0)
print("softmax", [round(v, 6) for v in sm.tolist()], "sum", round(float(sm.sum()), 6))
print("CrossEntropyLoss", round(float(nn.CrossEntropyLoss()(logits_m, torch.tensor([0]))), 6))
lp = torch.log_softmax(logits_m, dim=0)
print("NLLLoss          ", round(float(nn.NLLLoss()(lp, torch.tensor([0]))), 6))

y = torch.tensor([0.0] * 90 + [1.0] * 10)
p = torch.tensor([0.0] * 100)
print("全预测多数类的准确率", round(float((y == p).float().mean()), 6))
```

输出样例：

```
sigmoid [0.880797, 0.119203]
BCELoss           0.126928
BCEWithLogitsLoss 0.126928
softmax [0.659001, 0.242433, 0.098566] sum 1.0
CrossEntropyLoss 0.41703
NLLLoss           0.41703
全预测多数类的准确率 0.9
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
