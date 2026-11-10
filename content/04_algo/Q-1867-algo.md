---
id: Q-1867
title: 回文链表：O(1) 空间怎么做？
module: 04_algo
sub: 双指针滑窗
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [快慢指针, 反转链表]
hint: 快慢指针找中点，反转后半段，再逐个比较。注意奇偶长度的中点处理。
auto: true
algo_seed: true
---

## 题目

**输入**：链表头节点，判断是否回文。
**要求**：O(n) 时间，O(1) 空间。

**问**：不额外开数组怎么做？

## 口述答案

> 三步：**快慢指针找中点** → **反转后半段** → **逐个比较**。
> 奇偶长度的处理要小心：奇数长度时慢指针正好在中点，后半段从中点的下一个开始比。
> 比较完可以把后半段再反转回来（好习惯，但不强制）。

## 讲深一层

```cpp
bool isPalindrome(ListNode* head) {
    if (!head || !head->next) return true;
    ListNode *slow = head, *fast = head;
    while (fast->next && fast->next->next) {     // 奇数时 slow 停在中点
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode *p = reverse(slow->next);           // 反转后半段
    ListNode *q = head;
    while (p) {
        if (p->val != q->val) return false;
        p = p->next; q = q->next;
    }
    return true;
}
```

循环条件用 `fast->next && fast->next->next` 而不是 `fast && fast->next`——后者偶数时 `slow` 会落在右中点，切分点要跟着变。

## 高频追问

1. **奇偶怎么统一？** —— 上面写法让 `slow` 总是左中点，`slow->next` 开始反转即可。
2. **比较完要恢复链表吗？** —— 严谨的话要，否则调用方的链表被改了。
3. **能用栈吗？** —— 能，但 O(n) 空间。

## 易错点

- ❌ 快慢指针条件写错 —— 中点位置偏一位
- ❌ 忘了判断空链表和单节点
- ✅ 掌握「找中点 + 反转 + 比较」三步


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
