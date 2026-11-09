---
id: Q-1908
title: 输出要保留两位小数，C++ 怎么写才不被判格式错？
module: 04_algo
sub: C++ 读写
priority: P0
difficulty: 1
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

**输入**：一个整数 `n`，随后 `n` 个浮点数。
**输出**：平均值，**保留两位小数**。

```
输入样例
3
1.0 2.0 4.0

输出样例
2.33
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    double s = 0, x;
    for (int i = 0; i < n; ++i) { cin >> x; s += x; }

    cout << fixed << setprecision(2) << (s / n) << '\n';
    return 0;
}
```

## 讲深一层

`fixed` 和 `setprecision` 必须搭配，且**会持久生效**——设置一次，后面所有浮点输出都按这个格式走。

| 组合 | 效果 |
|---|---|
| `setprecision(2)` 单独用 | 保留 2 位**有效数字**，`2.33` → `2.3` |
| `fixed + setprecision(2)` | 保留 2 位**小数**，`2.33` → `2.33` |
| `defaultfloat` | 恢复默认（按有效数字，自动选定点/科学计数） |

所以如果前面某处设了 `fixed`，后面输出整数不受影响，但输出其他浮点会被一起改掉。多组用例里要么每组重设，要么明确知道自己在做什么。

另一个坑：`printf("%.2f")` 和 `cout << fixed << setprecision(2)` 的**舍入规则一致**（都是四舍六入五成双的 IEEE 行为），但累加过程中的浮点误差可能导致 `2.335` 变成 `2.33` 而不是 `2.34`。题面若给了误差范围（如「误差不超过 1e-2」），按误差判；若要求精确匹配，得注意累加顺序。

## 高频追问

1. **`double` 够吗，要不要 `long double`？** —— 一般够。但如果题面说「误差 1e-9」，用 `long double` 更稳。
2. **负数怎么四舍五入？** —— C++ 的格式化按 IEEE 规则，`-2.345` 保留两位是 `-2.35`（远离零），不是向零截断。
3. **能不能先乘 100 再加 0.5 取整？** —— 能，但负数会错，且大数会溢出。别手写，用流格式。

## 易错点

- ❌ 只 `setprecision(2)` 不加 `fixed` —— 保留的是有效数字
- ❌ 用 `endl` —— 无谓 flush
- ❌ 忘了每组重置格式 —— 上一组的 `fixed` 影响下一组

## 关联项目

无。

## 来源

`<iomanip>` 的 `fixed` / `setprecision` 语义
