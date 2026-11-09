---
id: Q-1905
title: 输入是逗号分隔的一串数，C++ 怎么解析？
module: 04_algo
sub: C++ 读写
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

**输入**：一行逗号分隔的整数，如 `1,2,3,4`（可能带空格 `1, 2, 3`）。
**输出**：升序排序后，用逗号连接输出。

```
输入样例
3,1,4,1,5

输出样例
1,1,3,4,5
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    getline(cin, line);

    vector<int> a;
    stringstream ss(line);
    string tok;
    while (getline(ss, tok, ',')) {        // 按逗号切
        if (tok.empty()) continue;
        // 去掉可能的前导空格
        size_t b = tok.find_first_not_of(" \t");
        if (b == string::npos) continue;
        a.push_back(stoi(tok.substr(b)));
    }

    sort(a.begin(), a.end());
    for (size_t i = 0; i < a.size(); ++i) {
        if (i) cout << ',';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}
```

## 讲深一层

`getline(ss, tok, ',')` 是带自定义分隔符的版本。注意它的行为和 `cin >>` 完全不同：**不跳过空白，也不把分隔符当多个连续分隔处理**。

所以 `1, 2` 切出来是 `"1"` 和 `" 2"`——第二个带前导空格。`stoi` 其实会跳过前导空格，所以这里能过；但如果要做严格字符串比较，就得自己 trim。

输入形态对照：

| 分隔符 | 写法 |
|---|---|
| 空格/Tab/换行 | `cin >>` 或 `ss >>` |
| 逗号 | `getline(ss, tok, ',')` |
| 混合（逗号后带空格） | 先按逗号切，再 trim |
| 变长字段 | 手写双指针扫描，最可靠 |

## 高频追问

1. **`stoi` 遇到非法字符怎么办？** —— 抛 `invalid_argument`。机考里要么确保格式合法，要么用 `try/catch` 兜住。
2. **最后一个 token 后面有逗号会怎样？** —— 会切出一个空串，`skip` 掉即可。
3. **数据量很大时 `stringstream` 会不会太慢？** —— 会。几十万级建议手写指针扫描。

## 易错点

- ❌ 以为 `getline` 会 trim —— 不会，空格原样保留
- ❌ 用 `cin >>` 读逗号分隔 —— `>>` 不认逗号，会读失败
- ❌ 输出时末尾多一个逗号 —— 格式错

## 关联项目

无。

## 来源

`std::getline` 三分隔符版本语义
