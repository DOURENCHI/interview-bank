---
id: Q-1858
title: 找到字符串中所有字母异位词：固定窗口怎么滑？
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
tags: [滑窗, 计数]
hint: 窗口长度固定为 p 的长度，每次右进一个左出一个，比较计数数组是否相同。
auto: true
algo_seed: true
---

## 题目

**输入**：`s = "cbaebabacd", p = "abc"`
**输出**：`[0,6]`（`"cba"` 和 `"bac"`）

**问**：固定窗口怎么滑动？

## 口述答案

> 窗口长度固定为 p 的长度。先把窗口填满，比较一次计数数组；
> 之后每次右进一个字符、左出一个字符，再比较。
> 用长度 26 的数组而不是排序——比较两个 26 元数组是 O(26)，常数极小。
> 更进一步可以用一个 `diff` 变量记录「有多少个字符的计数不同」，把比较降到 O(1)。

## 讲深一层

```cpp
vector<int> findAnagrams(string s, string p) {
    vector<int> res;
    int n = s.size(), m = p.size();
    if (n < m) return res;
    vector<int> need(26,0), win(26,0);
    for (char c : p) ++need[c-'a'];
    for (int i = 0; i < m; ++i) ++win[s[i]-'a'];
    if (win == need) res.push_back(0);
    for (int i = m; i < n; ++i) {
        ++win[s[i]-'a'];
        --win[s[i-m]-'a'];
        if (win == need) res.push_back(i - m + 1);
    }
    return res;
}
```

## 高频追问

1. **为什么不用排序比较？** —— 每次排序 O(m log m)，滑动时白白浪费。
2. **`diff` 优化怎么做？** —— 维护计数不同的字符个数，为 0 即匹配。
3. **大小写混合？** —— 数组扩到 128 或 256。

## 易错点

- ❌ 窗口边界算错（起点是 `i-m+1`）
- ❌ 忘了判断 `n < m`
- ✅ 说清「固定窗口 + 计数数组」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
