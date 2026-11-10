---
id: Q-1847
title: 和为 K 的子数组：前缀和 + 哈希怎么配合？
module: 04_algo
sub: 数组哈希
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-10
tags: [前缀和, 哈希]
auto: true
algo_seed: true
---

## 题目

**题目**：统计和恰好为 `k` 的连续子数组个数。

```
输入：nums = [1,1,1], k = 2
输出：2      （[1,1] 出现两次）
```

**问**：前缀和 + 哈希是怎么配合的？为什么要把 `{0: 1}` 提前放进去？

## 口述答案

> 设前缀和 `pre[i] = nums[0..i-1]` 之和，那么子数组 `[j, i)` 的和等于 `pre[i] - pre[j]`。要求它等于 `k`，就是找**有多少个 `j` 满足 `pre[j] = pre[i] - k`**。
> 哈希表存"每个前缀和出现过几次"，遍历时查一次就能得到个数。`{0: 1}` 必须在开头放进去，代表"空前缀"，否则从下标 0 开始的子数组会被漏掉。

## 讲深一层

```cpp
int subarraySum(vector<int>& nums, int k) {
    unordered_map<int,int> cnt{{0, 1}};   // 空前缀
    int sum = 0, res = 0;
    for (int x : nums) {
        sum += x;
        auto it = cnt.find(sum - k);
        if (it != cnt.end()) res += it->second;
        ++cnt[sum];                        // 先查后加
    }
    return res;
}
```
时间 O(n)，空间 O(n)。

**为什么"先查后加"**：如果先加再查，当 `k == 0` 时会把当前元素自己算进去，多算。先查保证只统计"之前出现过的前缀和"。

**为什么不能用滑动窗口**：数组可能有负数，窗口和不单调，左指针不知道该不该右移。

## 高频追问

1. **如果数组全是正数呢？** —— 可以用滑动窗口 O(1) 空间，但要注意这题问的是"个数"，滑窗统计个数会更麻烦。
2. **`sum` 会溢出吗？** —— 元素接近 `INT_MAX` 且 n 大时会，用 `long long`。
3. **要返回具体子数组怎么办？** —— 哈希表里存"前缀和 → 下标列表"，查出后逐个还原。

## 易错点

- 忘了 `{0: 1}`，从 0 开始的子数组全漏
- 先加后查，`k=0` 时多算
- 用滑动窗口，遇到负数就错

## 关联项目

- 无（机考基本功）

## 来源

前缀和 + 哈希（LeetCode 560 类题，预测题）
