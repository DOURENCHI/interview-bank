---
id: Q-1727
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 34 题）
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
counter = {"n": 0}
def bump():
    counter["n"] += 1
    return counter["n"]
print(bump(), bump(), counter["n"])
```

- **A.** 1 2 2
- **B.** 1 1 1
- **C.** 1 2 3
- **D.** 0 1 1

## 口述答案

答案是 **A. 1 2 2**，实际输出 `1 2 2`。

可变对象作为全局变量时函数内的修改会生效，字典内容被就地累加；第三次打印仍是 2，因为 counter 里存的就是 2。

## 讲深一层

讲深一层：函数内 `counter["n"] += 1` 只做「取下标、加、写回」，从未给名字 counter 赋值，所以不需要 global；一旦写 `counter = {...}`，counter 立刻变局部名，外部字典不受影响。真正需要 global 的是重新绑定模块级名字。+= 在字典上是读-改-写三步，多线程下并非原子。

## 高频追问

1. **什么时候必须写 global？** —— 在函数内给模块级名字重新赋值时。
2. **为什么改字典内容不用 global？** —— 没有发生名字绑定，只是对象内部状态变化。
3. **多线程自增安全吗？** —— 不安全，counter["n"]+=1 非原子，要加锁。

## 易错点

- 在函数里写 counter = {"n":0} 想重置：变成局部变量，外部字典不变
- 以为必须加 global 才能改字典：加了不报错但非必需，关键是区分改内容与改名字
- 把 += 当原子操作：并发下会丢更新，最终值小于调用次数

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
