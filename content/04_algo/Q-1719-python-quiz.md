---
id: Q-1719
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 26 题）
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
print(isinstance(1, int), isinstance(True, int), isinstance("a", str))
```

- **A.** True True True
- **B.** True False True
- **C.** False True True
- **D.** True True False

## 口述答案

答案是 **A. True True True**，实际输出 `True True True`。

bool 是 int 的子类（Python 里 True 本质就是 1），所以 isinstance(True, int) 为 True——这是很多 if 判断写错的根源。

## 讲深一层

讲深一层：bool 继承 int，True/False 就是 1/0 的子类实例，所以 isinstance(True,int) 为 True、True+True 得 2；但 type(True) 是 bool，精确判断不受影响。用 isinstance(x,int) 校验会把布尔放进来，要排除得再判 type(x) is not bool。

## 高频追问

1. **怎么区分 True 和 1？** —— `type(x) is bool`，或 `x is True`。
2. **为什么 isinstance 认 bool 为 int？** —— bool 是 int 的子类，按继承链匹配。
3. **isinstance 和 type 的差异？** —— isinstance 支持继承与 ABC，type 只认精确类型。

## 易错点

- 用 type(x)==int 判整数却收到 True：返回 False，漏掉布尔
- 以为 isinstance(True,int) 是 False：实际 True，因为 bool 继承 int
- 把 isinstance 第二参写成字符串：抛 TypeError，要传类型或类型元组

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
