---
id: Q-1906
title: 输出要求空格分隔，行末不能有多余空格，怎么写？
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

**输入**：一个整数 `n`，随后 `n` 个整数。
**输出**：原样输出，**数与数之间一个空格，行末不能有空格**。

```
输入样例
3
1 2 3

输出样例（注意 3 后面没有空格）
1 2 3
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    for (int i = 0; i < n; ++i) {
        int x; cin >> x;
        if (i) cout << ' ';        // 第一个不输出空格
        cout << x;
    }
    cout << '\n';
    return 0;
}
```

## 讲深一层

「行末多余空格」是 OJ 评判里最常见的非算法失分点。有些 OJ 会忽略行末空白，有些**严格逐字符比对**——你没法预知，所以一律按严格标准写。

三种可行写法，按推荐排序：

| 写法 | 说明 |
|---|---|
| `if (i) cout << ' ';` | 最直观，零额外开销 |
| 先输出第一个，循环从 1 开始 | 等价，少一次判断 |
| 攒进 `vector` 再用 `join` 思路 | Python 更常用，C++ 略显重 |

反过来，如果用 Python 的 `' '.join(...)`，天然没有行末空格，这是 Python 在这件事上的优势。

## 高频追问

1. **每行最后输出 `\n` 还是 `endl`？** —— `'\n'`。`endl` 每次强制 flush，大数据量下慢几倍。
2. **多组用例之间有空白要求怎么办？** —— 严格照题面。常见是「每组之间一个空行」，但最后一行后面不要。
3. **最后一行要不要换行符？** —— 通常要，多数 OJ 容忍没有，但加上更安全。

## 易错点

- ❌ `cout << x << " ";` 收尾 —— 行末多一个空格
- ❌ 用 `endl` 换行 —— 性能问题
- ❌ 多组用例之间乱加空行 —— 格式错

## 关联项目

无。

## 来源

OJ 输出格式严格匹配惯例
