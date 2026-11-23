---
id: Q-1872
title: 被围绕的区域：为什么从边界反向 DFS？
module: algo
sub: DFS BFS
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DFS, 网格, 反向思维]
hint: 与边界连通的 O 一定不会被围。先标记这些，剩下的 O 才翻成 X，正向判断要复杂得多。
auto: true
algo_seed: true
---

## 题目

**输入**：`board`，把被 `'X'` 完全包围的 `'O'` 翻成 `'X'`，边界上的 `'O'` 保留。

**问**：为什么从边界反向 DFS？

## 口述答案

> 正向判断「这个 O 是否被包围」要搜到边界才知道，每个 O 都可能搜一遍，代价高。
> 反过来想：**与边界连通的 O 一定不会被包围**。所以先从四条边上的 O 出发，
> 把能到达的都标记成特殊字符（如 `'#'`），这些是安全区；
> 最后扫一遍：安全区还原成 O，剩下的 O 翻成 X。

## 讲深一层

```cpp
void dfs(vector<vector<char>>& b, int i, int j) {
    if (i<0||i>=(int)b.size()||j<0||j>=(int)b[0].size()||b[i][j]!='O') return;
    b[i][j] = '#';
    dfs(b,i+1,j); dfs(b,i-1,j); dfs(b,i,j+1); dfs(b,i,j-1);
}
void solve(vector<vector<char>>& b) {
    int R = b.size(), C = b[0].size();
    for (int i = 0; i < R; ++i) { dfs(b,i,0); dfs(b,i,C-1); }
    for (int j = 0; j < C; ++j) { dfs(b,0,j); dfs(b,R-1,j); }
    for (auto& row : b) for (auto& c : row)
        c = (c == '#') ? 'O' : 'X';
}
```

## 高频追问

1. **为什么标 `'#'` 而不是直接改 `'O'`？** —— 需要区分「安全」和「原始」，最后统一归一化。
2. **能不用递归吗？** —— 用栈或队列做 BFS。
3. **只翻内部所有 O 呢？** —— 那就是全翻，不用判断。

## 易错点

- ❌ 正向逐个判断 —— 复杂度高
- ❌ 忘了四条边都要扫
- ✅ 记住「从边界反推安全区」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
