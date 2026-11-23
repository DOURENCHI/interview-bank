---
id: Q-1866
title: 相交链表：长度差法和「走两遍」各自原理？
module: algo
sub: 双指针滑窗
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [双指针, 链表]
hint: 走两遍：a 走完接 b、b 走完接 a，路径等长必然同时到交点。长度差法本质相同。
auto: true
algo_seed: true
---

## 题目

**输入**：两个链表头节点，返回第一个公共节点（无则 null）。

**问**：长度差法和「走两遍」各自的原理？

## 口述答案

> 「走两遍」最优雅：指针 A 走完链表 A 接着走 B，指针 B 走完 B 接着走 A，
> 两者走的总路程相同（a+b），所以**一定同时到达交点**；若无交点则同时到 null。
> 长度差法本质相同：先算出长度差，让长的先走差那么多步，再同时走。
> 前者代码更短，后者更好理解。

## 讲深一层

```cpp
ListNode *getIntersectionNode(ListNode *ha, ListNode *hb) {
    ListNode *a = ha, *b = hb;
    while (a != b) {
        a = a ? a->next : hb;
        b = b ? b->next : ha;
    }
    return a;
}
```

循环终止条件 `a != b`：要么在交点相遇，要么都变成 null。

## 高频追问

1. **会死循环吗？** —— 不会，最多 2×(a+b) 步。
2. **长度差法怎么算？** —— 两次遍历求长度，长的先走 |diff| 步。
3. **如何判断有交点？** —— 看两个尾节点是否相同。

## 易错点

- ❌ 用值相等判断交点 —— 值可能重复
- ❌ 走两遍时忘了在 null 时切换
- ✅ 说清「总路程相同所以同时到达」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
