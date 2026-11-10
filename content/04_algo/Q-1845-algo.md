---
id: Q-1845
title: 字母异位词分组：为什么排序后的字符串能当 key？
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
tags: [哈希, 字符串]
auto: true
algo_seed: true
---

## 题目

**题目**：把字母异位词分到同一组。字母异位词指字母种类和数量相同、顺序不同。

```
输入：["eat","tea","tan","ate","nat","bat"]
输出：[["bat"],["nat","tan"],["ate","eat","tea"]]
```

**问**：为什么"排序后的字符串"能当 key？还有更快的做法吗？

## 口述答案

> 因为异位词排序后**必然完全相同**——排序消除了顺序差异，只留下字母的多重集合。这是"把等价类映射到同一个代表元"的标准技巧。
> 更快的做法是用**计数向量当 key**：26 个字母的出现次数拼成一个 26 长度的字符串（或直接用 `array<int,26>` 做哈希），复杂度从 O(k log k) 降到 O(k)。

## 讲深一层

```cpp
vector<vector<string>> groupAnagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> mp;
    for (auto &s : strs) {
        string key(26, '0');
        for (char c : s) ++key[c - 'a'];     // 计数当 key
        mp[key].push_back(s);
    }
    vector<vector<string>> res;
    for (auto &[k, v] : mp) res.push_back(v);
    return res;
}
```

| 方案 | 单串复杂度 | 优点 | 缺点 |
|---|---|---|---|
| 排序当 key | O(k log k) | 代码最短 | 长串时慢 |
| 计数当 key | O(k) | 线性 | key 较长（26 字节） |
| 质数乘积当 key | O(k) | key 短 | 长串会溢出 |

**一个容易忽略的点**：`key(26, '0')` 里必须初始化为字符 `'0'` 而不是 `0`，否则 `++key[i]` 会得到不可见字符，虽然仍能当 key，但调试时看不见。

## 高频追问

1. **质数乘积法为什么不可靠？** —— 乘积增长极快，长串必然溢出 `long long`，碰撞后就分组错误。
2. **输出顺序有要求吗？** —— 一般没有，但如果要求稳定顺序，要用 `map` 而不是 `unordered_map`。
3. **字符串含 Unicode 怎么办？** —— 计数数组要换成 `map<char32_t,int>` 或用 UTF-8 解码后再统计。

## 易错点

- key 用 `0` 初始化，得到不可见字符，调试困难
- 用质数乘积，长串溢出
- 忘记处理空串（空串自成一组）

## 关联项目

- 无（机考基本功）

## 来源

哈希分组（LeetCode 49 类题，预测题）
