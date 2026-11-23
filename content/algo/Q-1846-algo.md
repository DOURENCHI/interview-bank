---
id: Q-1846
title: 最长连续序列：为什么只从「序列起点」开始扩展？
module: algo
sub: 数组哈希
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-10
tags: [哈希, 集合]
auto: true
algo_seed: true
---

## 题目

**题目**：给定未排序数组，求最长连续序列的长度，要求 O(n)。

```
输入：[100,4,200,1,3,2]
输出：4     （序列 1,2,3,4）
```

**问**：为什么只从「序列起点」开始扩展？怎么判断一个数是不是起点？

## 口述答案

> 因为如果对每个数都往两边扩，同一段连续序列会被重复遍历多次，复杂度退化到 O(n²)。
> 判断起点很简单：**`x` 是起点，当且仅当 `x-1` 不在集合里**。只有起点才做扩展，每个元素最多被访问两次，整体 O(n)。

## 讲深一层

```cpp
int longestConsecutive(vector<int>& nums) {
    unordered_set<int> st(nums.begin(), nums.end());
    int best = 0;
    for (int x : st) {
        if (st.count(x - 1)) continue;      // 不是起点，跳过
        int y = x;
        while (st.count(y + 1)) ++y;        // 从起点一路往上数
        best = max(best, (int)(y - x + 1));
    }
    return best;
}
```

**复杂度分析要讲清**：外层循环遍历 n 个元素，内层 `while` 只在起点执行，而每个元素最多成为某条序列的一部分一次，所以内层总执行次数 ≤ n，整体 O(n)。

**为什么不能用排序**：排序是 O(n log n)，题目要求 O(n)，而且排序会改变"原始下标"信息（如果题目要返回下标就不能排）。

## 高频追问

1. **`unordered_set` 会比 `set` 快多少？** —— 平均 O(1) vs O(log n)，这里查询次数多，差别明显。
2. **要返回序列本身怎么办？** —— 记录起点和长度，最后重建；或者用 `map<int,int>` 记录每个端点的长度（并查集思想）。
3. **有重复元素怎么办？** —— 用 `set` 天然去重，或用 `unordered_set` 初始化时自动去重。

## 易错点

- 对每个元素都向两边扩，复杂度 O(n²)
- 用排序，违反 O(n) 要求
- 空数组没处理

## 关联项目

- 无（机考基本功）

## 来源

哈希集合应用（LeetCode 128 类题，预测题）
