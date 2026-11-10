---
id: Q-1812
title: 手写梯度下降：w 一步步走向 2.0 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: indexed
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
xs = [1.0, 2.0, 3.0]
ys = [2.0, 4.0, 6.0]


def cost(w):
    return sum((x * w - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def grad(w):
    return sum(2 * x * (x * w - y) for x, y in zip(xs, ys)) / len(xs)


w = 1.0
print(f"初始 w={w:.4f} cost={cost(w):.4f} grad={grad(w):.4f}")
for step in range(100):
    g = grad(w)
    w -= 0.01 * g
    if step < 3 or step % 25 == 0:
        print(f"Epoch {step}: w={w:.4f} cost={cost(w):.4f}")
print(f"最终 w={w:.4f}（真实值 2.0）")
```

输出样例：

```
初始 w=1.0000 cost=4.6667 grad=-9.3333
Epoch 0: w=1.0933 cost=3.8362
Epoch 1: w=1.1780 cost=3.1535
Epoch 2: w=1.2547 cost=2.5923
Epoch 25: w=1.9217 cost=0.0286
Epoch 50: w=1.9932 cost=0.0002
Epoch 75: w=1.9994 cost=0.0000
最终 w=1.9999（真实值 2.0）
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

`教学文档/Python实验台/Python考点实验台.html` · 04 线性模型与梯度下降
