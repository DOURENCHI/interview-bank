---
id: Q-1834
title: 矩阵置零：不用额外空间怎么标记要清零的行列？
module: 04_algo
sub: 数组哈希
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [矩阵, 原地]
hint: 用第一行和第一列当标记位，另外单独记第一行、第一列本身是否需要清零。
auto: true
algo_seed: true
---

## 题目

**输入**：`[[1,1,1],[1,0,1],[1,1,1]]`
**输出**：`[[1,0,1],[0,0,0],[1,0,1]]`
**要求**：原地修改。

**问**：不用额外空间怎么标记要清零的行列？

## 口述答案

> 用**第一行和第一列当标记位**：遇到 `m[i][j] == 0`，就把 `m[i][0]` 和 `m[0][j]` 置 0。
> 但这样会污染第一行/第一列本身的原始信息，所以要**先用两个布尔变量记下第一行和第一列原本是否有 0**。
> 最后按标记清零，再单独处理第一行和第一列。

## 讲深一层

```cpp
void setZeroes(vector<vector<int>>& m) {
    int R = m.size(), C = m[0].size();
    bool row0 = false, col0 = false;
    for (int j = 0; j < C; ++j) if (!m[0][j]) row0 = true;
    for (int i = 0; i < R; ++i) if (!m[i][0]) col0 = true;

    for (int i = 1; i < R; ++i)
        for (int j = 1; j < C; ++j)
            if (!m[i][j]) { m[i][0] = 0; m[0][j] = 0; }

    for (int i = 1; i < R; ++i)
        for (int j = 1; j < C; ++j)
            if (!m[i][0] || !m[0][j]) m[i][j] = 0;

    if (row0) for (int j = 0; j < C; ++j) m[0][j] = 0;
    if (col0) for (int i = 0; i < R; ++i) m[i][0] = 0;
}
```

## 高频追问

1. **为什么不用 set 存行列？** —— 那样是 O(m+n) 空间，题目要求原地。
2. **只用两个布尔够吗？** —— 够，因为第一行/列既当标记又需要单独记录。
3. **顺序能反吗？** —— 不能，必须先标记后清零，否则标记被清零操作破坏。

## 易错点

- ❌ 先清零再标记 —— 标记全被破坏
- ❌ 忘了单独处理第一行/第一列
- ✅ 说清「借用第一行/列 + 两个布尔」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
