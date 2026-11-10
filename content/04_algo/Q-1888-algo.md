---
id: Q-1888
title: 零钱兑换：为什么贪心不行，必须 DP？
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
tags: [DP, 完全背包]
hint: 面额组合下贪心会错过更优解。dp[j]=min(dp[j], dp[j-coin]+1) 求最少硬币数。
auto: true
algo_seed: true
---

## 题目

**输入**：`coins = [1,2,5], amount = 11`
**输出**：`3`（5+5+1）

**问**：为什么贪心不行，必须 DP？

## 口述答案

> 贪心每次取最大面额，在某些面额组合下会错过更优解。
> 例如面额 `[1,3,4]`、金额 6：贪心得 4+1+1=3 枚，最优是 3+3=2 枚。
> 所以必须 DP：`dp[j] = min(dp[j], dp[j-coin]+1)`，枚举所有面额，取最小枚数。

## 讲深一层

```cpp
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);      // 用 amount+1 表示无穷
    dp[0] = 0;
    for (int j = 1; j <= amount; ++j)
        for (int c : coins)
            if (c <= j) dp[j] = min(dp[j], dp[j - c] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
}
```

这是**完全背包**：每种硬币可用无限次，所以内层正序、外层是金额或硬币都可以。

## 高频追问

1. **为什么用 `amount+1` 当无穷？** —— 最大枚数不会超过 amount（全用 1 元），安全且不会溢出。
2. **求方案数呢？** —— `dp[j] += dp[j-c]`，且必须外层枚举硬币、内层正序（避免重复计数）。
3. **0-1 背包和完全背包在代码上差什么？** —— 内层循环方向（倒序 vs 正序）。

## 易错点

- ❌ 用贪心
- ❌ 无穷大用 INT_MAX 导致 +1 溢出
- ✅ 说清「完全背包的正序」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
