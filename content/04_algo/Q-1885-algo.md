---
id: Q-1885
title: 爬楼梯：为什么它和斐波那契是同一道题？
module: 04_algo
sub: DP
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DP, 递推]
hint: 到第 n 阶只能从 n-1 或 n-2 来，dp[n]=dp[n-1]+dp[n-2]。两个变量滚动，O(1) 空间。
auto: true
algo_seed: true
---

## 题目

**输入**：`n = 5`（每次走 1 或 2 阶）
**输出**：`8`

**问**：为什么它和斐波那契是同一道题？

## 口述答案

> 到第 n 阶，最后一步只能是从 n-1 走 1 阶，或从 n-2 走 2 阶。
> 所以 `dp[n] = dp[n-1] + dp[n-2]`，和斐波那契完全一样，只是初值不同（dp[1]=1, dp[2]=2）。
> 只要两个变量滚动就能 O(1) 空间。

## 讲深一层

```cpp
int climbStairs(int n) {
    if (n <= 2) return n;
    int a = 1, b = 2;
    for (int i = 3; i <= n; ++i) { int c = a + b; a = b; b = c; }
    return b;
}
```

| 方法 | 空间 | 说明 |
|---|---|---|
| 数组 DP | O(n) | 直观 |
| **滚动变量** | **O(1)** | 最优 |
| 矩阵快速幂 | O(log n) | n 极大时用 |

## 高频追问

1. **每次可走 1..k 阶？** —— 前缀和优化或完全背包。
2. **不能连续走 2 阶？** —— 加状态维度。
3. **n 到 1e18？** —— 矩阵快速幂 + 取模。

## 易错点

- ❌ 初值搞错（dp[0]=1 还是 0）
- ❌ 忘了取模（题目要求时）
- ✅ 说清「最后一步的来源」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
