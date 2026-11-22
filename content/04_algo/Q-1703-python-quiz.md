---
id: Q-1703
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 10 题）
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
print("abc".upper(), "A,B".split(","), "  x ".strip())
```

- **A.** ABC ['A', 'B'] x
- **B.** ABC ('A', 'B') x
- **C.** abc ['A', 'B'] x
- **D.** ABC ['A,B'] 'x'

## 口述答案

答案是 **A. ABC ['A', 'B'] x**，实际输出 `ABC ['A', 'B'] x`。

split 无参时按空白切分，传了分隔符就按分隔符切，返回列表；strip 只去掉两端空白。

## 讲深一层

讲深一层：str 不可变，所有方法都返回新串。split() 不带参按连续空白切并丢掉空串，"a  b".split() 得 ['a','b']；给了分隔符就严格按它切且保留空字段，"a,,b".split(",") 得 ['a','','b']。strip 删的是两端属于该字符集合的字符，不是删子串。

## 高频追问

1. **split() 和 split(" ") 区别？** —— 前者合并连续空白并去空串，后者每个空格都切、会产生空串。
2. **怎么去掉所有空白？** —— `"".join(s.split())` 或 `re.sub(r"\s+","",s)`。
3. **大小写相关方法有哪些？** —— upper/lower/title/capitalize/casefold，casefold 更适合国际化比较。

## 易错点

- 以为 strip 会改原串：调用后不赋值，s 仍是 "  x "
- 以为 split(",") 会丢空字段："a,,b" 得到 ['a','','b']，长度是 3
- 把 strip 当删除子串："abxba".strip("ab") 得 "x"，不是只删前后缀各一次

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
