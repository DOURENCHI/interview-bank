---
id: Q-1895
title: 最小路径和：二维 DP 怎么压缩成一维？
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
tags: [DP, 滚动数组]
hint: 原地按行更新：dp[j]=min(dp[j], dp[j-1])+grid[i][j]。dp[j] 来自上方，dp[j-1] 来自左方。
auto: true
algo_seed: true
---

## 口述答案

**套路**：原地按行更新：dp[j]=min(dp[j], dp[j-1])+grid[i][j]。dp[j] 来自上方，dp[j-1] 来自左方。

（口述版待补：先说思路和复杂度，再写代码，最后主动说边界。）

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
