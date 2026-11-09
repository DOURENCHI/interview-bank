---
id: Q-1824
title: 算法：插入排序与内置排序对比 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: draft
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 Python 程序对应的读入与输出写法是什么？

```python
def insertion_sort(a):
    a = list(a)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


data = [5, 2, 4, 6, 1, 3]
print("原数组      ", data)
print("插入排序后  ", insertion_sort(data))
print("sorted() 后 ", sorted(data))
print("原数组未被修改", data)

print("sorted 关键字参数", sorted([3, 1, 2], key=lambda x: -x))
print("sorted 带下标", sorted([(2, "b"), (1, "a")], key=lambda p: p[0]))
```

输出样例：

```
原数组       [5, 2, 4, 6, 1, 3]
插入排序后   [1, 2, 3, 4, 5, 6]
sorted() 后  [1, 2, 3, 4, 5, 6]
原数组未被修改 [5, 2, 4, 6, 1, 3]
sorted 关键字参数 [3, 2, 1]
sorted 带下标 [(1, 'a'), (2, 'b')]
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
