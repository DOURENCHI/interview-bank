---
id: Q-1868
title: 有序数组的平方：为什么从两端取最大？
module: 04_algo
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
tags: [双指针, 数组]
hint: 负数平方后可能最大，最大值必在两端。双指针从两端取大者倒序填入。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [-4,-1,0,3,10]`（非递减）
**输出**：`[0,1,9,16,100]`

**问**：为什么从两端取最大？

## 口述答案

> 因为负数平方后可能最大——数组两端的绝对值最大，所以平方后的最大值**必在两端之一**。
> 用两个指针从两端往中间走，每次取绝对值大的那个，平方后**从后往前填**结果数组。
> 从后往前填是关键：这样不用搬移元素。

## 讲深一层

```cpp
vector<int> sortedSquares(vector<int>& a) {
    int n = a.size(), l = 0, r = n - 1, k = n - 1;
    vector<int> res(n);
    while (l <= r) {
        if (abs(a[l]) > abs(a[r])) res[k--] = a[l] * a[l++];
        else                       res[k--] = a[r] * a[r--];
    }
    return res;
}
```

## 高频追问

1. **全是正数/全是负数还成立吗？** —— 成立，退化成简单情况。
2. **能原地吗？** —— 可以，但元素会互相覆盖，不推荐。
3. **为什么不用排序？** —— 平方后排序是 O(n log n)，双指针是 O(n)。

## 易错点

- ❌ 从前往后填 —— 需要额外搬移
- ❌ 比较平方值而不是绝对值（效果相同但容易溢出）
- ✅ 记住「两端绝对值最大」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
