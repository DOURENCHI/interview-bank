---
id: Q-1910
title: Python 机考第一行两个整数，怎么写最快？
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

**输入**：第一行 `n m`，接下来 `n` 行每行 `m` 个整数。
**输出**：元素之和。

```
输入样例
2 3
1 2 3
4 5 6

输出样例
21
```

## 口述答案

```python
import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    total = 0
    for _ in range(n * m):
        total += int(next(it))
    print(total)

main()
```

## 讲深一层

Python 机考的核心思路是：**一次性读完全部输入，再按需要切片**。因为 `input()` 每调一次就是一次系统调用级别的开销，百万行时会明显拖慢。

三种读法对比：

| 写法 | 速度 | 适用 |
|---|---|---|
| `input()` 逐行 | 最慢 | 行数少，逻辑按行处理 |
| `sys.stdin.readline()` | 快 2–3 倍 | 需要按行处理 |
| `sys.stdin.read().split()` | 最快 | **数字为主的题，首选** |

`split()` 不传参数时按任意空白切分（空格、Tab、换行都算），所以上面完全不用管「换行在哪」，和 C++ 的 `cin >>` 等价。

## 高频追问

1. **`iter` + `next` 是必须的吗？** —— 不是，但用它按需取 token 比维护下标 `i` 更不容易越界。
2. **`sys.stdin.read()` 会不会内存爆？** —— 会。几十万 token 没问题，上千万就要改按行读。
3. **为什么包一层 `main()`？** —— 局部变量比全局变量快（`LOAD_FAST` vs `LOAD_GLOBAL`），数据量大时有可观差距。

## 易错点

- ❌ 用 `input()` 读百万行 —— 超时
- ❌ `split()` 后发现 token 数不够 —— 题面格式看错了，加断言能早发现
- ❌ 忘了 `int()` 转换 —— 字符串累加会变成拼接

## 关联项目

无。

## 来源

`sys.stdin.read` / `str.split` 语义
