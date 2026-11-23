---
id: Q-1777
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 84 题）
module: algo
sub: 容器与切片
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
p = torch.tensor([0.2, 0.7, 0.1])
print(round(float(torch.argmax(p)), 6), float(p[1]))
```

- **A.** 1.0 0.699999988079071
- **B.** (0.0, 0.2)
- **C.** (2.0, 0.1)
- **D.** (1.0, 0.7)

## 口述答案

答案是 **A. 1.0 0.699999988079071**，实际输出 `1.0 0.699999988079071`。

argmax 给下标 1；float32 张量里 0.7 的实际值是 0.699999988079071——这就是为什么打印要用 .6f 之类取整，别直接比相等。

## 讲深一层

`argmax` 返回 int64 下标张量，`float()` 转成 `1.0`；有并列最大值时返回第一个。`0.7` 在 float32 里的实际值是 0.699999988079071，因为 0.7 的二进制是无限循环小数。这也解释了为什么浮点比较要用 `torch.allclose` 或先 round，直接 `==` 判等几乎必然失败。

## 高频追问

1. **`argmax` 和 `max` 的区别？** —— `argmax` 只给下标，`max` 返回值本身（还能返回下标元组）
2. **有并列最大值返回哪个？** —— 第一个，CPU 上保证，GPU 上不保证顺序
3. **为什么打印出 `0.699999988`？** —— float32 只有 24 位有效位，0.7 无法精确表示，转 Python float 后暴露误差

## 易错点

- 用 `== 0.7` 判断——得 False，正确写法是 `abs(p[1]-0.7) < 1e-6`
- 把 `argmax` 当最大值——会答 0.7 而不是下标 1
- 以为 `torch.tensor([0.2,0.7,0.1])` 是 float64——浮点字面量默认 float32，误差正是由此而来

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
