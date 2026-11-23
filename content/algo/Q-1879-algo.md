---
id: Q-1879
title: 二叉树的最大深度：递归和层序各自怎么算？
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
tags: [DFS, BFS, 二叉树]
hint: 递归 1+max(左,右)；层序数层数。前者更短，后者能顺带拿到宽度。
auto: true
algo_seed: true
---

## 题目

**输入**：二叉树根节点，返回最大深度。

**问**：递归和层序各自怎么算？

## 口述答案

> 递归：`maxDepth(root) = 1 + max(左, 右)`，空节点返回 0。
> 层序：用队列按层遍历，每处理完一层层数加一。
> 前者代码最短；后者能顺带拿到宽度、某层节点等信息。

## 讲深一层

```cpp
int maxDepth(TreeNode* r) {
    if (!r) return 0;
    return 1 + max(maxDepth(r->left), maxDepth(r->right));
}
```

层序版：

```cpp
int maxDepth(TreeNode* r) {
    if (!r) return 0;
    queue<TreeNode*> q{{r}};
    int d = 0;
    while (!q.empty()) {
        for (int i = q.size(); i > 0; --i) {
            auto* n = q.front(); q.pop();
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        ++d;
    }
    return d;
}
```

## 高频追问

1. **最小深度呢？** —— 注意只有单侧子树时不能直接取 min（那是 0）。
2. **会爆栈吗？** —— 深度大时会，改迭代。
3. **平衡二叉树判断？** —— 后序遍历，返回高度并检查左右差。

## 易错点

- ❌ 空节点返回 1
- ❌ 最小深度直接取 min 忽略单侧
- ✅ 说清两种方法的取舍


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
