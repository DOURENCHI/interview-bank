---
id: Q-1870
title: 岛屿数量：DFS 和 BFS 各自的取舍？
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
tags: [DFS, BFS, 网格]
hint: DFS 代码短但递归深度可能爆栈；BFS 用队列稳但要额外空间。都要把访问过的置 0 防重访。
auto: true
algo_seed: true
---

## 题目

**输入**：`grid = [["1","1","0"],["1","0","0"],["0","0","1"]]`
**输出**：`2`

**问**：DFS 和 BFS 各自的取舍？

## 口述答案

> 遍历每个格子，遇到 `'1'` 就计数加一，然后从这个格子开始把连通的所有 `'1'` 都「淹掉」（改成 `'0'`）。
> 淹的过程用 DFS（代码短）或 BFS（队列，不会爆栈）。
> 关键一步是**访问后立刻标记**，否则会重复访问甚至死循环。

## 讲深一层

```cpp
void dfs(vector<vector<char>>& g, int i, int j) {
    if (i < 0 || i >= (int)g.size() || j < 0 || j >= (int)g[0].size() || g[i][j] != '1') return;
    g[i][j] = '0';                                  // 立刻标记
    dfs(g, i+1, j); dfs(g, i-1, j); dfs(g, i, j+1); dfs(g, i, j-1);
}
int numIslands(vector<vector<char>>& g) {
    int cnt = 0;
    for (int i = 0; i < (int)g.size(); ++i)
        for (int j = 0; j < (int)g[0].size(); ++j)
            if (g[i][j] == '1') { ++cnt; dfs(g, i, j); }
    return cnt;
}
```

| 方式 | 优点 | 缺点 |
|---|---|---|
| DFS | 代码短 | 大规模网格可能爆栈 |
| BFS | 不爆栈 | 要显式队列 |

## 高频追问

1. **网格很大怎么办？** —— 改 BFS 或迭代栈，避免递归深度。
2. **不能修改原网格呢？** —— 用 `visited` 数组，多 O(mn) 空间。
3. **八连通呢？** —— 方向数组扩到 8 个。

## 易错点

- ❌ 访问后才标记（应先标记再递归）
- ❌ 边界判断漏一个方向
- ✅ 说清「淹岛」这个思路


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
