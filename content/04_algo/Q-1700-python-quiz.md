---
id: Q-1700
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 7 题）
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
a = [1, 2, 3]
try:
    print(a[3])
except IndexError as e:
    print("IndexError")
```

- **A.** 3
- **B.** IndexError
- **C.** None
- **D.** []

## 口述答案

答案是 **B. IndexError**，实际输出 `IndexError`。

越界访问会抛 IndexError 而不是返回 None，必须靠 try/except 捕获——这是 Python 与 C++ 数组最大的行为差异之一。

## 讲深一层

讲深一层：越界一律抛 IndexError，包括负向越界 a[-4]；但切片 a[3:5] 不抛，返回 []。字典取不存在的键抛 KeyError，两者同属 LookupError。C++ 的 vector::operator[] 越界是未定义行为、可能静默读到脏数据，Python 用异常把错误显式化，except 应精确捕获。

## 高频追问

1. **怎么安全取值？** —— 先判 `if i < len(a)`，或用 `a[i:i+1]` 切片返回空列表。
2. **except 只写 Exception 行不行？** —— 行但过宽，会吞掉拼写错误等逻辑异常，应精确到 IndexError。
3. **字典越界抛什么？** —— KeyError，用 d.get(k) 或 defaultdict 规避。

## 易错点

- 以为越界返回 None：实际抛出未捕获的 IndexError，程序直接终止并打印 Traceback
- 用 a[3:4] 以为也会抛：切片不报错，返回 []，容易误判成「取到空值」
- 捕获 Exception 掩盖真错：把变量名拼错也一并吞掉，应写 except IndexError

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
