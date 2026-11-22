---
id: Q-1724
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 31 题）
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
a = [1, 2]
d = {"k": 1}
a.append(3)
d["k2"] = 2
print(a, d)
```

- **A.** [1, 2, 3] {'k': 1, 'k2': 2}
- **B.** [1, 2, 3] {'k': 1}
- **C.** [1, 2] {'k': 1, 'k2': 2}
- **D.** [3, 1, 2] {'k': 1, 'k2': 2}

## 口述答案

答案是 **A. [1, 2, 3] {'k': 1, 'k2': 2}**，实际输出 `[1, 2, 3] {'k': 1, 'k2': 2}`。

list 和 dict 是可变对象，append 与字典赋值都是原地修改，不产生新对象。

## 讲深一层

讲深一层：list、dict、set 可变，append 与 d[k]=v 都是原地修改，对象 id 不变，所有指向它的名字都会看到新内容。str、tuple、int 不可变，「修改」只会新建对象并重新绑定名字。函数传参传的是对象引用，所以在函数里 append 会影响调用方，而 `a = a + [3]` 只是局部重绑定，外面看不到。

## 高频追问

1. **怎么判断原地还是新建？** —— 看 id 是否变化，或用 `a is b` 比较。
2. **函数里改列表会影响外面吗？** —— 会，引用同一对象；重新赋值则不会。
3. **浅拷贝够吗？** —— 一层够；嵌套结构要用 copy.deepcopy。

## 易错点

- 以为 a.append(3) 有返回值：返回 None，写 `a=a.append(3)` 后 a 变 None
- 以为函数内 d["x"]=1 不影响外部：字典是引用，外部会看到修改
- 用 `b=a` 当拷贝：两者同一对象，改 b 等于改 a

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
