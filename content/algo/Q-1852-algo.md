---
id: Q-1852
title: 随机链表的复制：哈希表里存的是什么映射？
module: algo
sub: 数组哈希
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-10
tags: [哈希, 链表]
auto: true
algo_seed: true
---

## 题目

**题目**：复制一个带随机指针的链表，新链表要完全独立（不能指向老节点）。

```
节点结构：{val, next, random}
输入：[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

**问**：哈希表里存的是什么映射？为什么必须先建完映射再连边？

## 口述答案

> 存的是 **`老节点 → 新节点`** 的映射。
> 必须先建完映射：因为 `random` 可能指向**还没创建的节点**（比如第一个节点的 random 指向最后一个）。如果边遍历边连边，遇到未创建的节点就没法设指针。所以采用两遍：第一遍只创建所有节点并建映射，第二遍按映射连 `next` 和 `random`。

## 讲深一层

```cpp
Node* copyRandomList(Node* head) {
    if (!head) return nullptr;
    unordered_map<Node*, Node*> mp;
    for (Node *p = head; p; p = p->next) mp[p] = new Node(p->val);   // 第一遍：建节点
    for (Node *p = head; p; p = p->next) {                          // 第二遍：连边
        mp[p]->next   = p->next   ? mp[p->next]   : nullptr;
        mp[p]->random = p->random ? mp[p->random] : nullptr;
    }
    return mp[head];
}
```
时间 O(n)，空间 O(n)。

**O(1) 空间的技巧（常被追问）**：把新节点直接插到老节点后面，形成 `A → A' → B → B'`；然后 `A'.random = A.random->next`；最后拆成两条链。

```cpp
// 关键三步
for (Node *p = head; p; ) { Node *n = p->next; p->next = new Node(p->val); p->next->next = n; p = n; }
for (Node *p = head; p; p = p->next->next) if (p->random) p->next->random = p->random->next;
```

## 高频追问

1. **为什么第二遍能安全连边？** —— 第一遍已经把全部节点创建好了，映射齐全，任何 `random` 目标都查得到。
2. **哈希表 key 为什么用指针？** —— 节点地址唯一；用 `val` 会在重复值上出错。
3. **深拷贝浅拷贝的区别？** —— 浅拷贝共享节点，深拷贝每个节点都是新的；这题要求深拷贝。

## 易错点

- 边遍历边连 `random`，遇到未创建节点
- 用 `val` 当哈希 key，重复值出错
- 忘了 `random` 可能为空

## 关联项目

- 无（机考基本功）

## 来源

链表 + 哈希（LeetCode 138 类题，预测题）
