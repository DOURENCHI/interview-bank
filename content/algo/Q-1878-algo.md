---
id: Q-1878
title: 单词搜索：回溯的剪枝和状态恢复怎么做？
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
tags: [回溯, DFS, 网格]
hint: 越界或不匹配立即返回 false；匹配后临时标记已访问，四方向递归，返回前恢复。
auto: true
algo_seed: true
---

## 题目

**输入**：`board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`, `word = "ABCCED"`
**输出**：`true`

**问**：回溯的剪枝和状态恢复怎么做？

## 口述答案

> 从每个格子出发尝试匹配第一个字符，匹配就递归四个方向匹配下一个字符。
> 剪枝：越界、字符不匹配**立刻返回 false**，不回退尝试。
> 状态恢复：匹配后**临时把该格改成特殊字符**标记已访问，四个方向递归完再改回来——
> 不恢复会污染其他分支。

## 讲深一层

```cpp
bool dfs(vector<vector<char>>& b, string& w, int i, int j, int k) {
    if (k == (int)w.size()) return true;
    if (i<0||i>=(int)b.size()||j<0||j>=(int)b[0].size()||b[i][j]!=w[k]) return false;
    char tmp = b[i][j];
    b[i][j] = '#';                                  // 标记
    bool ok = dfs(b,w,i+1,j,k+1) || dfs(b,w,i-1,j,k+1)
           || dfs(b,w,i,j+1,k+1) || dfs(b,w,i,j-1,k+1);
    b[i][j] = tmp;                                  // 恢复
    return ok;
}
```

## 高频追问

1. **为什么要恢复？** —— 同一条路径不能重复用同一格，但不同起点可以。
2. **能提前剪枝吗？** —— 统计字符频次，若 word 里某字符比 board 多，直接 false。
3. **复杂度？** —— O(mn × 4^L)，L 为单词长度。

## 易错点

- ❌ 不恢复状态 —— 后续路径被堵死
- ❌ 先判 k 还是先判边界，顺序错会越界
- ✅ 说清「标记—递归—恢复」三步


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
