---
id: Q-1821
title: 算法：双指针原地移除元素 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: indexed
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
def remove_element(nums, val):
    """原地移除所有等于 val 的元素，返回新长度。"""
    k = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    return k


a = [0, 1, 2, 2, 3, 0, 4, 2]
k = remove_element(a, 2)
print("新长度", k)
print("有效前缀", a[:k])
print("尾部是残留值，不用管", a[k:])
```

输出样例：

```
新长度 5
有效前缀 [0, 1, 3, 0, 4]
尾部是残留值，不用管 [0, 4, 2]
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
