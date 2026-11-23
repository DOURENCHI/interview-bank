---
id: Q-1860
title: 滑动窗口最大值：单调队列为什么能做到 O(n)？
module: algo
sub: 双指针滑窗
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [单调队列, 滑窗]
hint: 队列存下标且值递减，队头就是最大值。每个元素最多进出一次，均摊 O(1)。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [1,3,-1,-3,5,3,6,7], k = 3`
**输出**：`[3,3,5,5,6,7]`

**问**：单调队列为什么能做到 O(n)？

## 口述答案

> 维护一个**下标**队列，队列里的值从队头到队尾单调递减。
> 新元素进来时，把队尾所有比它小的都弹掉（它们不可能再成为最大值），再入队；
> 同时把「已经滑出窗口」的队头弹掉。这样队头永远是当前窗口最大值。
> 每个元素最多进队一次、出队一次，所以总复杂度 O(n)。

## 讲深一层

```cpp
vector<int> maxSlidingWindow(vector<int>& a, int k) {
    deque<int> dq;                 // 存下标
    vector<int> res;
    for (int i = 0; i < (int)a.size(); ++i) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();   // 过期
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();   // 更小的没用了
        dq.push_back(i);
        if (i >= k - 1) res.push_back(a[dq.front()]);
    }
    return res;
}
```

| 方法 | 时间 | 说明 |
|---|---|---|
| 暴力 | O(nk) | 每个窗口扫一遍 |
| 大顶堆 | O(n log n) | 要处理过期 |
| **单调队列** | **O(n)** | 最优 |

## 高频追问

1. **为什么存下标不存值？** —— 要判断是否滑出窗口。
2. **`<=` 还是 `<`？** —— 用 `<=` 弹掉相等值，队列更短，结果不变。
3. **求窗口最小值？** —— 改成单调递增队列。

## 易错点

- ❌ 存值不存下标 —— 无法判断过期
- ❌ 先弹过期再弹小值，顺序反了会残留
- ✅ 说清「每元素进出各一次」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
