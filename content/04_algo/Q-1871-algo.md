---
id: Q-1871
title: 岛屿的最大面积：怎么在递归里累计面积？
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
tags: [DFS, 网格]
hint: dfs 返回 1 + 四周返回值之和，越界或为 0 时返回 0。
auto: true
algo_seed: true
---

## 题目

**输入**：`grid = [[0,0,1,0],[1,1,1,0],[0,1,0,0]]`
**输出**：`4`

**问**：怎么在递归里累计面积？

## 口述答案

> `dfs` 返回 `1 + 四周返回值之和`，越界或为 0 时返回 0。
> 本质是把「这格算 1 个，再加上邻居的」写成递归式。
> 同样要访问后立刻置 0。

## 讲深一层

```cpp
int dfs(vector<vector<int>>& g, int i, int j) {
    if (i < 0 || i >= (int)g.size() || j < 0 || j >= (int)g[0].size() || g[i][j] == 0) return 0;
    g[i][j] = 0;
    return 1 + dfs(g,i+1,j) + dfs(g,i-1,j) + dfs(g,i,j+1) + dfs(g,i,j-1);
}
int maxAreaOfIsland(vector<vector<int>>& g) {
    int best = 0;
    for (int i = 0; i < (int)g.size(); ++i)
        for (int j = 0; j < (int)g[0].size(); ++j)
            if (g[i][j]) best = max(best, dfs(g, i, j));
    return best;
}
```

## 高频追问

1. **会不会重复计数？** —— 不会，置 0 后不会再进入。
2. **最大岛屿的坐标也要？** —— 额外记录路径。
3. **和岛屿数量的区别？** —— 一个计数连通块，一个求最大块。

## 易错点

- ❌ 忘了 `g[i][j] = 0`
- ❌ 返回值写成 `+1` 的位置错
- ✅ 说清「1 + 四周之和」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
