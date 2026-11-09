---
id: Q-1911
title: Python 一行给不定长整数，怎么读到行尾？
module: 04_algo
sub: Python 读写
priority: P0
difficulty: 2
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

**输入**：第一行 `n`；第二行 `n` 个整数（同一行）。
**输出**：最大值。

```
输入样例
5
3 1 4 1 5

输出样例
5
```

## 口述答案

```python
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    print(max(a[:n]))          # 只取前 n 个，防止行尾有脏数据

main()
```

## 讲深一层

`line.split()` 按空白切分，返回字符串列表；`map(int, ...)` 批量转整数。这是 Python 处理「一行多个数」的标准写法。

需要注意的边界：

| 情况 | 处理 |
|---|---|
| 行尾有空格 | `split()` 自动忽略，没问题 |
| 这行只有一个数 | 也能正常工作，返回长度 1 的列表 |
| 数跨了多行 | 这行读法就错了，要用 `sys.stdin.read().split()` |
| 数字之间有逗号 | 先 `split(',')` 再 `int`，并且要 `strip()` 空格 |

`sorted` 与内存：`list(map(...))` 会一次性建列表。如果只需要最大值，可以直接 `max(map(int, input().split()))`，省一个列表。

## 高频追问

1. **`input()` 和 `sys.stdin.readline()` 差别？** —— `input()` 会去掉行尾 `\n`，`readline()` 保留，需要自己 `strip()`。前者还会尝试解析 exec 相关逻辑（Python 3 已简化），略慢。
2. **`split()` 不带参数和带参数的区别？** —— 不带参数按任意空白切且忽略空串；带参数（如 `split(',')`）按字面切，**会保留空串**。
3. **数据量很大时 `map` 和列表推导谁快？** —— `map(int, ...)` 通常快一点，且省内存（惰性）。

## 易错点

- ❌ `int(input())` 读一行多个数 —— 直接 ValueError
- ❌ 忘了 `strip()` 就用 `readline()` —— 末尾 `\n` 进到数据里
- ❌ `split(',')` 后不 trim —— `' 2'` 转 int 虽然能过，但字符串比较会错

## 关联项目

无。

## 来源

`str.split` / `map` 语义
