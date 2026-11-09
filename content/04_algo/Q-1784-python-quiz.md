---
id: Q-1784
title: 这段 Python 代码输出什么？（08 CNN 与 RNN · 第 91 题）
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
x = torch.arange(25, dtype=torch.float32).reshape(1, 1, 5, 5)
conv = torch.nn.Conv2d(1, 1, kernel_size=3, bias=False)
with torch.no_grad():
    conv.weight.fill_(1.0)
print(tuple(conv(x).shape), conv(x).reshape(-1).tolist())
```

- **A.** (1, 1, 3, 3) [54.0, 63.0, 72.0, 99.0, 108.0, 117.0, 144.0, 153.0, 162.0]
- **B.** ((1, 1, 3, 3), [12.0, 15.0, 18.0, 21.0, 24.0, 27.0, 30.0, 33.0, 36.0])
- **C.** ((1, 1, 5, 5), [54.0, 63.0, 72.0, 99.0, 108.0, 117.0, 144.0, 153.0, 162.0])
- **D.** ((1, 1, 3, 3), [54.0, 99.0, 144.0, 63.0, 108.0, 153.0, 72.0, 117.0, 162.0])

## 口述答案

答案是 **A. (1, 1, 3, 3) [54.0, 63.0, 72.0, 99.0, 108.0, 117.0, 144.0, 153.0, 162.0]**，实际输出 `(1, 1, 3, 3) [54.0, 63.0, 72.0, 99.0, 108.0, 117.0, 144.0, 153.0, 162.0]`。

5×5 输入经 3×3 卷积（无 padding）变 3×3；权重全 1 时输出是每个 3×3 窗口的和，按行序得 [54,63,72, 99,108,117, 144,153,162]。

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
