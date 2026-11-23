---
id: Q-1706
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 13 题）
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
print(hash("x") == hash("x"), "x" == "x")
```

- **A.** True True
- **B.** True False
- **C.** False True
- **D.** False False

## 口述答案

答案是 **A. True True**，实际输出 `True True`。

同一字符串的 hash 相同且内容相等，所以两个表达式都是 True；Python 用字典+链表实现哈希表，hash 相等不必然相等，但这里两者都满足。

## 讲深一层

讲深一层：契约是「a == b 必须 hash(a) == hash(b)」，反过来不成立——不同键可哈希碰撞。str 的哈希带每进程随机盐（PYTHONHASHSEED），具体数值跨进程会变，但同一进程内必然相同，本题才稳定为 True。list/dict 不可哈希，因为可变会破坏桶位置；tuple 只含不可变元素时才可哈希。

## 高频追问

1. **为什么字符串哈希每次运行不同？** —— 防哈希碰撞攻击，解释器启动时随机加盐。
2. **自定义类做字典键要注意什么？** —— 实现 __hash__ 和 __eq__，且参与哈希的字段不可变。
3. **hash 冲突了字典怎么办？** —— 同一桶内再用 == 逐个比较，靠探测或链表解决。

## 易错点

- 以为 hash 相等就一定相等：碰撞时 hash(a)==hash(b) 但 a!=b
- 把 hash("x") 的具体数字写进答案：它随进程随机，题目只能问相等性
- 用 list 做 dict 键：直接 TypeError，程序不输出预期结果

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
