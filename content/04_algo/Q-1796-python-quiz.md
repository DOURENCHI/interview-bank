---
id: Q-1796
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 102 题）
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
import torch.nn as nn
import torch.nn.functional as F
class Res(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.c1 = nn.Conv2d(c, c, 3, padding=1)
        self.c2 = nn.Conv2d(c, c, 3, padding=1)
    def forward(self, x):
        return x + self.c2(F.relu(self.c1(x)))
print(tuple(Res(8)(torch.randn(1, 8, 16, 16)).shape))
```

- **A.** (1, 8, 16, 16)
- **B.** ((1, 16, 16, 16),)
- **C.** ((1, 8, 14, 14),)
- **D.** ((1, 8, 8, 8),)

## 口述答案

答案是 **A. (1, 8, 16, 16)**，实际输出 `(1, 8, 16, 16)`。

padding=1 保持空间尺寸，残差相加要求形状一致，所以残差块进出形状完全相同——这是残差能「深下去」的前提。

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

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
