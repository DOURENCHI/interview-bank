---
id: Q-1759
title: 这段 Python 代码输出什么？（04 线性模型与梯度下降 · 第 65 题）
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
xs = [1.0, 2.0, 3.0]
ys = [2.0, 4.0, 6.0]
def grad(w):
    return sum(2 * x * (x * w - y) for x, y in zip(xs, ys)) / len(xs)
def cost(w):
    return sum((x * w - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
print(grad(2.0), cost(2.0))
```

- **A.** 0.0 0.0
- **B.** (0.0, 14.0)
- **C.** (6.0, 0.0)
- **D.** (0.0, 1.0)

## 口述答案

答案是 **A. 0.0 0.0**，实际输出 `0.0 0.0`。

w=2 正好是数据的真实斜率，预测全对：梯度为 0（不再需要调整），代价为 0。梯度为 0 就是收敛的判据。

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

`教学文档/Python实验台/Python考点实验台.html` · 04 线性模型与梯度下降
