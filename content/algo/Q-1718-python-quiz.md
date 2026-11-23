---
id: Q-1718
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 25 题）
module: algo
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
print([i for i in range(5) if i % 2 == 0], {i: i * i for i in range(3)})
```

- **A.** [0, 2, 4] {0: 0, 1: 1, 2: 4}
- **B.** [0, 2, 4] {0: 0, 1: 1, 2: 8}
- **C.** [1, 3] {0: 0, 1: 1, 2: 4}
- **D.** [0, 2, 4] {1: 1, 2: 4}

## 口述答案

答案是 **A. [0, 2, 4] {0: 0, 1: 1, 2: 4}**，实际输出 `[0, 2, 4] {0: 0, 1: 1, 2: 4}`。

列表推导式的 if 是过滤条件不是三元表达式；字典推导式是 {键: 值}，键取 i、值取 i*i。

## 讲深一层

讲深一层：for 后面的 if 是过滤，只有条件为真的元素才产出；想要「二选一」得把三元写在 for 之前：`[x if x%2 else -x for x in a]`。字典推导式键重复时后值覆盖前值，`{i%2: i for i in range(4)}` 只剩两个键。Python 3 的推导式有独立作用域，循环变量不会泄漏到外面。

## 高频追问

1. **怎么在推导式里写 if-else？** —— 三元放 for 前面，过滤 if 放 for 后面，位置不能互换。
2. **推导式和生成器表达式区别？** —— 前者立即生成容器，后者惰性、只能迭代一次。
3. **字典键重复会怎样？** —— 后者覆盖前者，长度按去重后算。

## 易错点

- 把 if 写在 for 前面当过滤：`[i if i%2==0 for i in range(5)]` 是语法错误
- 以为 {i:i\*i for i in range(3)} 从 1 开始：从 0 起，含 0:0 这一项
- 用列表推导式处理大数据：立即分配全部内存，应改用生成器表达式

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
