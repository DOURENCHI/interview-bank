---
id: Q-1711
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 18 题）
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
print("%s-%d" % ("a", 5), "{}-{}".format("b", 6), f"c-{7}")
```

- **A.** a-5 b-6 c-7
- **B.** a-5 b-6 c-{7}
- **C.** a-5 b-6 c-8
- **D.** a-%s b-%d c-7

## 口述答案

答案是 **A. a-5 b-6 c-7**，实际输出 `a-5 b-6 c-7`。

三种格式化写法结果一致；f-string 是 3.6+ 的语法糖，{7} 会求值成 7。

## 讲深一层

讲深一层：三种写法语义一致但求值时机不同：% 和 .format 先构造模板再传参，f-string 在编译期就拆成字节码、运行时直接拼接，通常最快。f-string 花括号里是表达式不是字面量，{7} 求值成 7，写 {7+1} 得 8；要输出字面花括号必须写 {{ }}。%d 传字符串会抛 TypeError，f-string 不替你校验类型。

## 高频追问

1. **f-string 里怎么输出花括号？** —— 双写 {{ 和 }}。
2. **怎么保留两位小数？** —— `f"{x:.2f}"`，等价于 "%.2f" % x。
3. **f-string 里能写表达式吗？** —— 能，{a+b}、{d['k']}、{x!r} 都支持。

## 易错点

- 在 f-string 里写 {7} 以为输出 {7}：实际输出 7，要字面量得写 {{7}}
- 用 "%d" % "5"：抛 TypeError，%d 要求数字
- 混用 {} 和 %：`"{} %s".format(x)` 里的 %s 不会被替换，原样输出

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
