---
id: Q-1843
title: 字符串转换整数 atoi：边界有哪几处坑？
module: algo
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
tags: [字符串, 边界]
auto: true
algo_seed: true
---

## 题目

**题目**：实现 `atoi`：把字符串转成 32 位整数。规则是跳过前导空格、可有正负号、遇到非数字停止、溢出要截断到 `INT_MIN` / `INT_MAX`。

```
输入："42"            输出：42
输入："   -042"       输出：-42
输入："4193 with words" 输出：4193
输入："-91283472332"  输出：-2147483648
输入："words and 987" 输出：0
```

**问**：这道题的坑点集中在哪里？为什么不能直接 `stoi`？

## 口述答案

> 坑全在边界：**溢出**、**只有符号没有数字**、**全是空格**、**非数字开头返回 0**。`stoi` 遇到溢出会抛 `out_of_range`，机考里直接崩，所以必须自己处理。
> 正确做法是用 `long long` 累加，累加过程中判断是否越界，越界就返回对应的极值。

## 讲深一层

```cpp
int myAtoi(string s) {
    int i = 0, n = s.size();
    while (i < n && s[i] == ' ') ++i;            // 1. 跳过前导空格
    int sign = 1;
    if (i < n && (s[i] == '+' || s[i] == '-')) {  // 2. 符号
        sign = (s[i] == '-') ? -1 : 1;
        ++i;
    }
    long long val = 0;
    while (i < n && isdigit(s[i])) {             // 3. 数字
        val = val * 10 + (s[i] - '0');
        if (sign == 1 && val > INT_MAX) return INT_MAX;   // 4. 提前截断
        if (sign == -1 && -val < INT_MIN) return INT_MIN;
        ++i;
    }
    return (int)(sign * val);
}
```

| 边界用例 | 期望输出 | 常见错误 |
|---|---|---|
| `""` | 0 | 越界访问 |
| `"   "` | 0 | 返回 0 但没走完逻辑 |
| `"+"` / `"-"` | 0 | 返回符号本身 |
| `"-91283472332"` | -2147483648 | 返回 INT_MAX 或溢出成正数 |
| `"00000000000000123"` | 123 | 长串溢出 |

**为什么在累加过程中就判断，而不是最后判断**：`long long` 也可能被超长数字串撑爆（虽然 19 位以内安全），提前截断最稳。

## 高频追问

1. **溢出判断为什么用 `long long` 而不是 `int`？** —— `int` 一溢出就是未定义行为，可能变成负数，判断失效。
2. **`isdigit(s[i])` 有什么风险？** —— 参数是 `char` 时若为负值（非 ASCII）是未定义行为，应转 `unsigned char`。
3. **能不能先找数字子串再转？** —— 能，但要注意子串本身也可能溢出。

## 易错点

- 用 `stoi` 直接转，溢出抛异常
- 溢出只在最后判断，中间已经溢出
- `"-"` 单独一个符号返回 -1

## 关联项目

- 无（机考基本功）

## 来源

字符串解析题（LeetCode 8 类题，预测题）
