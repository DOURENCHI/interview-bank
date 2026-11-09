---
id: Q-1851
title: LRU 缓存：为什么哈希和双向链表缺一不可？
module: 04_algo
sub: 数组哈希
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: indexed
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [哈希, 链表, 设计]
hint: 哈希给 O(1) 定位，双向链表给 O(1) 挪到表头或删尾。单链表删节点还要找前驱，不满足 O(1)。
auto: true
algo_seed: true
---

## 口述答案

**套路**：哈希给 O(1) 定位，双向链表给 O(1) 挪到表头或删尾。单链表删节点还要找前驱，不满足 O(1)。

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
