---
id: Q-1877
title: 克隆图：DFS 里怎么避免重复克隆和死循环？
module: 04_algo
sub: DFS BFS
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DFS, 哈希, 图]
hint: 用哈希存「原节点→克隆节点」，进入时若已存在直接返回。
auto: true
algo_seed: true
---

## 题目

**输入**：连通无向图的节点，返回深拷贝。

**问**：DFS 里怎么避免重复克隆和死循环？

## 口述答案

> 用一个哈希表存「原节点 → 克隆节点」。进入一个节点时先查表，
> 已有就直接返回那副本，没有就新建、存表、再递归克隆它的邻居。
> 这个表同时解决了两个问题：**避免重复克隆**和**避免环导致死循环**。

## 讲深一层

```cpp
unordered_map<Node*, Node*> mp;
Node* clone(Node* n) {
    if (!n) return nullptr;
    if (mp.count(n)) return mp[n];
    Node* c = new Node(n->val);
    mp[n] = c;                                   // 先存再递归
    for (Node* nb : n->neighbors) c->neighbors.push_back(clone(nb));
    return c;
}
```

`mp[n] = c` 必须在递归之前——否则环会无限递归。

## 高频追问

1. **BFS 版怎么写？** —— 队列 + 同样的哈希表，先把节点建出来再连边。
2. **图不连通呢？** —— 外层再遍历一遍所有节点。
3. **为什么用节点指针当 key？** —— 值可能重复，指针唯一。

## 易错点

- ❌ 先递归再存表 —— 环上死循环
- ❌ 只克隆节点不克隆边
- ✅ 记住「先建节点存表，再连边」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
