---
id: Q-1899
title: 正则表达式匹配：DP 状态怎么定义？
module: algo
sub: DP
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DP, 字符串]
hint: dp[i][j] 表示 s 前 i 个与 p 前 j 个是否匹配；* 要看它和前面那个字符组成「0 次或多次」。
auto: true
algo_seed: true
---

## 题目

**输入**：`s = "aab", p = "c*a*b"`
**输出**：`true`
**规则**：`.` 匹配任意单字符，`*` 匹配前一个字符 0 次或多次。

**问**：DP 状态怎么定义？

## 口述答案

> `dp[i][j]` 表示「s 的前 i 个字符」能否被「p 的前 j 个字符」匹配。
> 关键在 `*`：它要和前一个字符一起看。
> 如果 `p[j-1]` 是 `*`，有两种选择：
> **用 0 次**（`dp[i][j-2]`），或**用一次以上**（`s[i-1]` 与 `p[j-2]` 匹配且 `dp[i-1][j]`）。

## 讲深一层

```cpp
bool isMatch(string s, string p) {
    int m = s.size(), n = p.size();
    vector<vector<bool>> dp(m+1, vector<bool>(n+1, false));
    dp[0][0] = true;
    for (int j = 2; j <= n; ++j)
        if (p[j-1] == '*') dp[0][j] = dp[0][j-2];   // 空串匹配 a*b*
    for (int i = 1; i <= m; ++i)
        for (int j = 1; j <= n; ++j) {
            if (p[j-1] == '*') {
                dp[i][j] = dp[i][j-2];                                  // 0 次
                if (p[j-2] == '.' || p[j-2] == s[i-1])
                    dp[i][j] = dp[i][j] || dp[i-1][j];                  // 多次
            } else {
                if (p[j-1] == '.' || p[j-1] == s[i-1])
                    dp[i][j] = dp[i-1][j-1];
            }
        }
    return dp[m][n];
}
```

## 高频追问

1. **为什么 `dp[0][j]` 要单独初始化？** —— 空串也能被 `a*b*c*` 匹配。
2. **`dp[i-1][j]` 为什么不是 `dp[i-1][j-2]`？** —— 用多次时 `*` 还在，要继续匹配剩余。
3. **回溯写法？** —— 可以，但会有重复子问题。

## 易错点

- ❌ `*` 当成独立字符处理
- ❌ 空串的初始化漏掉
- ✅ 说清「0 次 vs 多次」两种转移


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
