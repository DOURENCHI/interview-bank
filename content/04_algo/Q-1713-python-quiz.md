---
id: Q-1713
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 20 题）
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
print(10 // 3, 10.0 // 3, int(10 / 3))
```

- **A.** 3 3.0 3
- **B.** 3 3.3 3
- **C.** 4 3.0 3
- **D.** 3 3.0 4

## 口述答案

答案是 **A. 3 3.0 3**，实际输出 `3 3.0 3`。

10.0 // 3 的结果是 float 3.0（// 保留浮点类型）；int(10/3) 截断小数部分得 3。注意 10 / 3 = 3.333…，不是 3.33。

## 讲深一层

讲深一层：// 的结果类型跟随操作数——两边都是 int 得 int，只要有一个 float 就得 float，所以 10.0//3 是 3.0。取整方向是向下（floor），而 int() 是向零截断：int(-3.7) 得 -3，-3.7//1 得 -4.0，负数场景两者不同。int(10/3) 先做真除法得 3.333… 再截断，故为 3。

## 高频追问

1. **int(-3.7) 和 -3.7//1 一样吗？** —— -3 和 -4.0，截断与向下取整不同。
2. **怎么四舍五入到整数？** —— round(x)，注意银行家舍入。
3. **为什么 10.0//3 是 3.0？** —— 有 float 参与，结果保持 float。

## 易错点

- 以为 // 总返回 int：10.0//3 输出 3.0，写成 3 就错
- 用 int() 代替 // 处理负数：int(-3.7) 得 -3，floor 应得 -4
- 把 10/3 记成 3.33：实际是 3.3333333333333335

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
