---
id: Q-1901
title: 一行里给不定长个整数，C++ 怎么读到行尾？
module: 04_algo
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

**输入**：第一行一个整数 `n`；第二行 `n` 个整数，同一行。
**输出**：这 `n` 个数的最大值。

```
输入样例
5
3 1 4 1 5

输出样例
5
```

题面说「同一行」，但 `cin >>` 根本不看行。真正需要按行读的场景是：**这行有多少个数不确定，靠行尾判断**。

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');   // 关键：吃掉第一行的换行

    string line;
    getline(cin, line);
    stringstream ss(line);
    int x, mx = INT_MIN, cnt = 0;
    while (ss >> x) { mx = max(mx, x); ++cnt; }
    cout << mx << '\n';
    return 0;
}
```

## 讲深一层

三个层次，按需要选：

| 场景 | 写法 | 代价 |
|---|---|---|
| 个数已知，只在同一行 | 直接 `cin >> x` 循环 n 次 | 最简单，推荐 |
| 个数未知，读到行尾 | `getline` + `stringstream` | 多一次字符串构造 |
| 整份输入都要按行处理 | `while (getline(cin, line))` | 注意每行自己再切 |

`cin.ignore(...)` 这步是**必须的**：`cin >> n` 读完后，缓冲区里还留着那个换行符，紧接着的 `getline` 会立刻读到空串。这是 C++ 机考第一大坑。

## 高频追问

1. **`ignore` 的两个参数是什么？** —— 最大丢弃字符数 + 终止字符。上限用 `numeric_limits<streamsize>::max()` 表示不设限。
2. **只能用 `'\n'` 吗？** —— Windows 下输入可能是 `\r\n`，`getline` 默认按 `\n` 切，会把 `\r` 留在行尾。如果后面要比字符串，记得 `line.pop_back()` 或 `erase` 掉 `\r`。
3. **`stringstream` 很慢吗？** —— 比 `cin >>` 再慢一点，但机考数据量通常撑得住。真卡了再换手写解析。

## 易错点

- ❌ 忘了 `cin.ignore()` —— `getline` 拿到空串，然后整题读错
- ❌ 用 `cin.sync()` 代替 —— 各平台行为不一致，别用
- ❌ `while (ss >> x)` 写成 `while (!ss.eof())` —— eof 标志在读失败之后才置位，会多处理一次脏数据

## 关联项目

无。

## 来源

C++ 标准库 `istream::ignore` / `getline` 语义
