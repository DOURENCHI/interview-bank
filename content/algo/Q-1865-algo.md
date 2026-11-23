---
id: Q-1865
title: 环形链表：快慢指针为什么一定相遇？
module: algo
sub: 双指针滑窗
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [快慢指针, 链表]
hint: 进环后快指针每步追近 1，环长有限必然追上；不相遇只可能无环。
auto: true
algo_seed: true
---

## 题目

**输入**：链表头节点，判断是否有环。

**问**：快慢指针为什么一定相遇？

## 口述答案

> 快指针每次走两步、慢指针一步。如果无环，快指针先到 null，循环结束。
> 如果有环，两个指针都进环后，快指针每步**追近慢指针 1 个节点**，
> 而环长有限，所以最多「环长」步必然追上。
> 不相遇只可能是无环，不存在「一直在环里追不上」的情况。

## 讲深一层

```cpp
bool hasCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

**为什么追近 1 而不是 2**：快走 2、慢走 1，相对速度是 1，所以每步距离减 1，不会「跳过」。

## 高频追问

1. **快指针走 3 步行不行？** —— 行，也能相遇，但可能多绕几圈；走 2 最简单。
2. **找环入口呢？** —— 相遇后把一个指针放回头部，两个都每次走一步，再次相遇处即入口。
3. **为什么入口算法成立？** —— 设头到入口 a、入口到相遇点 b、环长 L，可推出 a ≡ (L-b) mod L。

## 易错点

- ❌ 循环条件漏 `fast->next` —— 空指针解引用
- ❌ 先移动后比较 / 先比较后移动的顺序混
- ✅ 记住「相对速度 1，必然追上」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
