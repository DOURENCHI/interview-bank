---
id: Q-1847
title: 最长连续序列：为什么只从「序列起点」开始扩展？
module: 04_algo
sub: 数组哈希
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: indexed
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [哈希, 集合]
hint: 先丢进 set，只对 n-1 不在 set 里的 n 往右数。每个元素最多访问两次，总 O(n)。
auto: true
algo_seed: true
---

## 口述答案

**套路**：先丢进 set，只对 n-1 不在 set 里的 n 往右数。每个元素最多访问两次，总 O(n)。

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
