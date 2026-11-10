---
id: Q-1890
title: 分割等和子集：怎么转化成 0-1 背包？
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
hint: 目标和 = sum/2，问能否凑出这个和。sum 为奇数直接 false。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [1, 5, 11, 5]`　**输出**：`true`（可分成 `[1,5,5]` 和 `[11]`）
**限制**：每个元素只能用一次；若 `nums = [1, 2, 3, 5]` 则输出 `false`。
**问**：怎么把「分割等和子集」转化成 0-1 背包？

## 口述答案

> 三步转化。第一步：若总和是奇数，直接返回 false——平分都不可能。第二步：目标变成「能否从数组里选出若干个数，和恰好等于 sum/2」——这就是一个**可行性 0-1 背包**：物品是每个数，重量和价值都是它本身，背包容量是 sum/2，问能不能恰好装满。第三步：状态用布尔型，`dp[j]` 表示「能否凑出和 j」，转移 `dp[j] = dp[j] || dp[j-nums[i]]`，内层**倒序**（每数一次），`dp[0] = true` 作初始。答案是 `dp[sum/2]`。
> 倒序在这里依然关键：正序会让同一个数被重复选，把「每数一次」变成「无限次」。

## 讲深一层

```cpp
bool canPartition(vector<int>& nums) {
    int sum = 0; for (int x : nums) sum += x;
    if (sum & 1) return false;                  // 奇数剪枝
    int T = sum / 2;
    vector<char> dp(T + 1, 0); dp[0] = 1;
    for (int x : nums)
        for (int j = T; j >= x; --j)            // 倒序：每数一次
            dp[j] = dp[j] || dp[j - x];
    return dp[T];
}
```

- 优化：用 `bitset`（`dp |= dp << x`）把内层循环交给硬件，快一个数量级
- 复杂度 O(n·sum/2)，空间 O(sum/2)

## 高频追问

1. 为什么是 sum/2 而不是 sum？——两半相等，找到一半即可
2. 如果要求两个子集的元素个数也相等呢？——dp 状态加一维记录个数
3. 正序会怎样？——每个数无限次，判定结果会假 true

## 易错点

- 忘了奇数剪枝（sum 为奇不可能平分）
- 布尔 dp 写成 max
- 内层方向写成正序

## 关联项目

- 无（算法题）。LeetCode 按题名搜：分割等和子集 416

## 来源

算法题通用解法整理（预测题，非真实面经）
