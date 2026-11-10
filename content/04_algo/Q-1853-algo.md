---
id: Q-1853
title: 外观数列：怎么从上一项推出下一项？
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
tags: [字符串, 模拟]
auto: true
algo_seed: true
---

## 题目

**题目**：外观数列。第 1 项是 `"1"`，之后每一项都是对前一项的"读数"：读成"几个几"。

```
1: 1
2: 11        （1 个 1）
3: 21        （2 个 1）
4: 1211      （1 个 2，1 个 1）
5: 111221    （1 个 1，1 个 2，2 个 1）
```

**问**：怎么从上一项推出下一项？边界怎么处理？

## 口述答案

> 对上一项做**游程编码**：从左往右扫，统计连续相同字符的个数，遇到变化就输出"个数 + 字符"，然后从新字符重新计数。
> 边界是最后一个游程：循环里只在"字符变化时"才输出，所以末尾那段必须在循环外补一次输出，否则最后一个游程会丢。
> ```cpp
> string countAndSay(int n) {
> string s = "1";
> for (int k = 2; k <= n; ++k) {
> string t;
> for (int i = 0; i < (int)s.size(); ) {
> int j = i;
> while (j < (int)s.size() && s[j] == s[i]) ++j;
> t += to_string(j - i) + s[i];      // 个数 + 字符
> i = j;
> }
> s = t;
> }
> return s;
> }
> ```
> 时间 O(n · L)，L 为第 n 项长度（增长约 1.3 倍/项）。空间 O(L)。
> **关键点**：数字要转成字符，`t += to_string(count)` 而不是 `t += count`（那会加 ASCII 码）。

## 讲深一层

```cpp
string countAndSay(int n) {
    string s = "1";
    for (int k = 2; k <= n; ++k) {
        string t;
        for (int i = 0; i < (int)s.size(); ) {
            int j = i;
            while (j < (int)s.size() && s[j] == s[i]) ++j;   // 找到游程右端
            t += to_string(j - i) + s[i];                    // 个数 + 字符
            i = j;
        }
        s = t;
    }
    return s;
}
```

| 项 | 长度 | 说明 |
|---|---|---|
| 1 | 1 | 1 |
| 5 | 6 | 111221 |
| 15 | 约 2.5 千 | 指数级增长 |
| 30 | 约 5.8 万 | 拼接开销开始明显 |

这题本质是**游程编码（RLE）反复迭代**。写的时候只要盯住一个不变量：**每段连续相同字符只被输出一次**，而循环里的"输出"发生在字符变化处，所以最后一段必须在循环外补。

## 高频追问

1. **为什么长度增长这么快？** —— 每项平均膨胀约 1.3 倍，n=30 时长度已到几万，n 再大就要考虑字符串拼接开销。
2. **能用递归吗？** —— 能，`countAndSay(n)` 依赖 `countAndSay(n-1)`，但迭代更省栈。
3. **怎么优化拼接？** —— 用 `reserve` 预估容量，或先算长度再写。

## 易错点

- 末尾游程漏输出
- `t += count` 加了数字的 ASCII 码
- `count` 超过 9 时忘记 `to_string` 会输出多字符

## 关联项目

- 无（机考基本功）

## 来源

模拟题（LeetCode 38 类题，预测题）
