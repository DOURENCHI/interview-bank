---
id: Q-1726
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 33 题）
module: algo
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
def outer():
    x = 1
    def inner():
        nonlocal x
        x += 1
        return x
    return inner(), x
print(outer())
```

- **A.** (2, 2)
- **B.** (1, 2)
- **C.** (2, 1)
- **D.** (1, 1)

## 口述答案

答案是 **A. (2, 2)**，实际输出 `(2, 2)`。

nonlocal 把内层作用域的 x 绑定到外层函数的变量，inner() 把 x 改成 2，所以 (inner() 的返回值, 当时的 x) 都是 2。

## 讲深一层

讲深一层：nonlocal 把名字绑定到最近的外层函数作用域（不是全局），只在该层已存在该变量时合法。删掉 nonlocal 后 x += 1 会让 x 在整个 inner 里成为局部变量，读取时尚未赋值，抛 UnboundLocalError。`return inner(), x` 从左到右求值，先调用改 x 为 2，再读 x 得 2，所以是 (2,2)。

## 高频追问

1. **nonlocal 和 global 区别？** —— nonlocal 找外层函数，global 找模块级。
2. **不用 nonlocal 会怎样？** —— UnboundLocalError: cannot access local variable 'x'。
3. **为什么返回 (2,2) 不是 (2,1)？** —— 元组元素从左到右求值，x 已被改。

## 易错点

- 漏写 nonlocal 直接 x+=1：抛 UnboundLocalError，没有任何输出
- 把 nonlocal 写成 global：模块级没有 x，x+=1 抛 NameError
- 以为 return 先算 x 再调 inner：求值顺序从左到右，实际先调用后取值

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
