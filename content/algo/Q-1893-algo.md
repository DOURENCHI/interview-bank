---
id: Q-1893
title: 不同路径：为什么组合数也能解？
module: algo
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
tags: [DP, 组合数学]
hint: 一共走 m+n-2 步，其中 m-1 步向下，答案就是 C(m+n-2, m-1)。注意溢出。
auto: true
algo_seed: true
---

## 题目

**输入**：`m = 3, n = 7`
**输出**：`28`

**问**：为什么组合数也能解？

## 口述答案

> 从左上到右下，一共走 `m+n-2` 步，其中 `m-1` 步向下、`n-1` 步向右。
> 所以答案就是「从 m+n-2 步里选 m-1 步向下」的组合数 `C(m+n-2, m-1)`。
> DP 的转移 `dp[i][j] = dp[i-1][j] + dp[i][j-1]` 本质上就是在算这个。

## 讲深一层

```cpp
int uniquePaths(int m, int n) {
    vector<int> dp(n, 1);
    for (int i = 1; i < m; ++i)
        for (int j = 1; j < n; ++j)
            dp[j] += dp[j-1];
    return dp[n-1];
}
```

一维 DP：`dp[j]` 是「上方来的」，`dp[j-1]` 是「左方来的」。

## 高频追问

1. **有障碍物呢？** —— 障碍处置 0。
2. **组合数会溢出吗？** —— 会，m、n 大时要用高精度或取模。
3. **能走三个方向吗？** —— 那 DP 就不适用了（有环），要另想。

## 易错点

- ❌ 一维 DP 初始化全 1 但第一列处理错
- ❌ 组合数直接算阶乘溢出
- ✅ 说清「向下 m-1 步、向右 n-1 步」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
