---
id: Q-1761
title: 这段 Python 代码输出什么？（04 线性模型与梯度下降 · 第 67 题）
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
def grad(w):
    return sum(2 * x * (x * w - y) for x, y in zip(xs, ys)) / len(xs)
def cost(w):
    return sum((x * w - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
for _ in range(10):
    w -= 1.0 * grad(w)
print(round(w, 4), round(cost(w), 4))
```

- **A.** -1615055826.8985 1.2172558208808118e+19
- **B.** (-1.6151, 2.0)
- **C.** (0.0, 0.0)
- **D.** (1.0, 4.6667)

## 口述答案

答案是 **A. -1615055826.8985 1.2172558208808118e+19**，实际输出 `-1615055826.8985 1.2172558208808118e+19`。

学习率从 0.01 放大到 1.0 后步子太大直接发散：w 变成天文数字、代价爆炸。梯度下降必须配足够小的学习率。

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
