---
id: Q-1828
title: 买卖股票的最佳时机：一次遍历怎么同时维护最低价和利润？
module: algo
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
tags: [数组, 贪心]
hint: 先更新历史最低买入价，再用当天价格减它更新利润。顺序不能反，否则会自己减自己。
auto: true
algo_seed: true
---

## 题目

**输入**：`prices = [7,1,5,3,6,4]`
**输出**：`5`（第 2 天买 1，第 5 天卖 6）
**限制**：只能买卖一次。

**问**：一次遍历怎么同时维护最低价和最大利润？

## 口述答案

> 遍历时维护两个量：到目前为止的最低买入价 `minPrice`，和最大利润 `best`。
> 每天先看「今天卖能赚多少」= `prices[i] - minPrice`，更新 best；
> 再用今天价格更新 minPrice。
> **顺序不能反**——先更新 minPrice 再用它算利润，会变成「今天买今天卖」，利润恒为 0。

## 讲深一层

```cpp
int maxProfit(vector<int>& p) {
    int minP = INT_MAX, best = 0;
    for (int x : p) {
        best = max(best, x - minP);   // 先算利润
        minP = min(minP, x);          // 再更新最低价
    }
    return best;
}
```

## 高频追问

1. **能买卖多次呢？** —— 累加所有上涨段：`if (p[i] > p[i-1]) sum += p[i] - p[i-1]`。
2. **含冷冻期呢？** —— 变成状态机 DP（持有/冷冻/可买三态）。
3. **最多两笔呢？** —— 用四个变量分别记录第一次买/卖、第二次买/卖的极值。

## 易错点

- ❌ 两个操作顺序反了
- ❌ `best` 初始化成 `INT_MIN` 但没处理空数组
- ✅ 记住「先算利润再更新最低价」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
