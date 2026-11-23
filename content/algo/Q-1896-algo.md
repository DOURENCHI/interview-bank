---
id: Q-1896
title: 乘积最大子数组：为什么要同时维护最大和最小？
module: algo
sub: DP
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DP, 数组]
hint: 负数会让最小值翻成最大值，所以两个都要留；遇到负数时先交换再更新。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [2,3,-2,4]`
**输出**：`6`（`[2,3]`）

**问**：为什么要同时维护最大和最小？

## 口述答案

> 因为**负数会让最小值翻成最大值**。
> 比如当前最小值是 -8，乘以下一个 -1 就变成 +8，可能是全局最大。
> 所以同时记 `maxEnd` 和 `minEnd`，遇到负数时先交换两者再更新。

## 讲深一层

```cpp
int maxProduct(vector<int>& a) {
    int mx = a[0], mn = a[0], best = a[0];
    for (int i = 1; i < (int)a.size(); ++i) {
        if (a[i] < 0) swap(mx, mn);        // 负数翻转
        mx = max(a[i], mx * a[i]);
        mn = min(a[i], mn * a[i]);
        best = max(best, mx);
    }
    return best;
}
```

不交换也可以，写成三者取 max/min：

```cpp
int t1 = mx * a[i], t2 = mn * a[i];
mx = max({a[i], t1, t2});
mn = min({a[i], t1, t2});
```

## 高频追问

1. **和最大子数组和的区别？** —— 加法有单调性（负前缀丢弃），乘法没有（负负得正）。
2. **有 0 怎么办？** —— 乘 0 后归零，上面的转移自然处理。
3. **能滚动吗？** —— 已经是 O(1)。

## 易错点

- ❌ 只维护最大值 —— 遇到负数就错
- ❌ 先更新 mx 再算 mn，用到了新值
- ✅ 说清「负数翻转」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
