---
id: Q-1827
title: 最大子数组和：Kadane 算法为什么只需两个变量？
module: 04_algo
sub: 数组哈希
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DP, 贪心, 数组]
hint: 以 i 结尾的最大和 = max(nums[i], 前一个最大和 + nums[i])。负数前缀直接丢掉，不用回溯。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [-2,1,-3,4,-1,2,1,-5,4]`
**输出**：`6`（子数组 `[4,-1,2,1]`）

**问**：Kadane 算法为什么只需要两个变量？

## 口述答案

> 定义「以 i 结尾的最大和」，递推是 `cur = max(nums[i], cur + nums[i])`。
> 意思是：前面的累加如果是负的，不如从头开始。
> 同时用一个变量记全局最大。
> 两个变量就够，因为状态只依赖前一个——不需要数组存所有历史。

## 讲深一层

```cpp
int maxSubArray(vector<int>& a) {
    int cur = a[0], best = a[0];
    for (int i = 1; i < (int)a.size(); ++i) {
        cur = max(a[i], cur + a[i]);   // 负前缀直接丢弃
        best = max(best, cur);
    }
    return best;
}
```

时间 O(n)，空间 O(1)。

| 方法 | 时间 | 说明 |
|---|---|---|
| 暴力枚举 | O(n³)/O(n²) | 不实用 |
| 分治 | O(n log n) | 可解「任意区间」变体 |
| **Kadane** | **O(n)** | 最优 |

## 高频追问

1. **要返回子数组本身呢？** —— 记 `start`，当 `cur` 重置时更新起点。
2. **全是负数怎么办？** —— 初始化用 `a[0]` 而不是 0，否则会返回 0。
3. **是 DP 还是贪心？** —— 是 DP（状态定义 + 转移）；说贪心也不算错，因为每步只做局部最优取舍。

## 易错点

- ❌ 初始化成 0 —— 全负数时返回 0 是错的
- ❌ 忘了更新 best
- ✅ 说清「负前缀不如重开」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
