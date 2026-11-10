---
id: Q-1894
title: 最小路径和：二维 DP 怎么压缩成一维？
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
tags: [DP, 滚动数组]
hint: 原地按行更新：dp[j]=min(dp[j], dp[j-1])+grid[i][j]。dp[j] 来自上方，dp[j-1] 来自左方。
auto: true
algo_seed: true
---

## 题目

**输入**：`grid = [[1,3,1],[1,5,1],[4,2,1]]`
**输出**：`7`（1→3→1→1→1）

**问**：二维 DP 怎么压缩成一维？

## 口述答案

> `dp[j]` 存「到当前行第 j 列的最小和」。按行原地更新：
> `dp[j] = min(dp[j], dp[j-1]) + grid[i][j]`。
> 其中 `dp[j]`（更新前）是「从上方来的」，`dp[j-1]`（已更新）是「从左方来的」。
> 一行就够，因为每个格子只依赖上和左。

## 讲深一层

```cpp
int minPathSum(vector<vector<int>>& g) {
    int R = g.size(), C = g[0].size();
    vector<int> dp(C);
    dp[0] = g[0][0];
    for (int j = 1; j < C; ++j) dp[j] = dp[j-1] + g[0][j];   // 第一行
    for (int i = 1; i < R; ++i) {
        dp[0] += g[i][0];                                     // 第一列
        for (int j = 1; j < C; ++j)
            dp[j] = min(dp[j], dp[j-1]) + g[i][j];
    }
    return dp[C-1];
}
```

## 高频追问

1. **第一行/第一列为什么要单独处理？** —— 它们只有一个方向可来。
2. **空间还能更省吗？** —— 原地修改 grid，O(1) 额外空间。
3. **求最大路径和呢？** —— 把 min 换 max。

## 易错点

- ❌ 第一行/第一列没单独初始化
- ❌ `dp[j]` 和 `dp[j-1]` 的更新顺序错
- ✅ 说清「上 = 更新前、左 = 已更新」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
