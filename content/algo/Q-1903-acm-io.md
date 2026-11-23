---
id: Q-1903
title: 第一行给组数 T，多组用例怎么组织？
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
tags: [ACM, 输入输出, 机考, C++ 读写]
auto: true
acm_seed: true
---

## 题目

**输入**：第一行 `T` 表示组数。每组一行 `n`，下一行 `n` 个整数。
**输出**：每组输出这 `n` 个数的和。

```
输入样例
2
3
1 2 3
2
10 20

输出样例
6
30
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; cin >> T;
    while (T--) {
        int n; cin >> n;
        long long s = 0;
        for (int i = 0; i < n; ++i) { int x; cin >> x; s += x; }
        cout << s << '\n';
    }
    return 0;
}
```

## 讲深一层

多组用例的关键不是循环，而是**状态复位**：每组开始时，所有累加量、标记数组、容器都要重新初始化。

初学者最常见的错误是「第一组对、第二组错」——因为上一组的数据残留在全局数组或静态变量里。养成习惯：**变量定义在循环内部**，能局部就局部。

```cpp
while (T--) {
    int n; cin >> n;
    long long s = 0;              // 在循环内定义，天然每组归零
    vector<int> a(n);             // 同上
    ...
}
```

如果数据量大、必须复用大数组，就显式 `fill(a.begin(), a.end(), 0)`，不要靠运气。

## 高频追问

1. **`T` 组数据但每组规模不同，内存怎么安排？** —— 优先每组内重新申请；`vector` 的 `clear()` 不释放容量，能复用又不反复分配。
2. **输出时每组之间要不要空行？** —— **严格按题面**。题面没说就一行一个答案。多一个空行可能被判错。
3. **`while (T--)` 里 `T` 变成 -1 有问题吗？** —— 循环结束后 `T` 是 -1，不影响正确性，但别再拿它当组数用。

## 易错点

- ❌ 累加变量定义在循环外 —— 第二组接着第一组累加
- ❌ 用全局数组但不清零 —— 典型「对一半错一半」
- ❌ 题目说「每组之间输出空行」却忘了 —— 格式错

## 关联项目

无。

## 来源

多组测试用例通用模式
