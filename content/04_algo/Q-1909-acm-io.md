---
id: Q-1909
title: 输入里混着数字和字符串，C++ 怎么读不串行？
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

**输入**：第一行 `n`；随后 `n` 行，每行形如 `名字 分数`（名字不含空格）。
**输出**：按分数降序，输出 `名字 分数`。

```
输入样例
3
tom 90
amy 95
bob 88

输出样例
amy 95
tom 90
bob 88
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    vector<pair<string,int>> v(n);
    for (int i = 0; i < n; ++i) cin >> v[i].first >> v[i].second;

    stable_sort(v.begin(), v.end(),
                [](auto& a, auto& b){ return a.second > b.second; });

    for (auto& p : v) cout << p.first << ' ' << p.second << '\n';
    return 0;
}
```

## 讲深一层

`cin >> string` 读的是「到下一个空白为止」，所以名字里**不能有空格**。题面说「名字不含空格」就能直接用；如果名字可能含空格（如 `Li Ming`），就必须 `getline` 整行再切分——这是两道完全不同的题。

排序稳定性：
- `sort` 不稳定，同分元素的相对顺序不定
- `stable_sort` 稳定，保持输入顺序

题面若要求「同分按输入顺序」，必须用 `stable_sort`，或者排序时把原始下标作为第二关键字。

## 高频追问

1. **`cin >> string` 遇到空行怎么办？** —— 会跳过空白继续找下一个 token，不会返回空串。想读空行必须 `getline`。
2. **`pair` 的默认比较是什么？** —— 先比 `first` 再比 `second`。这里要按分数降序，所以必须自定义比较器。
3. **`auto&` 在 lambda 参数里为什么带 `&`？** —— 避免拷贝。用 `const auto&` 更严谨。

## 易错点

- ❌ 用 `sort` 但题面要求稳定 —— 同分顺序错
- ❌ 比较器写成 `>=` —— `sort` 要求严格弱序，`>=` 会越界崩溃
- ❌ 名字含空格却用 `cin >>` —— 只读到第一个词

## 关联项目

无。

## 来源

`istream::operator>>(string)` 与 `stable_sort` 语义
