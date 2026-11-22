---
id: Q-1739
title: 这段 Python 代码输出什么？（02 NumPy 与张量基础 · 第 46 题）
module: 04_algo
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
import numpy as np
f = np.array([3.7, -2.2, 5.0])
print(np.floor(f).tolist(), np.ceil(f).tolist(), np.abs(f).tolist())
```

- **A.** [3.0, -3.0, 5.0] [4.0, -2.0, 5.0] [3.7, 2.2, 5.0]
- **B.** [3.0 -2.0 5.0] [4.0 -2.0 5.0] [3.7 2.2 5.0]
- **C.** [4.0 -2.0 5.0] [3.0 -3.0 5.0] [3.7 2.2 5.0]
- **D.** [3.0 -2.0 5.0] [4.0 -2.0 5.0] [-3.7 2.2 5.0]

## 口述答案

答案是 **A. [3.0, -3.0, 5.0] [4.0, -2.0, 5.0] [3.7, 2.2, 5.0]**，实际输出 `[3.0, -3.0, 5.0] [4.0, -2.0, 5.0] [3.7, 2.2, 5.0]`。

floor 向负无穷取整（-2.2 → -3），ceil 向正无穷取整（-2.2 → -2）；abs 保留原符号去掉负号，-2.2 → 2.2。

## 讲深一层

讲深一层：floor 向负无穷、ceil 向正无穷、trunc/int 向零，三者只在负数上分道：-2.2 分别得 -3.0、-2.0、-2。np.floor 返回的仍是浮点数组（3.0 而非 3），dtype 不因取整而改变；要整数得再 astype(int)。对 -0.0，abs 得 0.0，符号位被清掉但打印看不出差异。

## 高频追问

1. **floor 和 int 对负数区别？** —— -3.0 vs -2，方向不同。
2. **怎么取整成 int 数组？** —— `np.floor(f).astype(int)`。
3. **ceil(-2.2) 为什么是 -2？** —— 向正无穷取整，-2 大于 -2.2。

## 易错点

- 把 floor(-2.2) 算成 -2：那是向零截断，floor 应得 -3.0
- 以为 floor 返回 int：仍是 float，输出 3.0
- 把 ceil 和 floor 记反：-2.2 的 ceil 是 -2，不是 -3

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 02 NumPy 与张量基础
