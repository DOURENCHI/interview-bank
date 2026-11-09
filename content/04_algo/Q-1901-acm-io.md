---
id: Q-1901
title: 机考第一行给两个整数，C++ 怎么读最稳？
module: 04_algo
sub: C++ 读写
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 机考 ACM 模式通用写法整理
verified_at: 2026-11-09
tags: [ACM, 输入输出, 机考, C++ 读写]
auto: true
acm_seed: true
---

## 题目

**输入**：第一行两个整数 `n m`，接下来 `n` 行，每行 `m` 个整数。
**输出**：所有元素之和。

```
输入样例
2 3
1 2 3
4 5 6

输出样例
21
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;      // 读失败直接退出，别硬跑
    long long sum = 0;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j) {
            int x; cin >> x;
            sum += x;
        }
    cout << sum << '\n';
    return 0;
}
```

## 讲深一层

`cin >> x` 按**空白字符**（空格、Tab、换行）分隔，自动跳过前导空白。所以上面完全不用关心「换行在哪」——`1 2 3` 和分三行写 `1\n2\n3` 对 `cin >>` 是等价的。

这带来两个直接后果：

| 事实 | 影响 |
|---|---|
| `>>` 会把换行当分隔符丢掉 | 想按行读必须换 `getline` |
| 读到一个格式错误的输入会置 `failbit` | 之后所有 `cin >>` 都立刻失败，不报错也不抛异常 |

第一行加 `if (!(cin >> n >> m)) return 0;` 就是防这个——多组用例读到 EOF 时会自然退出，不会死循环。

## 高频追问

1. **`sum` 为什么用 `long long`？** —— `n*m` 个 int 累加很容易溢出。机考常见 `n,m ≤ 1000`、元素 ≤ 1e9，一乘就过 2^31。
2. **`ios::sync_with_stdio(false)` 到底关了什么？** —— 关掉 C 和 C++ 流缓冲区的同步。默认情况下 `cin` 每次都要和 `stdin` 对齐，慢一个量级。
3. **加了这行还能用 `printf` 吗？** —— 能编译能跑，但两条流顺序会乱。要么全用 C++ 流，要么全用 C 的 IO，别混。

## 易错点

- ❌ 只写 `int` 累加 —— 大数据点必挂，且挂得莫名其妙
- ❌ 忘了 `cin.tie(nullptr)` —— 只关 sync 不开 tie，`endl` 仍会 flush，还是慢
- ❌ 用 `endl` 换行 —— 每次 flush 一次。用 `'\n'`

## 关联项目

无（机考基本功）。

## 来源

ACM 模式通用写法 + C++ 标准库 `ios_base` 行为
