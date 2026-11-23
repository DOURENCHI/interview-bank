---
id: Q-1861
title: 移动零：快慢指针原地怎么做？
module: algo
sub: 双指针滑窗
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [双指针, 数组]
hint: 慢指针指向下一个非零该放的位置，快指针扫；遇到非零就交换。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [0,1,0,3,12]`
**输出**：`[1,3,12,0,0]`
**要求**：原地，保持非零元素相对顺序。

**问**：快慢指针原地怎么做？

## 口述答案

> 慢指针 `slow` 指向「下一个非零元素该放的位置」，快指针扫全数组。
> 遇到非零就和 `slow` 位置交换，然后 `slow++`。
> 这样非零元素被依次挤到前面，零自然被换到后面，且相对顺序不变。

## 讲深一层

```cpp
void moveZeroes(vector<int>& a) {
    int slow = 0;
    for (int fast = 0; fast < (int)a.size(); ++fast)
        if (a[fast] != 0) swap(a[slow++], a[fast]);
}
```

不用额外数组，也不需要「先统计零的个数再补零」。

## 高频追问

1. **交换会不会打乱顺序？** —— 不会，`slow` 之前的都已是稳定排列。
2. **不交换、直接覆盖行吗？** —— 行，但要记非零个数，最后补零。
3. **要保持零的顺序吗？** —— 题目通常不要求；要的话这个写法也满足。

## 易错点

- ❌ 用额外数组 —— 不满足原地
- ❌ `slow++` 位置写错
- ✅ 说清「slow 是写指针」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
