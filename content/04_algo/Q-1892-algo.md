---
id: Q-1892
title: 最长公共子序列：二维 DP 的边界怎么设？
module: 04_algo
sub: DP
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DP, 字符串]
hint: dp 开 (m+1)×(n+1)，第 0 行第 0 列为 0 表示空串。字符相等取左上+1，否则取上/左较大。
auto: true
algo_seed: true
---

## 题目

**输入**：`text1 = "abcde", text2 = "ace"`
**输出**：`3`（`"ace"`）

**问**：二维 DP 的边界怎么设？

## 口述答案

> `dp` 开 `(m+1) × (n+1)`，第 0 行和第 0 列全为 0，表示「其中一个串为空」。
> 这样不用特判 i-1/j-1。
> 转移：字符相等取左上 + 1；不等取上、左的较大值。

## 讲深一层

```cpp
int longestCommonSubsequence(string a, string b) {
    int m = a.size(), n = b.size();
    vector<vector<int>> dp(m+1, vector<int>(n+1, 0));
    for (int i = 1; i <= m; ++i)
        for (int j = 1; j <= n; ++j)
            dp[i][j] = (a[i-1] == b[j-1])
                     ? dp[i-1][j-1] + 1
                     : max(dp[i-1][j], dp[i][j-1]);
    return dp[m][n];
}
```

## 高频追问

1. **和「最长公共子串」什么区别？** —— 子串要求连续，不等时直接置 0。
2. **空间压缩？** —— 用两行或一维倒序。
3. **要输出具体 LCS？** —— 从右下角回溯。

## 易错点

- ❌ 下标从 0 开始却用 `dp[i-1][j-1]` —— 越界
- ❌ 不等时忘了取 max
- ✅ 记住「多开一行一列当边界」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
