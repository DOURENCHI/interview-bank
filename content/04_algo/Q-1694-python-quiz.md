---
id: Q-1694
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 1 题）
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
print(type(3), type(3.0), type("a"), type([1]))
```

- **A.** <class 'int'> <class 'float'> <class 'str'> <class 'list'>
- **B.** <class 'int'> <class 'float'> <class 'str'> <class 'tuple'>
- **C.** <class 'int'> <class 'double'> <class 'str'> <class 'list'>
- **D.** <class 'number'> <class 'float'> <class 'str'> <class 'array'>

## 口述答案

答案是 **A. <class 'int'> <class 'float'> <class 'str'> <class 'list'>**，实际输出 `<class 'int'> <class 'float'> <class 'str'> <class 'list'>`。

Python 里 int / float / str / list 都是内置类型，浮点数只有一种 float（没有 double），列表是 list，元组才是 tuple。

## 讲深一层

讲深一层：type(x) 返回精确类型而不是父类，所以 type(True) 是 <class 'bool'> 而非 int，这与 isinstance 相反。想拿短名字用 type(x).__name__。几个值用逗号分隔传给 print，输出之间自动补一个空格。换成 numpy 标量会打印 <class 'numpy.int64'>。

## 高频追问

1. **type 和 isinstance 的区别？** —— type 要求精确相等，isinstance 认继承链，所以 isinstance(True,int) 为 True。
2. **怎么判断一个变量是不是数字？** —— isinstance(x,(int,float))，注意 bool 也会命中 int。
3. **type(3) == int 成立吗？** —— 成立，类对象唯一，`is` 比较也为 True。

## 易错点

- 以为 Python 有 double：写 type(3.0) 期待 <class 'double'>，实际是 float
- 把 list 和 tuple 记反：type([1]) 是 list，type((1,)) 才是 tuple
- 用 type 判继承：type(True)==int 得 False，应该改用 isinstance

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
