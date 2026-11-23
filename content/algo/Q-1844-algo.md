---
id: Q-1844
title: 实现 strStr()：KMP 的 next 数组到底在算什么？
module: algo
sub: 数组哈希
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-10
tags: [字符串, KMP]
auto: true
algo_seed: true
---

## 题目

**题目**：实现 `strStr(haystack, needle)`，返回 needle 在 haystack 中第一次出现的下标，不存在返回 -1。

```
输入：haystack = "sadbutsad", needle = "sad"   输出：0
输入：haystack = "leetcode",  needle = "leeto" 输出：-1
```

**问**：KMP 的 `next` 数组到底在算什么？为什么它能把复杂度从 O(nm) 降到 O(n+m)？

## 口述答案

> `next[i]` 算的是**子串 `p[0..i]` 的最长相等前后缀长度**。它的作用是：匹配失败时告诉你"模式串该退到哪一位继续比"，而不是从头再来。
> 暴力法每次失配都让主串指针回退，做了大量重复比较；KMP 利用"已经匹配过的部分是已知的"这一点，只退模式串指针，主串指针永回退，所以是线性的。

## 讲深一层

```cpp
vector<int> buildNext(const string &p) {
    int m = p.size();
    vector<int> nxt(m, 0);
    for (int i = 1, k = 0; i < m; ++i) {
        while (k > 0 && p[i] != p[k]) k = nxt[k - 1];   // 失配，退到上一个可行位置
        if (p[i] == p[k]) ++k;
        nxt[i] = k;
    }
    return nxt;
}

int strStr(string hay, string needle) {
    if (needle.empty()) return 0;
    auto nxt = buildNext(needle);
    for (int i = 0, k = 0; i < (int)hay.size(); ++i) {
        while (k > 0 && hay[i] != needle[k]) k = nxt[k - 1];
        if (hay[i] == needle[k]) ++k;
        if (k == (int)needle.size()) return i - k + 1;
    }
    return -1;
}
```

举例 `p = "ababaca"`：

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| p[i] | a | b | a | b | a | c | a |
| next[i] | 0 | 0 | 1 | 2 | 3 | 0 | 1 |

`next[4] = 3` 表示 `"ababa"` 的最长相等前后缀是 `"aba"`，长度 3。失配时直接退到下标 3 继续比，跳过前 3 个字符的重复比较。

**复杂度为什么是线性的**：`k` 每次最多加 1，而 `while` 里每次至少减 1，所以 `k` 的总减少量不超过总增加量，均摊 O(1)。

## 高频追问

1. **机考里该手写 KMP 吗？** —— 不必。`haystack.find(needle)` 通常就是优化过的实现，除非题目要求"不许用库函数"。
2. **`next` 数组和 `nextval` 有什么区别？** —— `nextval` 在 `p[i] == p[next[i]]` 时继续往前退，减少无意义的比较。
3. **还有别的线性算法吗？** —— Rabin-Karp（滚动哈希，平均 O(n+m)）、BM（实际最快，但实现复杂）。

## 易错点

- `next` 数组从 0 开始还是从 -1 开始搞混
- 失配时把主串指针也回退（退化成暴力）
- needle 为空时没处理

## 关联项目

- 无（机考基本功）

## 来源

字符串匹配（LeetCode 28 类题，预测题）
