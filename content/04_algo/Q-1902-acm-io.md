---
id: Q-1902
title: 输入有多少组不知道，只说到文件结束，C++ 怎么写？
module: 04_algo
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

**输入**：多组数据，每组一行两个整数 `a b`，直到文件结束。
**输出**：每组输出 `a+b`，一行一个。

```
输入样例
1 2
3 4

输出样例
3
7
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int a, b;
    while (cin >> a >> b) {          // 读到 EOF 自动结束
        cout << a + b << '\n';
    }
    return 0;
}
```

## 讲深一层

`cin >> a >> b` 在流里没数据时返回的流对象会被转成 `false`，循环就退出了。**这是「读失败即结束」的惯用法**，不要写成 `while (!cin.eof())`。

原因：`eof()` 只有在**尝试读并且失败之后**才置位。写成 `while (!cin.eof())` 会多跑一轮，把上一轮的 `a`、`b` 再输出一次。

三种常见形态要能一眼认出来：

| 题面说法 | 写法 |
|---|---|
| 「直到文件结束」 | `while (cin >> a >> b)` |
| 「第一行是组数 T」 | `cin >> T; while (T--)` |
| 「以 0 0 结束」 | `while (cin >> a >> b, a || b)` |

## 高频追问

1. **`while (T--)` 会不会多跑一次？** —— `T--` 是先取值后减，`T=3` 时依次得到 3、2、1，跑三次，正确。
2. **EOF 之后还能再用 `cin` 吗？** —— 不能，`failbit` 已置位。要 `cin.clear()` 才有救，机考里通常不需要。
3. **用 `scanf` 怎么写？** —— `while (scanf("%d%d", &a, &b) != EOF)`，注意返回值是成功读入的项数，也可以是 `== 2`。

## 易错点

- ❌ `while (!cin.eof())` —— 多输出一轮脏数据
- ❌ 在循环里 `cin.clear()` —— 把结束信号清掉了，可能死循环
- ❌ 每组之间多输出空行 —— 题面没要求就是错

## 关联项目

无。

## 来源

`istream::operator bool` 与 `eofbit` / `failbit` 语义
