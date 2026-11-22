---
id: Q-1717
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 24 题）
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
print((lambda x: x * 2)(5), (lambda x, y=3: x + y)(1))
```

- **A.** 10 4
- **B.** 10 3
- **C.** 5 4
- **D.** 10 1

## 口述答案

答案是 **A. 10 4**，实际输出 `10 4`。

lambda 是匿名函数，默认参数 y=3 让第二个调用只传 1 也成立，结果 1+3=4。

## 讲深一层

讲深一层：lambda 体只能是单个表达式，其值即返回值，不能写 return、赋值或语句块。默认参数在定义时求值并绑定，而闭包变量延迟绑定，所以 [lambda: i for i in range(3)] 三个函数都返回 2；要固定得写 lambda i=i: i。它主要给 key/sorted/map 传短函数。

## 高频追问

1. **lambda 能有多个参数吗？** —— 能，`lambda x,y=3: x+y`，也支持 *args/**kw。
2. **循环里创建 lambda 为什么都返回同一个值？** —— 闭包按名延迟绑定，循环结束后 i 是最后一个值。
3. **lambda 和 def 区别？** —— 表达式 vs 语句，lambda 无名字、无文档字符串，调试栈里都叫 <lambda>。

## 易错点

- 给 lambda 写 return：语法错误 SyntaxError，lambda 体只能是表达式
- 循环里用 lambda 捕获 i 不绑定默认值：三个函数全返回 2 而非 0,1,2
- 以为 (lambda x: x*2) 直接得 10：不调用只是函数对象，必须加 (5)

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
