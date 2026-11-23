---
id: Q-1839
title: 字符串相乘：为什么要转成数组模拟竖式？
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
verified_at: 2026-11-09
tags: [字符串, 数学]
hint: 结果长度最多 m+n，用 int 数组存每位累加值，最后统一进位。直接转整数会溢出。
auto: true
algo_seed: true
---

## 题目

**输入**：`num1 = "123", num2 = "456"`
**输出**：`"56088"`
**限制**：不能直接把字符串转整数，也不能用大数库。

**问**：为什么转成数组模拟竖式？

## 口述答案

> 因为结果可能远超 `long long` 范围（几十位），必须自己处理大数。
> 做法是模拟竖式：结果长度最多 `m+n`，用 int 数组存每一位的累加值，
> 两层循环把 `num1[i] * num2[j]` 累加到 `res[i+j+1]`，
> 最后从后往前统一处理进位。

## 讲深一层

```cpp
string multiply(string a, string b) {
    if (a == "0" || b == "0") return "0";
    int m = a.size(), n = b.size();
    vector<int> r(m + n, 0);
    for (int i = m - 1; i >= 0; --i)
        for (int j = n - 1; j >= 0; --j) {
            int mul = (a[i]-'0') * (b[j]-'0');
            int p1 = i + j, p2 = i + j + 1;
            int sum = mul + r[p2];
            r[p2] = sum % 10;
            r[p1] += sum / 10;
        }
    string s;
    for (int x : r) if (!(s.empty() && x == 0)) s += char('0' + x);
    return s.empty() ? "0" : s;
}
```

**下标 `i+j+1`** 是关键：两个一位数相乘的结果最多两位，落在 `i+j` 和 `i+j+1`。

## 高频追问

1. **为什么是 `i+j+1` 不是 `i+j`？** —— 从后往前存储，个位在末尾。
2. **进位为什么直接加到 `r[p1]`？** —— 它的值可能超过 9，但最后统一处理也行；这里是用「边算边进位」。
3. **加法版本呢？** —— 更简单，双指针从后往前加 + 进位。

## 易错点

- ❌ 下标写成 `i+j` —— 结果整体偏位
- ❌ 忘了去掉前导 0
- ❌ 用 `int` 直接转 —— 溢出


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
