---
id: Q-1916
title: Python 输出要求空格分隔且行末不能有空格，怎么写？
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

**输入**：`n` 个整数。
**输出**：原样输出，数与数之间一个空格，**行末无空格**。

```
输入样例
3
1 2 3

输出样例
1 2 3
```

## 口述答案

```python
import sys

def main():
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))[:n]

    print(" ".join(map(str, a)))                 # 推荐：天然无行末空格
    # print(*a)                                  # 也行，sep 默认就是空格
    # print(*a, sep=" ")                         # 显式写法

main()
```

## 讲深一层

Python 在这件事上比 C++ 省心：`' '.join(...)` 由分隔符**连接**元素，天然不会在末尾留下分隔符。

`print(*a)` 是把列表展开成位置参数，`sep` 默认就是空格，效果一样。两者选择：

| 写法 | 适用 |
|---|---|
| `' '.join(map(str, a))` | 元素需要转换或格式化时 |
| `print(*a)` | 元素已是字符串或直接可打印时，最简洁 |
| `print(*a, sep=", ")` | 自定义分隔符 |

注意 `print` 默认在末尾加 `\n`，如果题面要求「最后一行不换行」，要 `print(..., end="")`。

## 高频追问

1. **元素是浮点要保留两位怎么办？** —— `' '.join(f"{x:.2f}" for x in a)`。
2. **`print(*a)` 会不会有性能问题？** —— 元素极多时展开成参数有开销，几万个还行，几十万建议用 `join`。
3. **要输出到同一行并追加怎么办？** —— `print(x, end=" ")`，但注意最后一次的尾随空格。

## 易错点

- ❌ `for x in a: print(x, end=" ")` —— 末尾多一个空格
- ❌ `print(a)` —— 打印成 `[1, 2, 3]`，带方括号和逗号
- ❌ 忘了 `map(str, ...)` —— `join` 只接受字符串

## 关联项目

无。

## 来源

`str.join` 与 `print` 的 `sep`/`end` 语义
