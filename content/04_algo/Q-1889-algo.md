---
id: Q-1889
title: 零钱兑换：为什么贪心不行，必须 DP？
module: 04_algo
sub: DP
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: indexed
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DP, 完全背包]
hint: 面额组合下贪心会错过更优解。dp[j]=min(dp[j], dp[j-coin]+1) 求最少硬币数。
auto: true
algo_seed: true
---

## 口述答案

> 待补充。这题要能边说边写：先说思路和复杂度，再写代码，最后主动说边界。

**套路**：面额组合下贪心会错过更优解。dp[j]=min(dp[j], dp[j-coin]+1) 求最少硬币数。

## 讲深一层

待补充。补三件事：为什么这个套路成立、复杂度怎么算、和哪道题是同一模板。

## 高频追问

待补充。常见追问方向：换数据规模怎么办、能不能做到 O(1) 空间、有负数还成立吗。

## 易错点

待补充。

## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

按华为机考题型分布推导（数组/字符串/哈希 40%、双指针滑窗 20%、DFS/BFS 20%、DP 20%）
