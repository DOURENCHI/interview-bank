---
id: Q-1884
title: N 皇后：怎么用三个数组做到 O(1) 冲突判断？
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
tags: [回溯, 位运算]
hint: 列数组、主对角线（row-col+n）、副对角线（row+col）。放前查三个，放完标记，回溯时撤销。
auto: true
algo_seed: true
---

## 题目

**输入**：`n = 4`
**输出**：所有解的布局，共 2 个。

**问**：怎么用三个数组做到 O(1) 冲突判断？

## 口述答案

> 逐行放置，每行一个皇后。冲突只有三种：同列、同主对角线、同副对角线。
> 用三个布尔数组：`col[j]`、`diag1[row-j+n]`、`diag2[row+j]`。
> 放之前查三个，放完标记三个，回溯时撤销三个。
> 这样判断冲突是 O(1)，不用每次扫棋盘。

## 讲深一层

```cpp
void solve(int row, int n, vector<int>& pos,
           vector<bool>& col, vector<bool>& d1, vector<bool>& d2,
           vector<vector<string>>& res) {
    if (row == n) { /* 生成答案 */ return; }
    for (int j = 0; j < n; ++j) {
        if (col[j] || d1[row-j+n] || d2[row+j]) continue;
        col[j] = d1[row-j+n] = d2[row+j] = true;
        pos[row] = j;
        solve(row+1, n, pos, col, d1, d2, res);
        col[j] = d1[row-j+n] = d2[row+j] = false;
    }
}
```

对角线下标的推导：主对角线满足 `row - j` 为常数（加 n 避免负下标），副对角线满足 `row + j` 为常数。

## 高频追问

1. **为什么按行放？** —— 每行一个，天然排除行冲突。
2. **位运算优化？** —— 用整数位表示列和对角线占用，更快。
3. **N=8 有多少解？** —— 92 个。

## 易错点

- ❌ 对角线下标不加偏移 —— 负下标越界
- ❌ 回溯时忘撤销
- ✅ 记住 `row-j+n` 和 `row+j`


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
