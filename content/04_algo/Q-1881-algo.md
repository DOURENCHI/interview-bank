---
id: Q-1881
title: 验证二叉搜索树：为什么只比较父子不够？
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
tags: [DFS, BST, 中序]
hint: 要保证整个左子树都小于根，得传上下界，或用中序遍历检查严格递增。
auto: true
algo_seed: true
---

## 题目

**输入**：二叉树，判断是否为 BST。

**问**：为什么只比较父子不够？

## 口述答案

> 因为 BST 要求**整棵左子树都小于根**，不只是左孩子。
> 反例：根 5，左孩子 4，4 的右孩子 6 —— 局部 4<5 成立，但 6 在左子树里却大于根。
> 正确做法有两种：**传上下界**（递归时带 `[min, max]`），
> 或者**中序遍历检查严格递增**。

## 讲深一层

```cpp
bool check(TreeNode* r, long lo, long hi) {
    if (!r) return true;
    if (r->val <= lo || r->val >= hi) return false;
    return check(r->left, lo, r->val) && check(r->right, r->val, hi);
}
bool isValidBST(TreeNode* r) { return check(r, LONG_MIN, LONG_MAX); }
```

用 `long` 是因为节点值可能就是 `INT_MIN`/`INT_MAX`。

中序版：记录前一个节点，要求严格递增。

## 高频追问

1. **等于算不算 BST？** —— 标准定义不允许重复，用严格不等。
2. **中序版怎么写？** —— 递归左、比较 pre、递归右。
3. **为什么用 long？** —— 避免边界值被误判。

## 易错点

- ❌ 只比较父子 —— 漏判深层
- ❌ 用 int 当界的初值
- ✅ 记住「传上下界」或「中序递增」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
