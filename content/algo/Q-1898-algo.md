---
id: Q-1898
title: 股票买卖含冷冻期：状态机 DP 有哪几个状态？
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
tags: [DP, 状态机]
hint: 持有 / 不持有且冷冻 / 不持有可买，三态转移。状态定义清楚，转移就自然。
auto: true
algo_seed: true
---

## 题目

**规则**：卖出后第二天不能买（冷冻一天），可交易多次。
**问**：状态机 DP 有哪几个状态？

## 口述答案

> 三个状态：**持有股票**、**不持有且在冷冻期**、**不持有且可买**。
> 转移：
> 持有 = max(昨天持有, 昨天可买 - 今天价格)；
> 冷冻 = 昨天持有 + 今天价格（今天卖出）；
> 可买 = max(昨天可买, 昨天冷冻)。
> 答案取「冷冻」和「可买」的较大值。

## 讲深一层

```cpp
int maxProfit(vector<int>& p) {
    int hold = INT_MIN, freeze = 0, free_ = 0;
    for (int x : p) {
        int nh = max(hold, free_ - x);
        int nf = hold + x;
        int nfree = max(free_, freeze);
        hold = nh; freeze = nf; free_ = nfree;
    }
    return max(freeze, free_);
}
```

## 高频追问

1. **为什么 `hold` 初始化成 `INT_MIN`？** —— 表示「还没买」，非法状态，不能被选中。
2. **冷冻期两天呢？** —— 加一个状态或用队列记历史。
3. **含手续费？** —— 卖出时减手续费。

## 易错点

- ❌ 状态定义不清就直接写转移
- ❌ 用新值算旧状态（要先存临时变量）
- ✅ 先把三个状态和转移写清楚


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
