---
id: Q-1829
title: 合并区间：按什么排序，为什么是左端点？
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
tags: [排序, 区间]
hint: 按左端点排序后重叠区间一定相邻。只需比较当前区间左端与已合并区间的右端。
auto: true
algo_seed: true
---

## 题目

**输入**：`intervals = [[1,3],[2,6],[8,10],[15,18]]`
**输出**：`[[1,6],[8,10],[15,18]]`

**问**：按什么排序，为什么是左端点？

## 口述答案

> 按**左端点升序**排序。排完之后，能合并的区间一定相邻——
> 因为如果 A 的左端 ≤ B 的左端，且 A 的右端 ≥ B 的左端，它们就重叠。
> 排序后只需线性扫一遍：当前区间的右端和下一个区间的左端比，重叠就合并右端，不重叠就收一个答案。

## 讲深一层

```cpp
vector<vector<int>> merge(vector<vector<int>>& in) {
    sort(in.begin(), in.end());                 // 默认按 first 再 second
    vector<vector<int>> res;
    for (auto& x : in) {
        if (!res.empty() && x[0] <= res.back()[1])
            res.back()[1] = max(res.back()[1], x[1]);   // 注意取 max
        else
            res.push_back(x);
    }
    return res;
}
```

`max` 那步容易漏：`[1,10]` 和 `[2,3]` 合并，右端应保持 10，不是 3。

## 高频追问

1. **按右端点排序行不行？** —— 合并区间不行；但「最多不重叠区间数」那类问题要按右端点。
2. **区间是开区间怎么办？** —— 条件从 `<=` 改成 `<`。
3. **要插入一个新区间呢？** —— 先找到位置，再按同样逻辑合并。

## 易错点

- ❌ 合并时忘了取 `max`
- ❌ 用 `x[0] < res.back()[1]` —— 端点相接（如 `[1,2]` 和 `[2,3]`）应算重叠
- ✅ 记住「按左端排序 + 取 max」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
