---
id: Q-1883
title: 路径总和 II：回溯时怎么恢复路径？
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
tags: [回溯, DFS, 二叉树]
hint: 进入节点 push，递归左右，返回前 pop。少一次 pop 就会串路径。
auto: true
algo_seed: true
---

## 题目

**输入**：二叉树 + 目标和，找出所有「根到叶子」路径和等于目标。

**问**：回溯时怎么恢复路径？

## 口述答案

> 进入节点先 `push`，递归左右，**返回前 `pop`**。
> 少一次 pop 就会把别的分支的节点留在路径里，结果串成一堆错路径。
> 判断时机在叶子节点：左右都空时检查当前和是否等于目标。

## 讲深一层

```cpp
void dfs(TreeNode* r, int need, vector<int>& path, vector<vector<int>>& res) {
    if (!r) return;
    path.push_back(r->val);
    need -= r->val;
    if (!r->left && !r->right && need == 0) res.push_back(path);
    dfs(r->left, need, path, res);
    dfs(r->right, need, path, res);
    path.pop_back();                             // 关键
}
```

## 高频追问

1. **为什么要判叶子？** —— 不判的话中途满足也会被收，但那不是完整路径。
2. **有负数节点要注意什么？** —— 不能提前剪枝（后面可能变回来）。
3. **只求是否存在？** —— 那就不用记录路径，直接返回 bool。

## 易错点

- ❌ 忘了 pop
- ❌ 不判叶子
- ✅ 说清「进 push、出 pop」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
