---
id: Q-1721
title: 这段 Python 代码输出什么？（01 Python 语言地基 · 第 28 题）
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
print(id(None) == id(None), None is None)
```

- **A.** True True
- **B.** True False
- **C.** False True
- **D.** False False

## 口述答案

答案是 **A. True True**，实际输出 `True True`。

None 是单例，解释器里只有一个，所以 id 相同、is 也为 True——判空推荐写「x is None」。

## 讲深一层

讲深一层：None 是 NoneType 的唯一实例，解释器启动时创建，所以 id(None) 恒定、is 最可靠。它与 0、""、False 都不相等，但布尔值为假，if not x 无法区分「是 None」和「是空值」。None 不支持大小比较，None<0 抛 TypeError；默认参数写 None 是避免可变默认值共享的标准做法。

## 高频追问

1. **判空用 is None 还是 == None？** —— 用 is，绕过 __eq__ 且更快。
2. **None 和 False 区别？** —— 类型不同、== 得 False，但两者布尔值都为假。
3. **函数默认参数为什么写 None？** —— 避免可变默认值在多次调用间共享。

## 易错点

- 用 if not x 判 None：0、""、[] 也会命中，误判成空值
- 写 x == None：对象重写 __eq__ 时可能返回真，且不符合 PEP 8
- 以为 None == False：实际 False，虽然布尔值都为假

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 01 Python 语言地基
