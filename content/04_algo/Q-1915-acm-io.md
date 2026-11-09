---
id: Q-1915
title: Python 要读一整行（含空格），怎么写？
module: 04_algo
sub: Python 读写
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 机考 ACM 模式通用写法整理
verified_at: 2026-11-09
tags: [ACM, 输入输出, 机考, Python 读写]
auto: true
acm_seed: true
---

## 题目

**输入**：第一行 `n`；随后 `n` 行，每行一个可能含空格的句子。
**输出**：逐行原样输出，前面加行号。

```
输入样例
2
hello world
foo bar baz

输出样例
1: hello world
2: foo bar baz
```

## 口述答案

```python
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    for i in range(1, n + 1):
        s = input().rstrip("\n")        # 只去换行，保留行内空格
        print(f"{i}: {s}")

main()
```

## 讲深一层

关键区别：`split()` 会把空格当分隔符**吃掉**，`rstrip("\n")` 只去掉行尾换行符，行内空格完整保留。

对比三种去空白方式：

| 写法 | 行为 | 什么时候用 |
|---|---|---|
| `s.rstrip("\n")` | 只去尾部换行 | **读整行内容时** |
| `s.strip()` | 去首尾所有空白（含空格） | 读数字/单 token 时 |
| 不去 | 保留 `\n` | 几乎从不 |

如果一行里既有空格又不能用 `split()`，就得手工截取——比如「名字 + 一串数字」这种混合格式。

## 高频追问

1. **`rstrip("\n")` 和 `rstrip()` 有区别吗？** —— 有。不带参数会去掉**所有**尾部空白，包括有意义的前导/尾随空格。读文本时必须带参数。
2. **`input()` 要不要再 `rstrip`？** —— 不用，`input()` 已经去掉行尾换行。但它不能用在需要保留行尾空格的场景（极少）。
3. **Windows 下读到 `\r\n` 怎么办？** —— `rstrip("\r\n")` 两个都去掉。

## 易错点

- ❌ 用 `split()[0]` 取整行 —— 只拿到第一个词
- ❌ 用 `strip()` 读句子 —— 句首句尾的空格被吃掉
- ❌ 忘了 `int(input())` 后行位置 —— `readline` 不会多读，这里安全

## 关联项目

无。

## 来源

`str.rstrip` 与 `input()` 语义
