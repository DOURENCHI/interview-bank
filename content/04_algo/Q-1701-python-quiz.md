---
id: Q-1701
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 8 题）
module: 04_algo
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
print(round(2.675, 2), round(0.5), round(1.5), round(-0.5))
```

- **A.** 2.67 0 2 0
- **B.** 2.68 0 2 -1
- **C.** 2.67 1 2 0
- **D.** 2.67 0 1 0

## 口述答案

答案是 **A. 2.67 0 2 0**，实际输出 `2.67 0 2 0`。

round 是「四舍六入五成双」（银行家舍入）：0.5→0、1.5→2、-0.5→0；2.675 的真实二进制值略小于 2.675，所以结果是 2.67。

## 讲深一层

讲深一层：round 采用 round-half-to-even，恰好 .5 时向偶数靠：round(2.5)=2、round(3.5)=4、round(-2.5)=-2，批量舍入的期望偏差更小。省掉第二个参数返回 int，给了 ndigits 返回 float。2.675 二进制里是 2.67499999…，所以得 2.67。

## 高频追问

1. **想要真正的四舍五入怎么办？** —— `Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`。
2. **round(2.5) 和 round(3.5) 各是多少？** —— 2 和 4，都落到偶数。
3. **为什么 2.675 舍成 2.67？** —— 二进制无法精确表示，实际存储值略小于 2.675。

## 易错点

- 按「四舍五入」算 round(0.5) 得 1：实际是 0，银行家舍入进偶数
- 以为 round(2.675,2) 是 2.68：二进制误差使其为 2.67
- 以为 round(x,2) 返回字符串：返回 float，末尾 0 不保留，2.50 显示成 2.5

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
