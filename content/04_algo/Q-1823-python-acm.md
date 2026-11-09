---
id: Q-1823
title: 算法：二分查找与排序查找 的 ACM 输入输出怎么写？
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
def bsearch(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


a = [1, 3, 5, 7, 9, 11, 13, 15]
for t in (11, 4):
    print("找", t, "->", bsearch(a, t))

import bisect

print("bisect_left 找 9 ->", bisect.bisect_left(a, 9))
print("bisect_left 找 10 ->", bisect.bisect_left(a, 10))
print("插入位置（保持有序）", bisect.insort(a, 10), "->", a)
```

输出样例：

```
找 11 -> 5
找 4 -> -1
bisect_left 找 9 -> 4
bisect_left 找 10 -> 5
插入位置（保持有序） None -> [1, 3, 5, 7, 9, 10, 11, 13, 15]
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
