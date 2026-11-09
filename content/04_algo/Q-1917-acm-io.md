---
id: Q-1917
title: Python 读百万级数据超时，怎么优化输入？
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

**输入**：`n` 个数（`n ≤ 1e6`），求最大值。
**输出**：最大值。

典型「算法对但 IO 超时」场景。

## 口述答案

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    mx = max(map(int, data[1:n + 1]))
    sys.stdout.write(str(mx))

main()
```

## 讲深一层

关键在 `sys.stdin.buffer`：它拿到的是**字节流**，跳过文本解码这一层。

| 写法 | 相对速度 | 说明 |
|---|---|---|
| `input()` 逐行 | 1x | 每次都要解码 + 去换行 |
| `sys.stdin.readline()` | 2–3x | 仍走文本层 |
| `sys.stdin.read()` | 5x | 一次读完，文本层 |
| `sys.stdin.buffer.read()` | 8–10x | **字节层，最快** |

`buffer.read().split()` 得到的是 `bytes` 列表，`int(b'123')` 是合法的（Python 会自动转），所以后面照常处理。

另一个隐藏瓶颈是 `print`：每次 `print` 都要拼缓冲并可能 flush。循环里输出几万行时，攒成列表再 `'\n'.join` 一次性写，能差出好几秒。

## 高频追问

1. **`bytes` 和 `str` 混用会出错吗？** —— `int()` 和比较都能用，但 `b'abc' == 'abc'` 是 `False`。只要不混着比字符串就没事。
2. **`sys.setrecursionlimit` 要不要设？** —— 写递归 DFS 时务必设，默认 1000 层，图/树题容易爆。设到 1e6 还要注意真爆栈时进程会崩。
3. **PyPy 会不会更快？** —— 循环密集的题快很多，但机考环境用什么由平台决定，不能假设。

## 易错点

- ❌ 用 `input()` 读百万行 —— 必超时
- ❌ 循环 `print` —— 输出成瓶颈
- ❌ `buffer.read()` 后又想 `split()` 按行处理 —— 换行已被切掉，得自己重新组装

## 关联项目

无。

## 来源

`sys.stdin.buffer` 与 CPython IO 开销
