---
id: Q-1842
title: 最长回文子串：中心扩展为什么比 DP 好写？
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
tags: [字符串, 中心扩展]
auto: true
algo_seed: true
---

## 题目

**题目**：求字符串中最长的回文子串。

```
输入："babad"   输出："bab"（"aba" 也算对）
输入："cbbd"    输出："bb"
```

**问**：中心扩展为什么比 DP 更好写？它的复杂度和边界处理难点在哪？

## 口述答案

> 因为回文的定义就是"从中心向两边对称"，中心扩展直接照着定义写：枚举每个中心，向两边扩到不相等为止。代码只有十行，不需要推状态转移。
> DP 要定义 `dp[i][j]` 表示 `s[i..j]` 是否回文，转移是 `dp[i][j] = (s[i]==s[j]) && dp[i+1][j-1]`，还要处理长度为 1 和 2 的边界，写起来啰嗦。两者都是 O(n²)，空间上扩展是 O(1)，DP 是 O(n²)。

## 讲深一层

```cpp
string longestPalindrome(string s) {
    if (s.empty()) return "";
    int start = 0, maxLen = 1;
    auto expand = [&](int l, int r) {
        while (l >= 0 && r < (int)s.size() && s[l] == s[r]) { --l; ++r; }
        int len = r - l - 1;                 // 注意：不相等之后才停
        if (len > maxLen) { maxLen = len; start = l + 1; }
    };
    for (int i = 0; i < (int)s.size(); ++i) {
        expand(i, i);        // 奇数长度，中心是一个字符
        expand(i, i + 1);    // 偶数长度，中心是两个字符之间
    }
    return s.substr(start, maxLen);
}
```

**两个必须讲清的点**：

1. **要枚举 2n-1 个中心**：n 个字符中心加 n-1 个间隙中心，漏掉偶数长度会错（如 `"cbbd"`）。
2. **长度是 `r - l - 1`**：循环退出时 `l` 和 `r` 已经越过边界一位，直接用 `r-l+1` 会多算 2。

**为什么不用马拉车**：Manacher 是 O(n)，但实现复杂度高、易错，机考里 O(n²) 对 n=1000 完全够用。

## 高频追问

1. **DP 版怎么写？** —— 按长度从小到大枚举，`dp[i][j]` 只依赖 `dp[i+1][j-1]`，所以循环顺序必须是长度递增。
2. **怎么判断一个串是不是回文？** —— 双指针相向，或 `s == string(s.rbegin(), s.rend())`。
3. **回文子串的个数怎么求？** —— 同样中心扩展，每个中心贡献 `(len+1)/2` 个。

## 易错点

- 只枚举奇数中心，偶数长度回文全漏
- 长度算成 `r-l+1`，多算两位
- 空串没处理，`substr` 抛异常

## 关联项目

- 无（机考基本功）

## 来源

字符串经典题（LeetCode 5 类题，预测题）
