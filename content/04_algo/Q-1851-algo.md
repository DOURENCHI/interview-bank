---
id: Q-1851
title: 两个数组的交集：哈希和排序双指针怎么选？
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
verified_at: 2026-11-10
tags: [哈希, 双指针]
auto: true
algo_seed: true
---

## 题目

**题目**：求两个数组的交集（每个元素只出现一次，顺序不限）。

```
输入：nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出：[9,4]（顺序不限）
```

**问**：哈希法和排序双指针法怎么选？如果 nums2 是"流式"的、且远大于 nums1，又该怎么改？

## 口述答案

> **看数据规模和数据是否有序**。哈希法 O(n+m) 但要额外空间；排序双指针 O(n log n + m log m)，空间 O(1)（不计排序）。数据已经有序时双指针明显更优。
> 如果 nums2 是流式且远大于 nums1，应该**把 nums1 放进哈希集合**，然后流式扫 nums2 逐个查——这样只存小集合，内存占用小。

## 讲深一层

```cpp
// 哈希法
vector<int> intersection(vector<int>& a, vector<int>& b) {
    unordered_set<int> s(a.begin(), a.end());
    vector<int> res;
    for (int x : b) if (s.erase(x)) res.push_back(x);   // erase 返回删除个数
    return res;
}

// 排序 + 双指针（空间 O(1)）
vector<int> intersection2(vector<int>& a, vector<int>& b) {
    sort(a.begin(), a.end()); sort(b.begin(), b.end());
    vector<int> res;
    int i = 0, j = 0;
    while (i < (int)a.size() && j < (int)b.size()) {
        if (a[i] < b[j]) ++i;
        else if (a[i] > b[j]) ++j;
        else { res.push_back(a[i]); while (i < (int)a.size() && a[i] == res.back()) ++i;
                                     while (j < (int)b.size() && b[j] == res.back()) ++j; }
    }
    return res;
}
```

`erase(x)` 返回删除的元素个数，用它判断"是否存在于 s 中"，同时保证结果不重复——比 `count` + `erase` 两步更简洁。

## 高频追问

1. **如果要求保留重复（交集 II）？** —— 用 `unordered_map<int,int>` 计数，或者双指针时每次都前进而不是跳过重复。
2. **数据有序但要求 O(1) 空间？** —— 双指针，正是它的强项。
3. **超大数组放不进内存？** —— 用 Bloom filter 预筛，或外部排序后归并。

## 易错点

- 哈希法不删元素，结果出现重复
- 双指针跳重复时越界
- 用 `vector` 做集合，查找退化成 O(n)

## 关联项目

- 无（机考基本功）

## 来源

哈希与双指针（LeetCode 349 类题，预测题）
