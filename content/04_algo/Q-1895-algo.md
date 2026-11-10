---
id: Q-1895
title: 单词拆分：为什么用 DP 而不是 DFS 暴搜？
module: 04_algo
sub: DP
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [DP, 字符串]
hint: 暴搜会重复计算同一后缀。dp[i] 表示前 i 个字符能否拆分，枚举分割点。
auto: true
algo_seed: true
---

## 题目

**输入**：`s = "leetcode", wordDict = ["leet","code"]`
**输出**：`true`

**问**：为什么用 DP 而不是 DFS 暴搜？

## 口述答案

> 暴搜会**重复计算同一个后缀**——比如 "aaab" 从不同起点切，会反复判断 "ab" 能不能拆。
> DP 把「前 i 个字符能否拆分」记下来：`dp[i] = OR over j<i (dp[j] && s[j:i] in dict)`。
> 每个位置只算一次，复杂度 O(n²·L)。

## 讲深一层

```cpp
bool wordBreak(string s, vector<string>& dict) {
    unordered_set<string> st(dict.begin(), dict.end());
    int n = s.size();
    vector<bool> dp(n + 1, false);
    dp[0] = true;
    for (int i = 1; i <= n; ++i)
        for (int j = 0; j < i; ++j)
            if (dp[j] && st.count(s.substr(j, i - j))) { dp[i] = true; break; }
    return dp[n];
}
```

## 高频追问

1. **要返回所有拆法？** —— 那就得 DFS + 剪枝或记忆化。
2. **字典很大怎么优化？** —— 用 Trie 或按最大词长限制 j 的范围。
3. **字符串匹配开销？** —— `substr` 每次 O(L)，可换哈希。

## 易错点

- ❌ `dp[0]` 忘了设 true
- ❌ j 的范围写错
- ✅ 说清「dp[i] 表示前缀可拆」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
