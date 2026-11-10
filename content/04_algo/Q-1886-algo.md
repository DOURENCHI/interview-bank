---
id: Q-1886
title: 打家劫舍：状态转移里「选或不选」怎么表达？
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
tags: [DP, 线性]
hint: dp[i]=max(dp[i-1], dp[i-2]+nums[i])：不偷当前就继承前一个，偷当前就得跳过前一个。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [2,7,9,3,1]`
**输出**：`12`（偷 2 + 9 + 1）
**限制**：不能偷相邻两家。

**问**：状态转移里「选或不选」怎么表达？

## 口述答案

> `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`。
> 意思是：不偷第 i 家，就等于前 i-1 家的最优；偷第 i 家，就得跳过 i-1，取前 i-2 家的最优再加。
> 两个选择取大。
> 同样可以滚动成两个变量。

## 讲深一层

```cpp
int rob(vector<int>& a) {
    int prev = 0, cur = 0;               // dp[i-2], dp[i-1]
    for (int x : a) {
        int t = max(cur, prev + x);
        prev = cur; cur = t;
    }
    return cur;
}
```

| 状态定义 | 转移 |
|---|---|
| dp[i] = 前 i 家最大 | max(dp[i-1], dp[i-2]+a[i]) |
| 滚动 | prev/cur 两变量 |

## 高频追问

1. **环形房屋？** —— 拆成「不含首」和「不含尾」两次（见打家劫舍 II）。
2. **树形房屋？** —— 树形 DP，返回「偷/不偷」两个值。
3. **能连续偷两家呢？** —— 状态扩展成「最近一次偷的是距离 k」。

## 易错点

- ❌ `dp[i-1]` 和 `dp[i-2]` 混
- ❌ 滚动时更新顺序错
- ✅ 说清「偷当前就必须跳过前一个」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
