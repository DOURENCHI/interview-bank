---
id: Q-1908
title: 数据量到了十万级，C++ 读入太慢超时怎么办？
module: algo
sub: ACM 读写
priority: P0
difficulty: 2
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

**输入**：`n` 个数（`n ≤ 1e6`），求最大值。
**输出**：最大值。

这是典型的「算法对但 IO 超时」场景。

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);   // 关 C/C++ 流同步
    cin.tie(nullptr);              // 解除 cin 与 cout 绑定

    int n; cin >> n;
    int mx = INT_MIN, x;
    for (int i = 0; i < n; ++i) { cin >> x; if (x > mx) mx = x; }
    cout << mx << '\n';
    return 0;
}
```

再快一档是手写快读（百万级以上才需要）：

```cpp
static inline int read() {
    int x = 0, f = 1; char c = getchar();
    while (c < '0' || c > '9') { if (c == '-') f = -1; c = getchar(); }
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = getchar(); }
    return x * f;
}
```

## 讲深一层

三档速度，按数据量选：

| 做法 | 相对速度 | 适用 |
|---|---|---|
| 默认 `cin` | 1x | 1e4 以内 |
| `sync_with_stdio(false)` + `tie(nullptr)` | 3–5x | 1e5–1e6，**大多数机考够用** |
| 手写 `getchar` 快读 | 8–10x | 1e6 以上，或已知卡 IO |

原理：`sync_with_stdio(false)` 让 `cin` 不再每次和 `stdin` 同步缓冲区；`tie(nullptr)` 让 `cin` 读之前不再先 flush `cout`（默认是绑定的，每读一次可能刷一次输出）。

**注意 `tie(nullptr)` 必须在任何 IO 之前调用**，中途调用无效。

## 高频追问

1. **关了 sync 还能用 `scanf` 吗？** —— 能编译，但两套缓冲各自为政，输出顺序会乱。全用一套。
2. **`getchar_unlocked` 是什么？** —— POSIX 的非线程安全版本，更快，但 Windows/MSVC 没有。机考环境不确定就用 `getchar`。
3. **怎么知道是 IO 慢还是算法慢？** —— 看数据点：小数据过、大数据超时，多半是复杂度；所有点都临界超时，才怀疑 IO。

## 易错点

- ❌ 只关 sync 不开 tie —— 提速有限
- ❌ 用 `endl` —— 刚省下的时间又还回去
- ❌ 手写快读没处理负数和 EOF —— 边界全错

## 关联项目

无。

## 来源

C++ 流缓冲机制；竞赛快读惯例
