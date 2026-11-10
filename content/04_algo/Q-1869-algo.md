---
id: Q-1869
title: 验证回文串：怎么跳过非字母数字字符？
module: 04_algo
sub: 双指针滑窗
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [双指针, 字符串]
hint: 双指针向中间靠，遇到非字母数字就跳过，比较时统一大小写。
auto: true
algo_seed: true
---

## 题目

**输入**：`s = "A man, a plan, a canal: Panama"`
**输出**：`true`（忽略大小写和非字母数字）

**问**：怎么跳过非字母数字字符？

## 口述答案

> 双指针从两端往中间走，遇到非字母数字就跳过，比较时统一转小写。
> 关键是**两个指针都要跳过**，且跳过之后要重新检查边界，别越界。

## 讲深一层

```cpp
bool isPalindrome(string s) {
    int i = 0, j = s.size() - 1;
    while (i < j) {
        while (i < j && !isalnum(s[i])) ++i;
        while (i < j && !isalnum(s[j])) --j;
        if (tolower(s[i]) != tolower(s[j])) return false;
        ++i; --j;
    }
    return true;
}
```

`isalnum` 对负 char 是未定义行为，严格要 `isalnum((unsigned char)c)`。

## 高频追问

1. **中文怎么办？** —— `isalnum` 只处理 ASCII，Unicode 要自己判。
2. **能先把过滤后的串提出来吗？** —— 能，但 O(n) 额外空间。
3. **只考虑字母数字的另一种理解？** —— 有些题只要求字母，看清题面。

## 易错点

- ❌ 内层 while 不带 `i < j` —— 越界
- ❌ 用 `char` 直接传 `isalnum` —— 负数未定义
- ✅ 记住「双指针 + 跳过 + 统一大小写」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
