---
id: Q-1876
title: 课程表 II：BFS 拓扑排序的输出顺序就是答案吗？
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
tags: [拓扑排序, BFS]
hint: 是。出队顺序即一个合法拓扑序；有环时输出长度不足，返回空。
auto: true
algo_seed: true
---

## 题目

**背景**：「课程表 I（207）」判断能否修完所有课；「课程表 II（210）」进一步要求**给出一个可行的修课顺序**。
**输入**：`numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]`
**输出**：一个拓扑序，如 `[0,1,2,3]`（答案不唯一）。
**问**：BFS 拓扑排序的输出顺序就是答案吗？怎么判无解？

## 口述答案

> 是。Kahn 算法的 BFS 天然按依赖顺序出队：入度为 0 的课先出队，出队后把它指向的课入度减一，减到 0 的接着入队——**出队序列就是一个合法修课顺序**。判无解和 I 一样：最后出队数小于总课程数，说明剩下的节点互相依赖成环，返回空数组。和 I 的代码只差一行——I 用计数器判环，II 把出队节点存进结果数组直接返回。
> 另一种做法是 DFS + 三色标记，DFS 的**后序逆序**也是拓扑序，两种都要会。

## 讲深一层

```cpp
vector<int> findOrder(int n, vector<vector<int>>& pre) {
    vector<vector<int>> g(n); vector<int> indeg(n, 0);
    for (auto& p : pre) { g[p[1]].push_back(p[0]); ++indeg[p[0]]; }
    queue<int> q;
    for (int i = 0; i < n; ++i) if (!indeg[i]) q.push(i);
    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);                       // 与 I 的唯一差别：记录顺序
        for (int v : g[u]) if (--indeg[v] == 0) q.push(v);
    }
    if ((int)order.size() != n) return {};        // 有环 → 空数组
    return order;
}
```

| | 207 课程表 I | 210 课程表 II |
|---|---|---|
| 问什么 | 能否修完 | 给出顺序 |
| 区别 | 计数判环 | 记录出队序列 |

## 高频追问

1. 拓扑序唯一吗？——不唯一；只有每步入度为 0 的节点恰有一个时才唯一
2. DFS 怎么做拓扑排序？——后序逆序； visiting/visited 三色判环
3. 用邻接矩阵还是邻接表？——稀疏图用邻接表，O(V+E)

## 易错点

- 建边方向搞反：先修课指向后修课（prerequisites[i] = [a, b] 表示先 b 后 a）
- 有环时忘了返回空数组而不是部分序列

## 关联项目

- 无（算法题）。LeetCode 按题名搜：课程表 II 210

## 来源

算法题通用解法整理（预测题，非真实面经）
