---
id: Q-1831
title: 除自身以外数组的乘积：不许用除法怎么做？
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
verified_at: 2026-11-09
tags: [前缀积, 数组]
hint: 两遍遍历：从左累乘出前缀积，从右累乘出后缀积，两者相乘。结果数组可复用为后缀积。
auto: true
algo_seed: true
---

## 题目

**输入**：`nums = [1,2,3,4]`
**输出**：`[24,12,8,6]`
**要求**：不能用除法，O(n)。

**问**：不许用除法怎么做？

## 口述答案

> 答案的每一项 = 左边所有数之积 × 右边所有数之积。
> 所以做两次遍历：从左往右累乘出「前缀积」写进结果数组；
> 再从右往左累乘「后缀积」，边累乘边和结果数组相乘。
> 两次都是 O(n)，额外空间只有一个变量。

## 讲深一层

```cpp
vector<int> productExceptSelf(vector<int>& a) {
    int n = a.size();
    vector<int> res(n, 1);
    for (int i = 1; i < n; ++i) res[i] = res[i-1] * a[i-1];   // 前缀积
    int suf = 1;
    for (int i = n - 1; i >= 0; --i) {
        res[i] *= suf;          // 左 × 右
        suf *= a[i];
    }
    return res;
}
```

用结果数组存前缀积，省掉一个数组。

## 高频追问

1. **为什么不能用除法？** —— 有 0 时除法失效；题目也是这么限制的。
2. **有 0 怎么办？** —— 上面的做法天然正确，不依赖除法。
3. **溢出怎么办？** —— 乘积大时用 `long long` 或按题目要求取模。

## 易错点

- ❌ 用了除法 —— 有 0 直接崩
- ❌ 两次遍历的下标边界写错（前缀积从 i=1 开始）
- ✅ 说清「左积 × 右积」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
