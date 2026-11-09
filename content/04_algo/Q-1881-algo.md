---
id: Q-1881
title: 二叉树的层序遍历：为什么必须用队列？
module: 04_algo
sub: DFS BFS
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: indexed
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [BFS, 队列, 二叉树]
hint: 队列先进先出保证按层顺序，用栈会变成深度优先。每轮先记下当前层节点数再处理。
auto: true
algo_seed: true
---

## 口述答案

**套路**：队列先进先出保证按层顺序，用栈会变成深度优先。每轮先记下当前层节点数再处理。

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
