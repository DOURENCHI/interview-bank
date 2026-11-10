---
id: Q-1850
title: LRU 缓存：为什么哈希和双向链表缺一不可？
module: 04_algo
sub: 数组哈希
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-10
tags: [哈希, 链表, 设计]
auto: true
algo_seed: true
---

## 题目

**题目**：实现 LRU 缓存，`get` 和 `put` 都要 O(1)，容量满时淘汰最久未使用的。

```
容量 2：
put(1,1) put(2,2) get(1) → 1
put(3,3)            → 淘汰 2
get(2) → -1
```

**问**：为什么哈希和双向链表缺一不可？单用其中一个为什么做不到 O(1)？

## 口述答案

> 因为 LRU 需要同时做两件 O(1) 的事：**按 key 查到节点**、**把节点移到链表头**。
> 哈希表给前者，但它不知道"谁最久没用"；链表给后者（头是最新、尾是最旧、移动只需改指针），但按 key 找节点要 O(n)。两者结合：哈希存 `key → 链表节点指针`，链表维护访问顺序。
> 必须是**双向**链表：删除节点要改前驱的 `next`，单向链表拿不到前驱。

## 讲深一层

```cpp
struct Node { int k, v; Node *prev = nullptr, *next = nullptr; };

class LRUCache {
    int cap;
    unordered_map<int, Node*> mp;
    Node *head, *tail;          // 哨兵：head.next 最新，tail.prev 最旧
public:
    LRUCache(int c) : cap(c) {
        head = new Node(); tail = new Node();
        head->next = tail; tail->prev = head;
    }
    void remove(Node *p) { p->prev->next = p->next; p->next->prev = p->prev; }
    void pushFront(Node *p) {
        p->next = head->next; p->prev = head;
        head->next->prev = p; head->next = p;
    }
    int get(int key) {
        auto it = mp.find(key);
        if (it == mp.end()) return -1;
        remove(it->second); pushFront(it->second);
        return it->second->v;
    }
    void put(int key, int value) {
        if (auto it = mp.find(key); it != mp.end()) {
            it->second->v = value; remove(it->second); pushFront(it->second);
            return;
        }
        if ((int)mp.size() == cap) {
            Node *old = tail->prev; remove(old); mp.erase(old->k); delete old;
        }
        Node *p = new Node{key, value};
        pushFront(p); mp[key] = p;
    }
};
```

| 结构 | 提供什么 | 缺什么 |
|---|---|---|
| 哈希表 | O(1) 按 key 定位 | 不知道访问顺序 |
| 单向链表 | 顺序 | 删除需前驱，O(n) |
| 双向链表 | O(1) 移动/删除 | 按 key 定位 O(n) |

**哨兵节点的作用**：省掉"链表为空""操作头尾"的特殊判断，代码少一半 bug。

## 高频追问

1. **`put` 已存在的 key 要注意什么？** —— 更新值之外还要把节点移到头部，否则淘汰顺序错。
2. **为什么不用 `std::list`？** —— 可以，`list::splice` 能把节点移到头部且不失效迭代器，代码更短；手写双向链表更能展示基本功。
3. **LFU 怎么做？** —— 需要"频率 → 双向链表"的桶，再加一个记录最小频率的变量。

## 易错点

- 用单向链表，删除时拿不到前驱
- `put` 更新已有 key 时忘了移到头部
- 淘汰时删了链表节点却没从哈希表删 key

## 关联项目

- 无（机考基本功）

## 来源

设计题（LeetCode 146 类题，预测题）
