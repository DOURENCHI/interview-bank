---
id: Q-1756
title: 这段 Python 代码输出什么？（04 线性模型与梯度下降 · 第 63 题）
module: algo
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
xs = [1.0, 2.0, 3.0]
ys = [2.0, 4.0, 6.0]
w = 1.0
def grad(w):
    return sum(2 * x * (x * w - y) for x, y in zip(xs, ys)) / len(xs)
for _ in range(3):
    w -= 0.01 * grad(w)
def cost(w):
    return sum((x * w - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
print(round(w, 4), round(cost(w), 4))
```

- **A.** 1.2547 2.5923
- **B.** 1.0933 3.8362
- **C.** 1.1800 3.1535
- **D.** 0.7 0.49

## 口述答案

答案是 **A. 1.2547 2.5923**，实际输出 `1.2547 2.5923`。

每步 w -= 0.01 × 梯度：梯度为负所以 w 增大。三步后 w≈1.2547，代价从 4.6667 降到 2.5923。

## 讲深一层

更新式 `w ← w − lr·g`，初始 g=−9.3333，lr=0.01 第一步只挪 0.0933。该问题 Hessian 是 `28/3≈9.33`，稳定条件 `lr < 0.214`。误差每步按 `1−0.0933≈0.907` 衰减，三步到 1.2547，离 2.0 还远。

## 高频追问

1. **为什么不一步到 2.0？** —— 梯度下降是迭代逼近，步长受 lr 限制；只有闭式解能一步到位
2. **lr 取 0.2 会怎样？** —— 接近 2/9.33 的临界值，误差乘子接近 −0.87，来回震荡不收敛
3. **cost 为什么从 4.6667 降到 2.5923？** —— w 从 1 靠近 2，三个样本误差同步缩小，平方和从 14 降到 7.78

## 易错点

- 把 lr 漏掉写成 `w -= grad(w)`——这就是 Q-1760 的发散场景，w 会冲到 −1.6e9
- 每轮用更新前的 w 算 cost——cost 滞后一步，末值对不上 2.5923
- 循环次数数错（写成 4 次）——w≈1.324、cost≈2.13，落到选项之外

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 04 线性模型与梯度下降
