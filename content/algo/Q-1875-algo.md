---
id: Q-1875
title: 课程表：拓扑排序怎么判断有环？
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
hint: 统计入度，入度为 0 的入队；出队计数若小于节点总数，剩下那些就在环里。
auto: true
algo_seed: true
---

## 题目

**输入**：`numCourses = 2, prerequisites = [[1,0]]`（学 1 前要先学 0）
**输出**：能否修完（即图中有无环）

**问**：拓扑排序怎么判断有环？

## 口述答案

> 统计每个节点的入度，入度为 0 的先入队；出队时把它指向的节点入度减一，减到 0 就入队。
> 最后看**出队节点数是否等于总节点数**：少了就说明剩下的节点互相依赖，在环里。
> 这就是 Kahn 算法。

## 讲深一层

```cpp
bool canFinish(int n, vector<vector<int>>& pre) {
    vector<vector<int>> g(n);
    vector<int> indeg(n, 0);
    for (auto& p : pre) { g[p[1]].push_back(p[0]); ++indeg[p[0]]; }
    queue<int> q;
    for (int i = 0; i < n; ++i) if (!indeg[i]) q.push(i);
    int done = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop(); ++done;
        for (int v : g[u]) if (--indeg[v] == 0) q.push(v);
    }
    return done == n;
}
```

| 方法 | 判断环 |
|---|---|
| Kahn（BFS） | 完成数 < n 则有环 |
| DFS 三色标记 | 遇到「正在访问」的节点则有环 |

## 高频追问

1. **DFS 版怎么写？** —— 白/灰/黑三色，灰色表示在当前路径上，遇到灰色即有环。
2. **为什么入度 0 可以安全移除？** —— 没有前驱依赖了。
3. **有多个解怎么办？** —— 拓扑序不唯一，Kahn 出队顺序即一个合法解。

## 易错点

- ❌ 忘了把 `prerequisites` 的方向建对（先学 → 后学）
- ❌ 用「出队数 == n」判断写成 `<=`
- ✅ 说清「完成数不足即环」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
