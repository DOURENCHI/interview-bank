---
id: Q-1857
title: 最小覆盖子串：need 和 window 两个计数器怎么维护？
module: 04_algo
sub: 双指针滑窗
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [滑窗, 哈希]
hint: need 记目标频次，window 记当前窗口；用 valid 记已满足的字符种类数，等于 need 大小就尝试收缩。
auto: true
algo_seed: true
---

## 题目

**输入**：`s = "ADOBECODEBANC", t = "ABC"`
**输出**：`"BANC"`

**问**：need 和 window 两个计数器怎么维护？

## 口述答案

> 三个东西：`need` 记 t 里每个字符要多少，`window` 记当前窗口里有多少，
> 再用一个 `valid` 记「已经满足数量的字符种类数」。
> 右指针扩张时更新 window，如果某字符数量刚好等于 need，valid 加一；
> 当 `valid == need.size()` 说明窗口覆盖了 t，此时尝试收缩左边界，边收缩边记录最短。

## 讲深一层

```cpp
string minWindow(string s, string t) {
    unordered_map<char,int> need, win;
    for (char c : t) ++need[c];
    int needKinds = need.size(), valid = 0;
    int l = 0, start = 0, len = INT_MAX;

    for (int r = 0; r < (int)s.size(); ++r) {
        char c = s[r];
        if (need.count(c)) {
            ++win[c];
            if (win[c] == need[c]) ++valid;
        }
        while (valid == needKinds) {            // 已覆盖，尝试收缩
            if (r - l + 1 < len) { len = r - l + 1; start = l; }
            char d = s[l++];
            if (need.count(d)) {
                if (win[d] == need[d]) --valid;  // 先判再减
                --win[d];
            }
        }
    }
    return len == INT_MAX ? "" : s.substr(start, len);
}
```

## 高频追问

1. **为什么用 `valid` 而不是每次比较两个 map？** —— 比较是 O(k)，valid 让判断变 O(1)。
2. **收缩时为什么先判 `win[d] == need[d]`？** —— 减之前相等，说明减完就不满足了。
3. **含重复字符的 t 行吗？** —— 行，need 记的是数量。

## 易错点

- ❌ 收缩时先减再判 —— valid 少算
- ❌ 返回空串的条件写错
- ✅ 说清「valid 记的是种类数，不是字符总数」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
