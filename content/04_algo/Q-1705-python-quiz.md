---
id: Q-1705
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 12 题）
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
d = {"a": 1}
print(d.get("b", 0), d.get("a"), len(d))
```

- **A.** 0 1 1
- **B.** None 1 1
- **C.** 0 1 2
- **D.** 1 1 1

## 口述答案

答案是 **A. 0 1 1**，实际输出 `0 1 1`。

get 找不到键返回默认值（这里是 0），不会像 d["b"] 那样抛 KeyError；len(d) 是键的个数，此时仍是 1（get 不会插入键）。

## 讲深一层

讲深一层：get 只读不写，缺键返回默认值且 len 不变；想「缺就写入」要用 setdefault(k,v)，它会插入并返回该值。默认值参数在调用前就求值，d.get(k, heavy()) 即使命中键也会白算一次，需要惰性就用 try 或 defaultdict。d["b"] 则抛 KeyError。

## 高频追问

1. **get 和 setdefault 区别？** —— get 不改字典，setdefault 缺键时插入并返回默认值。
2. **怎么让缺键自动建列表？** —— defaultdict(list)，直接 `d[k].append(x)`。
3. **get 的默认值能是可变对象吗？** —— 能但不建议，同一个 list 会被多处共享，容易串数据。

## 易错点

- 以为 get 会写入默认值：后续 d["b"] 仍抛 KeyError，len 还是 1
- 不传默认值就当 0：d.get("b") 返回 None，参与加法抛 TypeError
- 用 d["b"] 代替 get：直接抛 KeyError，整段输出变成异常信息

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
