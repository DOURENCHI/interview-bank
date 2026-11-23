---
id: Q-1882
title: 二叉树的中序遍历：迭代写法为什么要显式用栈？
module: algo
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
tags: [栈, 中序, 二叉树]
hint: 递归的调用栈要手动模拟：一路向左压栈，弹出访问后再转向右子树。
auto: true
algo_seed: true
---

## 题目

**要求**：用迭代写法实现中序遍历。

**问**：为什么必须显式用栈？

## 口述答案

> 因为中序是「左 → 根 → 右」，必须先把左链一路压到底才能访问根，
> 而递归的调用栈会自动帮你记住「回来之后该访问谁」。
> 迭代就要手动模拟这个栈：**一路向左压栈**，弹出访问，再转向右子树。

## 讲深一层

```cpp
vector<int> inorderTraversal(TreeNode* r) {
    vector<int> res;
    stack<TreeNode*> st;
    while (r || !st.empty()) {
        while (r) { st.push(r); r = r->left; }   // 一路向左
        r = st.top(); st.pop();
        res.push_back(r->val);                    // 访问
        r = r->right;                             // 转向右
    }
    return res;
}
```

前序：访问提前到入栈时；后序：用双栈或标记法。

## 高频追问

1. **前序迭代怎么写？** —— 压栈时先访问，然后压右再压左。
2. **后序迭代？** —— 前序改成「根右左」，最后反转。
3. **Morris 遍历？** —— 利用叶子节点的空右指针，O(1) 空间。

## 易错点

- ❌ 外层条件只写 `!st.empty()` —— 根还没压入时直接退出
- ❌ 忘了 `r = r->right`
- ✅ 说清「一路向左压栈」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
