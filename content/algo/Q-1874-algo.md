---
id: Q-1874
title: 01 矩阵：多源 BFS 求最近距离怎么初始化？
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
tags: [BFS, 多源]
hint: 所有 0 入队、距离设 0，BFS 逐层外扩，第一次到达即最短。
auto: true
algo_seed: true
---

## 题目

**输入**：`mat = [[0,0,0],[0,1,0],[1,1,1]]`
**输出**：每个格子到最近 0 的距离

**问**：多源 BFS 求最近距离怎么初始化？

## 口述答案

> 把**所有 0 都入队**，距离设为 0，其余设为 -1（未访问）。
> 然后 BFS 逐层外扩，每到一个未访问格子就写「当前距离 + 1」。
> 因为是多源同时出发，**第一次到达某格时就是最短距离**，不用比较。

## 讲深一层

```cpp
vector<vector<int>> updateMatrix(vector<vector<int>>& m) {
    int R = m.size(), C = m[0].size();
    vector<vector<int>> d(R, vector<int>(C, -1));
    queue<pair<int,int>> q;
    for (int i = 0; i < R; ++i) for (int j = 0; j < C; ++j)
        if (m[i][j] == 0) { d[i][j] = 0; q.push({i,j}); }
    int dir[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    while (!q.empty()) {
        auto [i,j] = q.front(); q.pop();
        for (auto& dd : dir) {
            int x = i+dd[0], y = j+dd[1];
            if (x>=0&&x<R&&y>=0&&y<C&&d[x][y]==-1) {
                d[x][y] = d[i][j] + 1; q.push({x,y});
            }
        }
    }
    return d;
}
```

## 高频追问

1. **为什么不用对每个 1 单独 BFS？** —— 那是 O(mn) 次 BFS，太慢。
2. **DP 两遍法呢？** —— 也可以：左上、右下各扫一遍取 min，O(mn)。
3. **距离是曼哈顿距离吗？** —— 四连通 BFS 得到的就是曼哈顿距离。

## 易错点

- ❌ 只从一个 0 出发
- ❌ 用 -1 当未访问又拿它参与运算
- ✅ 说清「多源 + 首达即最短」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
