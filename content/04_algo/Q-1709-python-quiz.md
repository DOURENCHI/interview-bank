---
id: Q-1709
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 16 题）
module: 04_algo
sub: 语法与类型
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
print(list(range(2, 8, 2)), list(range(3)), len(list(range(0, 10, 3))))
```

- **A.** [2, 4, 6] [0, 1, 2] 4
- **B.** [2, 4, 6, 8] [0, 1, 2] 4
- **C.** [2, 4, 6] [0, 1, 2] 3
- **D.** [2, 4, 6] [1, 2, 3] 4

## 口述答案

答案是 **A. [2, 4, 6] [0, 1, 2] 4**，实际输出 `[2, 4, 6] [0, 1, 2] 4`。

range(2, 8, 2) 左闭右开取到 7 所以是 [2,4,6]；range(0,10,3) 有 0/3/6/9 四个数，长度 4。

## 讲深一层

讲深一层：range 是惰性序列而非列表，只存 start/stop/step 三个数，len 和 in 都是 O(1) 计算，不占元素内存。区间恒为左闭右开，所以 range(2,8,2) 到 6 就停。step 为负时同样左闭右开：range(5,0,-1) 得 5,4,3,2,1。step=0 抛 ValueError，参数也不接受浮点。

## 高频追问

1. **range 和 list(range) 区别？** —— range 惰性省内存，list 立即展开全部元素。
2. **range(0,10,3) 为什么是 4 个？** —— 0,3,6,9，个数为 (stop-start+step-1)//step。
3. **怎么倒序循环？** —— `range(n-1,-1,-1)` 或 `reversed(range(n))`。

## 易错点

- 把 range(2,8,2) 写成含 8：左闭右开，实际 [2,4,6] 三个元素
- 以为 range(3) 是 1,2,3：从 0 起，是 0,1,2
- 用浮点步长 range(0,1,0.1)：抛 TypeError，需用 numpy.arange 或整数缩放

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
