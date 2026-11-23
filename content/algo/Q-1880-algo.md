---
id: Q-1880
title: 二叉树的层序遍历：为什么必须用队列？
module: algo
sub: DFS BFS
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [BFS, 队列, 二叉树]
hint: 队列先进先出保证按层顺序，用栈会变成深度优先。每轮先记下当前层节点数再处理。
auto: true
algo_seed: true
---

## 题目

**输入**：二叉树根节点
**输出**：`[[3],[9,20],[15,7]]`

**问**：为什么必须用队列？

## 口述答案

> 队列先进先出，保证**同一层的节点按顺序被处理、下一层的节点排在后面**。
> 用栈会变成深度优先，就不是按层了。
> 实现上每轮先记下**当前层的节点数 `q.size()`**，只处理这么多个，
> 就能自然分层。

## 讲深一层

```cpp
vector<vector<int>> levelOrder(TreeNode* r) {
    vector<vector<int>> res;
    if (!r) return res;
    queue<TreeNode*> q{{r}};
    while (!q.empty()) {
        int sz = q.size();
        vector<int> lv;
        for (int i = 0; i < sz; ++i) {
            auto* n = q.front(); q.pop();
            lv.push_back(n->val);
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        res.push_back(lv);
    }
    return res;
}
```

`sz` 必须在循环**之前**取——循环中 size 会变。

## 高频追问

1. **锯齿形层序？** —— 偶数层反转。
2. **右视图？** —— 每层取最后一个。
3. **不用 sz 行不行？** —— 用两个队列或加层标记。

## 易错点

- ❌ 循环里用 `q.size()` 当条件 —— 会处理到新入队的
- ❌ 忘了判空树
- ✅ 记住「先取 size 再循环」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
