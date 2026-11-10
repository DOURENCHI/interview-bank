---
id: Q-1838
title: 最长公共前缀：怎么优雅地逐列比较？
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
tags: [字符串]
hint: 以第一个字符串为基准逐位比对所有串，某串越界或不匹配就截断。不要两两求前缀。
auto: true
algo_seed: true
---

## 题目

**输入**：`strs = ["flower","flow","flight"]`
**输出**：`"fl"`

**问**：怎么优雅地逐列比较？

## 口述答案

> 以第一个字符串为基准，逐位比较所有字符串的同一位置。
> 一旦某个字符串在这一位越界、或者字符不匹配，当前位置之前的就是答案。
> 不要两两求前缀——那样每次都要重新扫，而且中间结果没意义。

## 讲深一层

```cpp
string longestCommonPrefix(vector<string>& s) {
    if (s.empty()) return "";
    for (int i = 0; i < (int)s[0].size(); ++i) {
        char c = s[0][i];
        for (int j = 1; j < (int)s.size(); ++j) {
            if (i >= (int)s[j].size() || s[j][i] != c)
                return s[0].substr(0, i);
        }
    }
    return s[0];
}
```

时间 O(总字符数)，最坏 O(n·m)。

## 高频追问

1. **字符串数量很多怎么办？** —— 可以两两分治合并前缀，减少重复扫描。
2. **空数组/含空串？** —— 提前返回。
3. **能用排序吗？** —— 能：排序后只比较第一个和最后一个（最短公共前缀必是两者的公共前缀）。

## 易错点

- ❌ 忘了检查越界（短字符串先耗尽）
- ❌ 两两求前缀，逻辑绕
- ✅ 记住「排序后比首尾」这个技巧


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
