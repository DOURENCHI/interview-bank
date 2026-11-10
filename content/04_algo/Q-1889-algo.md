---
id: Q-1889
title: 0-1 背包：为什么内层循环必须倒序？
module: 04_algo
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
tags: [DP, 背包]
hint: 倒序保证 dp[j] 用的是上一轮的值；正序会让同一物品被重复选，变成完全背包。
auto: true
algo_seed: true
---

## 题目

**输入**：`n` 个物品（重量 w、价值 v），背包容量 `W`，每件最多取一次。
**输出**：最大价值。

**问**：为什么内层循环必须倒序？

## 口述答案

> 因为一维数组压缩时，`dp[j]` 依赖的是「上一轮」的 `dp[j-w]`。
> 正序遍历时，`dp[j-w]` 可能已经被**本轮**更新过，相当于同一件物品被选了多次，变成完全背包。
> 倒序保证 `dp[j-w]` 还是上一轮的值，才是真正的「每件最多一次」。

## 讲深一层

```cpp
int knapsack(vector<int>& w, vector<int>& v, int W) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < (int)w.size(); ++i)
        for (int j = W; j >= w[i]; --j)          // 倒序
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    return dp[W];
}
```

| 背包类型 | 内层方向 | 含义 |
|---|---|---|
| 0-1 | **倒序** | 每件一次 |
| 完全 | 正序 | 每件无限 |

## 高频追问

1. **二维数组版要倒序吗？** —— 不用，因为 `dp[i][j]` 依赖 `dp[i-1][...]`，天然隔离。
2. **要求恰好装满？** —— 初始化为 -inf，`dp[0]=0`。
3. **求方案数？** —— `dp[j] += dp[j-w[i]]`。

## 易错点

- ❌ 内层正序 —— 变成完全背包
- ❌ 内层起点写 0 而不是 `w[i]`（虽不出错但浪费）
- ✅ 能解释「倒序 = 用上一轮的值」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
