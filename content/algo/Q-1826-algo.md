---
id: Q-1826
title: 三数之和：怎么保证结果不重复？
module: algo
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
tags: [哈希, 双指针, 去重]
hint: 先排序，固定一个数后用双指针夹逼；跳过与上一个相同的固定值和指针值，否则出重复三元组。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [-1,0,1,2,-1,-4]`
**输出**：`[[-1,-1,2],[-1,0,1]]`
**要求**：三元组不能重复。

**问**：怎么保证不重复？

## 口述答案

> 先排序，然后固定第一个数，剩下两个用双指针从两端夹逼。
> 去重靠三处：固定值跳过和上一个相同的、左指针跳过相同值、右指针跳过相同值。
> 排序是关键——它让「相同的数挨在一起」，去重才有依据；也让双指针的单调性成立。

## 讲深一层

```cpp
vector<vector<int>> threeSum(vector<int>& a) {
    sort(a.begin(), a.end());
    vector<vector<int>> res;
    int n = a.size();
    for (int i = 0; i < n - 2; ++i) {
        if (i && a[i] == a[i-1]) continue;        // 固定值去重
        int l = i + 1, r = n - 1;
        while (l < r) {
            int s = a[i] + a[l] + a[r];
            if (s < 0) ++l;
            else if (s > 0) --r;
            else {
                res.push_back({a[i], a[l], a[r]});
                while (l < r && a[l] == a[l+1]) ++l;   // 左去重
                while (l < r && a[r] == a[r-1]) --r;   // 右去重
                ++l; --r;
            }
        }
    }
    return res;
}
```

复杂度 O(n²)：外层 n，内层双指针 O(n)。

## 高频追问

1. **为什么先排序不破坏正确性？** —— 要求返回数值组合，不是下标。
2. **剪枝能做吗？** —— 能：`a[i] > 0` 直接 break（后面都更大）。
3. **四数之和呢？** —— 再套一层循环，同样去重。

## 易错点

- ❌ 只在最后用 set 去重 —— 慢且占内存
- ❌ 三处去重漏一处 —— 出现重复三元组
- ✅ 记住「排序 + 固定一个 + 双指针 + 三处去重」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
