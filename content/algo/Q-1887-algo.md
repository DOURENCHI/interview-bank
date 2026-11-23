---
id: Q-1887
title: 最长递增子序列：O(n²) 和 O(n log n) 两种解法差在哪？
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
tags: [DP, 二分]
hint: O(n²) 是 dp[i]=max(dp[j])+1；O(n log n) 用 tails 存各长度的最小结尾，二分定位替换。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [10,9,2,5,3,7,101,18]`
**输出**：`4`（`[2,3,7,101]`）

**问**：O(n²) 和 O(n log n) 两种解法差在哪？

## 口述答案

> O(n²)：`dp[i]` 表示「以 i 结尾的 LIS 长度」，转移是 `dp[i] = max(dp[j]) + 1, j<i 且 a[j]<a[i]`。
> O(n log n)：维护一个 `tails` 数组，`tails[k]` 表示长度为 k+1 的递增子序列的**最小结尾**。
> 遍历每个数，用二分找到它该放的位置并替换，数组长度就是答案。
> 关键洞察：结尾越小，后面越容易接上，所以只留最小结尾。

## 讲深一层

```cpp
int lengthOfLIS(vector<int>& a) {
    vector<int> tails;
    for (int x : a) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;                    // 替换成更小的结尾
    }
    return tails.size();
}
```

注意 `tails` **不是 LIS 本身**，只是长度正确。

## 高频追问

1. **要还原 LIS 怎么做？** —— 额外记录每个元素的前驱下标。
2. **严格递增 vs 非递减？** —— 用 `lower_bound`（严格）或 `upper_bound`（允许相等）。
3. **为什么替换是对的？** —— 替换不改变已有长度的可达性，只让后续更容易接。

## 易错点

- ❌ 把 `tails` 当答案输出
- ❌ `lower_bound` 和 `upper_bound` 用混
- ✅ 说清「结尾越小越容易接」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
