---
id: Q-1859
title: 长度最小的子数组：滑窗和前缀和+二分怎么选？
module: algo
sub: 双指针滑窗
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [滑窗, 前缀和]
hint: 全是正数时滑窗 O(n) 最优；有负数时滑窗失效，得用前缀和+二分或单调队列。
auto: true
algo_seed: true
---

## 题目

**输入**：`target = 7, nums = [2,3,1,2,4,3]`
**输出**：`2`（`[4,3]`）
**要求**：元素全为正。

**问**：滑动窗口和前缀和+二分怎么选？

## 口述答案

> **全是正数**时用滑动窗口：窗口和单调递增，右扩左缩都不会回退，O(n)。
> **有负数**时滑窗失效——加了负数窗口和可能变小，左指针的移动依据就没了，
> 这时要用前缀和 + 二分（O(n log n)）或单调队列。
> 所以先问题目有没有「正数」这个前提。

## 讲深一层

```cpp
int minSubArrayLen(int target, vector<int>& a) {
    int l = 0, sum = 0, best = INT_MAX;
    for (int r = 0; r < (int)a.size(); ++r) {
        sum += a[r];
        while (sum >= target) {              // 满足条件就尝试缩
            best = min(best, r - l + 1);
            sum -= a[l++];
        }
    }
    return best == INT_MAX ? 0 : best;
}
```

## 高频追问

1. **有负数怎么办？** —— 前缀和 `pre[j]-pre[i] >= target`，对每个 j 二分最小的 i。
2. **为什么 while 不是 if？** —— 缩一次可能还满足，要继续缩。
3. **要返回子数组本身？** —— 记录 best 对应的区间。

## 易错点

- ❌ 有负数还用滑窗
- ❌ 用 if 只缩一次 —— 漏掉更短解
- ✅ 先确认「元素是否全正」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
