---
id: Q-1854
title: 字符串解码：嵌套括号怎么处理？
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
tags: [栈, 字符串]
auto: true
algo_seed: true
---

## 题目

**题目**：解码字符串，规则是 `k[encoded]` 表示把括号内内容重复 k 次。可以嵌套。

```
输入："3[a]2[bc]"      输出："aaabcbc"
输入："3[a2[c]]"       输出："accaccacc"
输入："2[abc]3[cd]ef"  输出："abcabccdcdcdef"
```

**问**：嵌套括号怎么处理？为什么需要两个栈而不是一个？

## 口述答案

> 因为进入括号时**要同时保存两样东西**：当前的重复次数和括号外的已有字符串。只用一个栈存不了这两类信息，所以用两个栈（或一个栈存结构体）。
> 遇到 `[`：把当前数字压入数字栈、当前字符串压入字符串栈、两者清零；
> 遇到 `]`：弹出两者，把当前字符串重复 k 次后接回外层字符串。

## 讲深一层

```cpp
string decodeString(string s) {
    stack<int> nums;
    stack<string> strs;
    int num = 0;
    string cur;
    for (char c : s) {
        if (isdigit(c)) num = num * 10 + (c - '0');      // 多位数
        else if (c == '[') { nums.push(num); strs.push(cur); num = 0; cur.clear(); }
        else if (c == ']') {
            string tmp = cur;
            cur = strs.top(); strs.pop();
            int k = nums.top(); nums.pop();
            while (k--) cur += tmp;                       // 重复并接回外层
        } else cur += c;
    }
    return cur;
}
```

| 步骤 | 数字栈 | 字符串栈 | 当前串 |
|---|---|---|---|
| `3[` | 3 | "" | "" |
| `a2[c` | 3, 2 | "", "a" | "c" |
| `]` | 3 | "" | "acc" |
| `]` | — | — | "accaccacc" |

**为什么 `num = num*10 + digit`**：数字可能多位（`"12[ab]"`），逐位累加才正确。

替代写法：递归（遇到 `[` 就递归进去，遇到 `]` 返回），代码更短但需要注意下标传递。

## 高频追问

1. **`while (k--)` 有性能问题吗？** —— 大 k 时反复 `+=` 会多次扩容，可以 `reserve` 或先算总长度。
2. **递归版怎么写？** —— 用一个引用参数传下标，`[` 时递归，`]` 或越界时返回。
3. **括号不匹配怎么办？** —— 题目保证合法；若要健壮，需在 `]` 时检查栈非空。

## 易错点

- 数字用 `char` 存，遇到多位数就错
- `]` 时忘了把外层字符串接回去
- 嵌套时把 `cur` 当成了全局变量

## 关联项目

- 无（机考基本功）

## 来源

栈 + 解析（LeetCode 394 类题，预测题）
