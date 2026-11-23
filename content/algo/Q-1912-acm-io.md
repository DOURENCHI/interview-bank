---
id: Q-1912
title: Python 读到文件结束怎么写？
module: algo
sub: ACM 读写
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

**输入**：多组数据，每组一行两个整数，直到文件结束。
**输出**：每组输出 `a+b`。

```
输入样例
1 2
3 4

输出样例
3
7
```

## 口述答案

```python
import sys

def main():
    out = []
    for line in sys.stdin:                 # 逐行迭代，读到 EOF 自然结束
        line = line.strip()
        if not line:
            continue                        # 跳过空行
        a, b = map(int, line.split())
        out.append(str(a + b))
    sys.stdout.write("\n".join(out))

main()
```

## 讲深一层

`for line in sys.stdin` 是最 Pythonic 的读法：它按行迭代，遇到 EOF 自动停，不抛异常。比 `while True: input()` 加 `try/except EOFError` 干净得多。

几个常见变体：

| 题面 | 写法 |
|---|---|
| 直到文件结束 | `for line in sys.stdin:` |
| 第一行是组数 | `t = int(input()); for _ in range(t):` |
| 以 `0 0` 结束 | 循环里判断 `if a == 0 and b == 0: break` |
| 读到空行为止 | `while True: line = input(); if not line: break` |

注意 `for line in sys.stdin` 读到空行时 `line` 是 `'\n'`，`strip()` 后变空串——**空行不是 EOF**，要自己判断。

## 高频追问

1. **`sys.stdin` 能迭代几次？** —— 只能一次。它是流，读完就没了。要复用先 `readlines()`。
2. **`input()` 版的 EOF 怎么处理？** —— `try: ... except EOFError: break`，比迭代版啰嗦。
3. **输出为什么要先攒起来？** —— 每行 `print` 都是一次写操作，攒起来一次性 `write` 快很多。

## 易错点

- ❌ 用 `while True` 不加 break 条件 —— 死循环
- ❌ 把空行当 EOF —— 提前退出
- ❌ 每组都 `print` —— 数据量大时慢

## 关联项目

无。

## 来源

文件对象迭代协议
