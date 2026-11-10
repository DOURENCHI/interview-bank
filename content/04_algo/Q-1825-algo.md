---
id: Q-1825
title: 两数之和：为什么一遍哈希就够了，不用双重循环？
module: 04_algo
sub: 数组哈希
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [哈希, 数组]
hint: 边遍历边存「还差多少→下标」，当前值一命中就返回。O(n) 时间换 O(n) 空间，比 O(n²) 稳。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [2,7,11,15], target = 9`
**输出**：`[0,1]`（2 + 7 = 9）
**约定**：每个输入只有一个答案，同一元素不能用两次。

**问**：为什么一遍哈希就够，不用双重循环？

## 口述答案

> 双重循环是 O(n²)。换个角度：遍历到 nums[i] 时，我其实在找「target - nums[i] 之前出现过没有」。
> 所以边遍历边把「值 → 下标」存进哈希表，查一次 O(1)，整体 O(n)。
> 关键是**存的是「已经见过的」**，不是整个数组——否则会把自己和自己配对。

## 讲深一层

```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int,int> seen;          // 值 -> 下标
    for (int i = 0; i < (int)nums.size(); ++i) {
        int need = target - nums[i];
        auto it = seen.find(need);
        if (it != seen.end()) return {it->second, i};
        seen[nums[i]] = i;                // 先查后存，避免自配
    }
    return {};
}
```

| 方案 | 时间 | 空间 |
|---|---|---|
| 双重循环 | O(n²) | O(1) |
| 排序 + 双指针 | O(n log n) | O(n)（要存下标） |
| **哈希一次遍历** | **O(n)** | O(n) |

## 高频追问

1. **「先查后存」为什么重要？** —— `target = 4, nums = [2]` 时，先存会让 2 和自己配对。
2. **有重复值怎么办？** —— 哈希存第一个出现的下标即可，题目保证唯一解。
3. **要返回所有解呢？** —— 改成排序 + 双指针，并去重（见三数之和）。

## 易错点

- ❌ 先存后查 —— 自配
- ❌ 用 `map` 而不是 `unordered_map` —— 多了 log n
- ✅ 说清「存已见过的，查还差多少」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
