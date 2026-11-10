---
id: Q-1897
title: 打家劫舍 II：环形怎么拆成两个线性？
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
tags: [DP, 环形]
hint: 首尾不能同时偷，分别算「不偷第一个」和「不偷最后一个」，取较大值。
auto: true
algo_seed: true
---

## 题目

**背景**：打家劫舍 II（213）在 I（198）的基础上把街道围成了**环**：第一家和最后一家相邻。
**输入**：`nums = [2, 3, 2]`　**输出**：`3`（不能同时偷首尾两家，只能偷 3）
**问**：环形约束怎么拆成已经会做的线性问题？

## 口述答案

> 环的麻烦只在首尾相邻。拆法：**分两种情况分别做线性打家劫舍，再取最大**——
> 情况一：不偷第一家，问题变成 `[1, n-1]` 这段线性街道；
> 情况二：不偷最后一家，问题变成 `[0, n-2]` 这段。
> 两种情况里首尾都绝不可能同时被偷，环形约束自动满足。答案就是两者较大值。
> 每段内部就是 I 的滚动变量解法。注意边界：只有一户人家（n=1）时两条区间都为空，直接返回 `nums[0]`。

## 讲深一层

```cpp
int robLine(vector<int>& a) {                    // 打家劫舍 I 的滚动解法
    int prev = 0, cur = 0;
    for (int x : a) { int t = max(cur, prev + x); prev = cur; cur = t; }
    return cur;
}
int rob(vector<int>& nums) {
    int n = nums.size();
    if (n == 1) return nums[0];                  // 特判：环退化为单点
    vector<int> a(nums.begin(), nums.end() - 1); // 不偷最后一家
    vector<int> b(nums.begin() + 1, nums.end()); // 不偷第一家
    return max(robLine(a), robLine(b));
}
```

- 复杂度 O(n) 时间、O(1) 额外空间（两段各滚一遍）
- 本质：环形 DP 的通用套路——**枚举首元素的决策，把环断成链**

## 高频追问

1. 为什么两种情况覆盖了所有方案？——任何方案要么不偷首、要么不偷尾（环形下两者不可兼得）
2. 如果是三户环呢？——n=2 时两家相邻也不可兼偷，max(nums[0], nums[1])，robLine 的空段处理会自然退化，但要留意
3. 环形 DP 还有别的例子吗？——环形石子合并、环形队列的区间 DP，套路同为「断环为链」

## 易错点

- 忘了 n=1 特判——两条空区间都返回 0
- 两个区间写错：一个去掉头、一个去掉尾，不是各去掉一半
- 在线性解法里加 if 特判首尾——不如拆区间干净

## 关联项目

- 无（算法题）。LeetCode 按题名搜：打家劫舍 II 213

## 来源

算法题通用解法整理（预测题，非真实面经）
