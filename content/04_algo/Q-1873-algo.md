---
id: Q-1873
title: 腐烂的橘子：多源 BFS 的分钟数怎么算？
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
tags: [BFS, 多源]
hint: 所有腐烂橘子同时入队作为第 0 层，每扩一层 minutes+1；结束后还有新鲜橘子则返回 -1。
auto: true
algo_seed: true
---

## 题目

**输入**：`grid = [[2,1,1],[1,1,0],[0,1,1]]`（2 腐烂、1 新鲜、0 空）
**输出**：`4`（分钟数），无法全部腐烂返回 -1。

**问**：多源 BFS 的分钟数怎么算？

## 口述答案

> 所有腐烂橘子**同时入队**作为第 0 层，然后逐层 BFS，每扩一层分钟数加一。
> BFS 结束后再检查是否还有新鲜橘子，有就返回 -1。
> 关键点是「同时入队」——这保证每一层都是同一时刻被感染的，层数才等价于时间。

## 讲深一层

```cpp
int orangesRotting(vector<vector<int>>& g) {
    int R = g.size(), C = g[0].size(), fresh = 0;
    queue<pair<int,int>> q;
    for (int i = 0; i < R; ++i) for (int j = 0; j < C; ++j) {
        if (g[i][j] == 2) q.push({i,j});
        else if (g[i][j] == 1) ++fresh;
    }
    if (!fresh) return 0;
    int dir[4][2] = {{1,0},{-1,0},{0,1},{0,-1}}, mins = 0;
    while (!q.empty()) {
        int sz = q.size();
        bool spread = false;
        for (int k = 0; k < sz; ++k) {
            auto [i,j] = q.front(); q.pop();
            for (auto& d : dir) {
                int x = i+d[0], y = j+d[1];
                if (x>=0&&x<R&&y>=0&&y<C&&g[x][y]==1) {
                    g[x][y] = 2; q.push({x,y}); --fresh; spread = true;
                }
            }
        }
        if (spread) ++mins;
    }
    return fresh ? -1 : mins;
}
```

## 高频追问

1. **为什么要按层（记 size）循环？** —— 不按层就没法算分钟数。
2. **初始没有腐烂橘子但有新鲜的？** —— 直接返回 -1。
3. **没有新鲜橘子？** —— 返回 0。

## 易错点

- ❌ 一个一个入队 —— 层数不等于时间
- ❌ 忘了最后检查 fresh
- ✅ 说清「多源同时入队 = 同一时刻」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
