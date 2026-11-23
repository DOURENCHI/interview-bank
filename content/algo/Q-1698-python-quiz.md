---
id: Q-1698
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 5 题）
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
print([1, 2, 3] + [4], [1, 2] * 2, 5 in [1, 2, 3])
```

- **A.** [1, 2, 3, 4] [1, 2, 1, 2] False
- **B.** [1, 2, 3, 4] [1, 2, 1, 2] True
- **C.** [1, 2, 3, 4] [1, 2] False
- **D.** [1, 2, 3, 4] [1, 2, 1, 2] TypeError

## 口述答案

答案是 **A. [1, 2, 3, 4] [1, 2, 1, 2] False**，实际输出 `[1, 2, 3, 4] [1, 2, 1, 2] False`。

列表相加是拼接、乘法是重复（不是幂）；in 是成员判断，5 不在 [1,2,3] 里所以 False。

## 讲深一层

讲深一层：list 的 + 和 * 都返回新列表，不修改原对象；* 是浅复制，`[[0]]*3` 的三行是同一个内层列表，改一行三行全变。+ 要求两边都是 list，`[1,2]+(3,)` 直接 TypeError。in 用 == 逐个比较，所以 `1 in [1.0]` 为 True。`a += b` 是原地扩展，与 `a = a + b` 的对象身份不同。

## 高频追问

1. **[1,2]\*2 和 numpy 的 \*2 区别？** —— list 是重复元素，ndarray 是逐元素相乘。
2. **怎么安全构造二维列表？** —— `[[0]*3 for _ in range(3)]` 或 copy.deepcopy，别用 `[[0]*3]*3`。
3. **tuple 支持 + 和 \* 吗？** —— 支持，同样返回新元组；但 `*=` 对不可变对象等价于重新绑定。

## 易错点

- 把 `[1,2]*2` 当成平方或 `[2,4]`：实际是 `[1, 2, 1, 2]`
- 认为 `[1,2,3]+4` 能追加：抛 TypeError，追加要用 append 或 `+[4]`
- 用 `[[0]]*3` 建二维表：三行同一对象，改 `[0][0]` 后三行全变

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
