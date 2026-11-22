---
id: Q-1904
title: cin 读完后接 getline，为什么会读到空串？
module: 04_algo
sub: ACM 读写
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 机考 ACM 模式通用写法整理
verified_at: 2026-11-09
tags: [ACM, 输入输出, 机考, C++ 读写]
auto: true
acm_seed: true
---

## 题目

**输入**：第一行一个整数 `n`；随后 `n` 行，每行一个可能含空格的字符串。
**输出**：逐行原样输出，并在前面加行号。

```
输入样例
2
hello world
foo bar baz

输出样例
1: hello world
2: foo bar baz
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');   // ← 少这行就全错

    for (int i = 1; i <= n; ++i) {
        string s;
        getline(cin, s);
        cout << i << ": " << s << '\n';
    }
    return 0;
}
```

## 讲深一层

这是 C++ 机考**第一大坑**，机制如下：

```
输入缓冲区：  "2\nhello world\nfoo bar baz\n"
cin >> n 后：  n = 2，缓冲区剩 "\nhello world\n..."
getline   ：  遇到第一个字符就是 '\n' → 立即返回空串
```

所以第一行 `getline` 永远拿到 `""`，后面的内容整体错位一行。修法有三种，选第一种：

| 写法 | 说明 |
|---|---|
| `cin.ignore(max, '\n')` | **推荐**。丢弃到行尾（含换行） |
| `cin.get()` | 只吃一个字符，够用但表达不清 |
| `getline` 前单独读一行 | 也有效，多一次无用调用 |

反过来也成立：`getline` 之后接 `cin >>`，如果整行都被 `getline` 吃掉了，不会有残留问题。**只有 `>>` → `getline` 这个方向需要 ignore。**

## 高频追问

1. **如果输入行尾是 `\r\n`（Windows 换行）呢？** —— `getline` 按 `\n` 切，`\r` 会留在串尾。要做字符串比较就 `if (!s.empty() && s.back() == '\r') s.pop_back();`
2. **`ignore` 能不能不带参数？** —— `cin.ignore()` 只丢一个字符，不够。
3. **能不能统一全用 `getline` 再解析？** —— 可以，而且更稳：所有行都 `getline`，数字用 `stoi` / `stringstream` 转。代价是慢一点。

## 易错点

- ❌ 不 ignore 直接 `getline` —— 第一行空串，全部错位
- ❌ `cin.sync()` 当 ignore 用 —— 行为不确定
- ❌ 每轮循环都 ignore —— 会把有效数据也吃掉

## 关联项目

无。

## 来源

`istream` 缓冲语义；`getline` 遇 `\n` 立即返回
