---
id: Q-1891
title: 编辑距离：三种操作对应 DP 表的哪三个方向？
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
hint: 插入看左、删除看上、替换看左上；三者取最小再 +1，字符相等时取左上不 +1。
auto: true
algo_seed: true
---

## 题目

**输入**：`word1 = "horse", word2 = "ros"`
**输出**：`3`

**问**：三种操作对应 DP 表的哪三个方向？

## 口述答案

> `dp[i][j]` 表示 word1 前 i 个字符变成 word2 前 j 个字符的最少操作数。
> 三种操作对应三个方向：**插入**看左边 `dp[i][j-1]`、**删除**看上边 `dp[i-1][j]`、
> **替换**看左上 `dp[i-1][j-1]`。
> 三者取最小再加 1；如果当前字符相等，直接取左上不加一。

## 讲深一层

```cpp
int minDistance(string a, string b) {
    int m = a.size(), n = b.size();
    vector<vector<int>> dp(m+1, vector<int>(n+1));
    for (int i = 0; i <= m; ++i) dp[i][0] = i;   // 全删
    for (int j = 0; j <= n; ++j) dp[0][j] = j;   // 全插
    for (int i = 1; i <= m; ++i)
        for (int j = 1; j <= n; ++j) {
            if (a[i-1] == b[j-1]) dp[i][j] = dp[i-1][j-1];
            else dp[i][j] = 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
        }
    return dp[m][n];
}
```

## 高频追问

1. **为什么插入看左、删除看上？** —— 因为 `dp[i][j-1]` 表示 word1 前 i 个已经变成 word2 前 j-1 个，差一个字符要插入。
2. **只能替换/删除呢？** —— 去掉对应方向。
3. **空间能压缩吗？** —— 能压成两行，但要保存上一行。

## 易错点

- ❌ 边界初始化漏（第 0 行/列）
- ❌ 字符相等时也加 1
- ✅ 记住「左=插入、上=删除、左上=替换」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
