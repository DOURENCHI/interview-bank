---
id: Q-1756
title: 这段 Python 代码输出什么？（04 线性模型与梯度下降 · 第 62 题）
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
w = 1.0
cost = sum((x * w - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
grad = sum(2 * x * (x * w - y) for x, y in zip(xs, ys)) / len(xs)
print(round(cost, 4), round(grad, 4))
```

- **A.** 4.6667 -9.3333
- **B.** 4.6667 9.3333
- **C.** 14.0 -28.0
- **D.** 0.0 0.0

## 口述答案

答案是 **A. 4.6667 -9.3333**，实际输出 `4.6667 -9.3333`。

w=1 时预测为 1/2/3，误差 -1/-2/-3，平方和 1+4+9=14 除以 3 得 4.6667；梯度是 loss 对 w 的导数，为负说明增大 w 能减小损失。

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
