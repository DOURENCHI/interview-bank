---
id: Q-1862
title: 删除有序数组中的重复项：为什么返回长度而不是新数组？
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
hint: 题目要求原地修改，返回值是有效长度，调用方按前 k 个读。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [1,1,2]`
**输出**：返回 `2`，且 `nums` 前两个元素为 `[1,2]`

**问**：为什么返回长度而不是新数组？

## 口述答案

> 题目要求原地修改，返回的是**有效长度 k**，调用方按前 k 个元素读取。
> 这样不用分配新数组，O(1) 空间。
> 做法是快慢指针：`slow` 指向已处理的最后一个不重复位置，
> `fast` 扫，遇到和 `nums[slow]` 不同的就写到 `slow+1`。

## 讲深一层

```cpp
int removeDuplicates(vector<int>& a) {
    if (a.empty()) return 0;
    int slow = 0;
    for (int fast = 1; fast < (int)a.size(); ++fast)
        if (a[fast] != a[slow]) a[++slow] = a[fast];
    return slow + 1;
}
```

## 高频追问

1. **允许最多重复两次呢？** —— 判断改成 `a[fast] != a[slow-1]`（前提 slow ≥ 1）。
2. **无序数组呢？** —— 这题依赖有序，无序要用哈希。
3. **返回的 k 之后的数据要不要清？** —— 不用，题目不关心。

## 易错点

- ❌ 返回 `slow` 而不是 `slow+1`
- ❌ 空数组没处理
- ✅ 说清「原地 + 返回有效长度」的约定


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
