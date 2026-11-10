---
id: Q-1840
title: 反转字符串中的单词：怎么处理多余空格？
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
tags: [字符串, 双指针]
auto: true
algo_seed: true
---

## 题目

**题目**：给定一个字符串，反转其中单词的顺序，单词之间用单个空格连接，首尾不能有空格。

```
输入：s = "  hello world  "
输出："world hello"

输入：s = "a good   example"
输出："example good a"
```

**问**：多余的空格怎么处理？为什么不能直接 `reverse` 整个字符串了事？

## 口述答案

> 因为 `reverse` 会把单词内部的字符也翻转，得到 `"dlrow olleh"`，还得再逐个单词翻回来——能做，但要额外一轮处理。
> 更直接的做法是**先切成单词，再倒序拼接**。切的时候要注意连续多个空格会产生空串，拼的时候手动控制空格，只有前面已经拼过东西才加空格。

## 讲深一层

```cpp
string reverseWords(string s) {
    vector<string> words;
    istringstream iss(s);
    string w;
    while (iss >> w) words.push_back(w);   // >> 自动跳过任意空白
    string res;
    for (int i = words.size() - 1; i >= 0; --i) {
        if (!res.empty()) res += ' ';
        res += words[i];
    }
    return res;
}
```
时间 O(n)，空间 O(n)。

**原地版（O(1) 额外空间）**：整体翻转 → 再逐个单词翻转。这也是面试官常追问的"能不能不用额外空间"。

```cpp
// 整体反转后逐词反转，最后压缩多余空格
reverse(s.begin(), s.end());
int i = 0, n = s.size();
while (i < n) {
    int j = i;
    while (j < n && s[j] != ' ') ++j;
    reverse(s.begin() + i, s.begin() + j);
    i = j + 1;
}
```

## 高频追问

1. **`istringstream >>` 为什么能自动跳空格？** —— `operator>>` 对 `string` 的定义是先跳过前导空白再读到下一个空白，天然做了 trim。
2. **原地版怎么处理连续空格？** —— 需要一次额外的"压缩空格"扫描，把结果写到慢指针处。
3. **Python 怎么做？** —— `' '.join(s.split()[::-1])`，`split()` 无参时按任意空白切分并丢弃空串。

## 易错点

- 用 `split(' ')` 而不是 `split()`，连续空格会产生空串
- 拼接时最后多一个空格
- 空串输入没处理，返回 `" "`

## 关联项目

- 无（机考基本功）

## 来源

字符串处理题（LeetCode 151 类题，预测题）
