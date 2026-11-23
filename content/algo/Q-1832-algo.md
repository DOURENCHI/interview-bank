---
id: Q-1832
title: 缺失的第一个正数：为什么能把数组本身当哈希表？
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
verified_at: 2026-11-09
tags: [原地哈希, 数组]
hint: 把值 v 换到下标 v-1 上做原地置换，再扫一遍找第一个 a[i] != i+1。O(n) 时间 O(1) 空间。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [3,4,-1,1]`
**输出**：`2`
**要求**：O(n) 时间，O(1) 额外空间。

**问**：为什么能把数组本身当哈希表？

## 口述答案

> 因为答案是 1..n+1 之间的数。所以可以让「值 v」待在「下标 v-1」上——
> 把每个 1..n 范围内的数换到它该在的位置，最后从前往后扫，
> 第一个 `nums[i] != i+1` 的位置，答案就是 `i+1`。
> 数组本身就成了哈希表，不需要额外空间。

## 讲深一层

```cpp
int firstMissingPositive(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n; ++i) {
        // 反复换，直到当前位置正确或换不了
        while (a[i] > 0 && a[i] <= n && a[a[i]-1] != a[i])
            swap(a[i], a[a[i]-1]);
    }
    for (int i = 0; i < n; ++i)
        if (a[i] != i + 1) return i + 1;
    return n + 1;
}
```

`while` 而不是 `if`：换过来的新值还需要继续归位，但每个数最多换一次，总复杂度仍 O(n)。

## 高频追问

1. **为什么用 while 不会超时？** —— 每次 swap 至少让一个数归位，总共最多 n 次。
2. **`a[a[i]-1] != a[i]` 这个条件防什么？** —— 防重复值造成死循环。
3. **不用原地哈希行不行？** —— 用 set 是 O(n) 空间，不满足要求。

## 易错点

- ❌ 用 `if` 而不是 `while` —— 换一次就不管了
- ❌ 忘了重复值判断 —— 死循环
- ✅ 说清「值 v 放下标 v-1」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
