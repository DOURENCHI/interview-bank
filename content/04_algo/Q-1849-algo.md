---
id: Q-1849
title: 有效的字母异位词：为什么计数数组比排序快？
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
verified_at: 2026-11-10
tags: [哈希, 字符串]
auto: true
algo_seed: true
---

## 题目

**题目**：判断两个字符串是否互为字母异位词。

```
输入：s = "anagram", t = "nagaram"   输出：true
输入：s = "rat",     t = "car"       输出：false
```

**问**：计数数组为什么比排序快？如果字符集是全部 Unicode，这招还成立吗？

## 口述答案

> 排序要 O(n log n)，计数只要 O(n)——它把"比较两个多重集合"变成了"逐个累加再检查是否归零"。
> 具体做法：遍历 `s` 时加一，遍历 `t` 时减一，最后所有计数为 0 就是异位词。连"长度是否相等"都能顺带检查。
> **Unicode 就不成立了**：字符种类可能上万，开数组不现实，要换 `unordered_map`，此时计数法的优势会缩小。

## 讲深一层

```cpp
bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;
    int cnt[26] = {0};
    for (int i = 0; i < (int)s.size(); ++i) { ++cnt[s[i] - 'a']; --cnt[t[i] - 'a']; }
    for (int v : cnt) if (v) return false;
    return true;
}
```

| 方案 | 时间 | 空间 | 备注 |
|---|---|---|---|
| 排序后比较 | O(n log n) | O(1)~O(n) | 代码最短 |
| 计数数组 | O(n) | O(1) | 字符集固定时最优 |
| 哈希表计数 | O(n) 平均 | O(k) | 字符集大时用 |

**一个容易漏的优化**：长度不等直接返回 false，能挡掉大量用例；否则后面还要跑完整统计。

**进阶追问**：如果输入是"字符流"、字符源源不断到来，排序完全不可用，必须用计数。

## 高频追问

1. **能不能只用一次遍历？** —— 上面的写法就是一次遍历（同时处理两个串），但要求长度相等，否则越界。
2. **含 Unicode 怎么写？** —— `unordered_map<char32_t,int>`，或用 UTF-8 解码后统计码点。
3. **和"字母异位词分组"什么关系？** —— 分组是这题的推广：把互为异位词的串归到同一类。

## 易错点

- 不先比较长度，越界或误判
- 数组开到 26 但输入含大写/数字
- 只统计 s 不比较 t 的计数

## 关联项目

- 无（机考基本功）

## 来源

计数数组应用（LeetCode 242 类题，预测题）
