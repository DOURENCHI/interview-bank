---
id: Q-1767
title: 这段 Python 代码输出什么？（05 nn.Module 与训练循环 · 第 73 题）
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
torch.manual_seed(5)
m = torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.Dropout(0.5))
m.train()
a = float(m(torch.ones(1, 4)).sum().detach())
m.eval()
b = float(m(torch.ones(1, 4)).sum().detach())
print(round(a, 4), round(b, 4))
```

- **A.** 3.4002 1.4552
- **B.** (3.4002, 3.4002)
- **C.** (1.4552, 3.4002)
- **D.** (3.4002, 1.4552)

## 口述答案

答案是 **A. 3.4002 1.4552**，实际输出 `3.4002 1.4552`。

train() 下 Dropout 随机置零一半神经元，输出被放大（除以 1-p）；eval() 下关闭 Dropout，输出确定。同一份权重两种模式输出不同。

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

`教学文档/Python实验台/Python考点实验台.html` · 05 nn.Module 与训练循环
