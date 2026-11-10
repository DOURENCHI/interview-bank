---
id: Q-1856
title: 无重复字符的最长子串：左边界为什么要取 max？
module: 04_algo
sub: 双指针滑窗
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [滑窗, 哈希]
hint: left = max(left, last[c]+1)。不取 max 的话，遇到更早出现过的字符会把窗口往回拉。
auto: true
algo_seed: true
---

## 题目

**输入**：`s = "abcabcbb"`
**输出**：`3`（`"abc"`）

**问**：窗口左边界为什么要取 max？

## 口述答案

> 用哈希记录每个字符**最后出现的下标**。右指针一路往前扩，
> 遇到重复字符时，左边界应该跳到「这个字符上次出现的下标 + 1」。
> 但必须写 `left = max(left, last[c] + 1)`——因为上次出现的下标可能**比当前 left 还小**，
> 那是更早的过期记录，直接赋值会把窗口往回拉，导致重复计算。

## 讲深一层

```cpp
int lengthOfLongestSubstring(string s) {
    vector<int> last(128, -1);
    int left = 0, best = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
        if (last[s[r]] >= left)          // 上次出现在当前窗口内
            left = last[s[r]] + 1;
        last[s[r]] = r;
        best = max(best, r - left + 1);
    }
    return best;
}
```

`last[c] >= left` 这个判断等价于取 max，写法更直观。

## 高频追问

1. **为什么要 `>= left` 而不是无条件跳？** —— 无条件跳会被过期记录拉回左边。
2. **能处理 Unicode 吗？** —— 上面假设 ASCII；Unicode 要用 `unordered_map<char32_t,int>`。
3. **要求返回子串本身？** —— 记录 best 对应的 `left/right`。

## 易错点

- ❌ 直接 `left = last[c] + 1` —— 窗口回退
- ❌ 忘了更新 `last[c]`
- ✅ 记住「左边界只能往前走」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
