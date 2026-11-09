#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACM 模式输入输出专项（18 道，C++ 10 + Python 8）。

为什么单独做这一块：机考练习环境全是「给函数签名」的模式，上机要自己读输入，
格式错一位就整题 0 分。这不是算法能力问题，是工程习惯问题。

用法: python tools/seed_acm.py [--dry]
幂等：题卡带 acm_seed 标记，重跑先清后建。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "04_algo"
ID_BASE, SPAN = 1600, 500

ITEMS = [
    # ==================== C++ ====================
    {
        "title": "机考第一行给两个整数，C++ 怎么读最稳？",
        "sub": "C++ 读写", "diff": 1,
        "body": """## 题目

**输入**：第一行两个整数 `n m`，接下来 `n` 行，每行 `m` 个整数。
**输出**：所有元素之和。

```
输入样例
2 3
1 2 3
4 5 6

输出样例
21
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;      // 读失败直接退出，别硬跑
    long long sum = 0;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j) {
            int x; cin >> x;
            sum += x;
        }
    cout << sum << '\\n';
    return 0;
}
```

## 讲深一层

`cin >> x` 按**空白字符**（空格、Tab、换行）分隔，自动跳过前导空白。所以上面完全不用关心「换行在哪」——`1 2 3` 和分三行写 `1\\n2\\n3` 对 `cin >>` 是等价的。

这带来两个直接后果：

| 事实 | 影响 |
|---|---|
| `>>` 会把换行当分隔符丢掉 | 想按行读必须换 `getline` |
| 读到一个格式错误的输入会置 `failbit` | 之后所有 `cin >>` 都立刻失败，不报错也不抛异常 |

第一行加 `if (!(cin >> n >> m)) return 0;` 就是防这个——多组用例读到 EOF 时会自然退出，不会死循环。

## 高频追问

1. **`sum` 为什么用 `long long`？** —— `n*m` 个 int 累加很容易溢出。机考常见 `n,m ≤ 1000`、元素 ≤ 1e9，一乘就过 2^31。
2. **`ios::sync_with_stdio(false)` 到底关了什么？** —— 关掉 C 和 C++ 流缓冲区的同步。默认情况下 `cin` 每次都要和 `stdin` 对齐，慢一个量级。
3. **加了这行还能用 `printf` 吗？** —— 能编译能跑，但两条流顺序会乱。要么全用 C++ 流，要么全用 C 的 IO，别混。

## 易错点

- ❌ 只写 `int` 累加 —— 大数据点必挂，且挂得莫名其妙
- ❌ 忘了 `cin.tie(nullptr)` —— 只关 sync 不开 tie，`endl` 仍会 flush，还是慢
- ❌ 用 `endl` 换行 —— 每次 flush 一次。用 `'\\n'`

## 关联项目

无（机考基本功）。

## 来源

ACM 模式通用写法 + C++ 标准库 `ios_base` 行为
""",
    },
    {
        "title": "一行里给不定长个整数，C++ 怎么读到行尾？",
        "sub": "C++ 读写", "diff": 2,
        "body": """## 题目

**输入**：第一行一个整数 `n`；第二行 `n` 个整数，同一行。
**输出**：这 `n` 个数的最大值。

```
输入样例
5
3 1 4 1 5

输出样例
5
```

题面说「同一行」，但 `cin >>` 根本不看行。真正需要按行读的场景是：**这行有多少个数不确定，靠行尾判断**。

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\\n');   // 关键：吃掉第一行的换行

    string line;
    getline(cin, line);
    stringstream ss(line);
    int x, mx = INT_MIN, cnt = 0;
    while (ss >> x) { mx = max(mx, x); ++cnt; }
    cout << mx << '\\n';
    return 0;
}
```

## 讲深一层

三个层次，按需要选：

| 场景 | 写法 | 代价 |
|---|---|---|
| 个数已知，只在同一行 | 直接 `cin >> x` 循环 n 次 | 最简单，推荐 |
| 个数未知，读到行尾 | `getline` + `stringstream` | 多一次字符串构造 |
| 整份输入都要按行处理 | `while (getline(cin, line))` | 注意每行自己再切 |

`cin.ignore(...)` 这步是**必须的**：`cin >> n` 读完后，缓冲区里还留着那个换行符，紧接着的 `getline` 会立刻读到空串。这是 C++ 机考第一大坑。

## 高频追问

1. **`ignore` 的两个参数是什么？** —— 最大丢弃字符数 + 终止字符。上限用 `numeric_limits<streamsize>::max()` 表示不设限。
2. **只能用 `'\\n'` 吗？** —— Windows 下输入可能是 `\\r\\n`，`getline` 默认按 `\\n` 切，会把 `\\r` 留在行尾。如果后面要比字符串，记得 `line.pop_back()` 或 `erase` 掉 `\\r`。
3. **`stringstream` 很慢吗？** —— 比 `cin >>` 再慢一点，但机考数据量通常撑得住。真卡了再换手写解析。

## 易错点

- ❌ 忘了 `cin.ignore()` —— `getline` 拿到空串，然后整题读错
- ❌ 用 `cin.sync()` 代替 —— 各平台行为不一致，别用
- ❌ `while (ss >> x)` 写成 `while (!ss.eof())` —— eof 标志在读失败之后才置位，会多处理一次脏数据

## 关联项目

无。

## 来源

C++ 标准库 `istream::ignore` / `getline` 语义
""",
    },
    {
        "title": "输入有多少组不知道，只说到文件结束，C++ 怎么写？",
        "sub": "C++ 读写", "diff": 1,
        "body": """## 题目

**输入**：多组数据，每组一行两个整数 `a b`，直到文件结束。
**输出**：每组输出 `a+b`，一行一个。

```
输入样例
1 2
3 4

输出样例
3
7
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int a, b;
    while (cin >> a >> b) {          // 读到 EOF 自动结束
        cout << a + b << '\\n';
    }
    return 0;
}
```

## 讲深一层

`cin >> a >> b` 在流里没数据时返回的流对象会被转成 `false`，循环就退出了。**这是「读失败即结束」的惯用法**，不要写成 `while (!cin.eof())`。

原因：`eof()` 只有在**尝试读并且失败之后**才置位。写成 `while (!cin.eof())` 会多跑一轮，把上一轮的 `a`、`b` 再输出一次。

三种常见形态要能一眼认出来：

| 题面说法 | 写法 |
|---|---|
| 「直到文件结束」 | `while (cin >> a >> b)` |
| 「第一行是组数 T」 | `cin >> T; while (T--)` |
| 「以 0 0 结束」 | `while (cin >> a >> b, a || b)` |

## 高频追问

1. **`while (T--)` 会不会多跑一次？** —— `T--` 是先取值后减，`T=3` 时依次得到 3、2、1，跑三次，正确。
2. **EOF 之后还能再用 `cin` 吗？** —— 不能，`failbit` 已置位。要 `cin.clear()` 才有救，机考里通常不需要。
3. **用 `scanf` 怎么写？** —— `while (scanf("%d%d", &a, &b) != EOF)`，注意返回值是成功读入的项数，也可以是 `== 2`。

## 易错点

- ❌ `while (!cin.eof())` —— 多输出一轮脏数据
- ❌ 在循环里 `cin.clear()` —— 把结束信号清掉了，可能死循环
- ❌ 每组之间多输出空行 —— 题面没要求就是错

## 关联项目

无。

## 来源

`istream::operator bool` 与 `eofbit` / `failbit` 语义
""",
    },
    {
        "title": "第一行给组数 T，多组用例怎么组织？",
        "sub": "C++ 读写", "diff": 1,
        "body": """## 题目

**输入**：第一行 `T` 表示组数。每组一行 `n`，下一行 `n` 个整数。
**输出**：每组输出这 `n` 个数的和。

```
输入样例
2
3
1 2 3
2
10 20

输出样例
6
30
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; cin >> T;
    while (T--) {
        int n; cin >> n;
        long long s = 0;
        for (int i = 0; i < n; ++i) { int x; cin >> x; s += x; }
        cout << s << '\\n';
    }
    return 0;
}
```

## 讲深一层

多组用例的关键不是循环，而是**状态复位**：每组开始时，所有累加量、标记数组、容器都要重新初始化。

初学者最常见的错误是「第一组对、第二组错」——因为上一组的数据残留在全局数组或静态变量里。养成习惯：**变量定义在循环内部**，能局部就局部。

```cpp
while (T--) {
    int n; cin >> n;
    long long s = 0;              // 在循环内定义，天然每组归零
    vector<int> a(n);             // 同上
    ...
}
```

如果数据量大、必须复用大数组，就显式 `fill(a.begin(), a.end(), 0)`，不要靠运气。

## 高频追问

1. **`T` 组数据但每组规模不同，内存怎么安排？** —— 优先每组内重新申请；`vector` 的 `clear()` 不释放容量，能复用又不反复分配。
2. **输出时每组之间要不要空行？** —— **严格按题面**。题面没说就一行一个答案。多一个空行可能被判错。
3. **`while (T--)` 里 `T` 变成 -1 有问题吗？** —— 循环结束后 `T` 是 -1，不影响正确性，但别再拿它当组数用。

## 易错点

- ❌ 累加变量定义在循环外 —— 第二组接着第一组累加
- ❌ 用全局数组但不清零 —— 典型「对一半错一半」
- ❌ 题目说「每组之间输出空行」却忘了 —— 格式错

## 关联项目

无。

## 来源

多组测试用例通用模式
""",
    },
    {
        "title": "cin 读完后接 getline，为什么会读到空串？",
        "sub": "C++ 读写", "diff": 2,
        "body": """## 题目

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
    cin.ignore(numeric_limits<streamsize>::max(), '\\n');   // ← 少这行就全错

    for (int i = 1; i <= n; ++i) {
        string s;
        getline(cin, s);
        cout << i << ": " << s << '\\n';
    }
    return 0;
}
```

## 讲深一层

这是 C++ 机考**第一大坑**，机制如下：

```
输入缓冲区：  "2\\nhello world\\nfoo bar baz\\n"
cin >> n 后：  n = 2，缓冲区剩 "\\nhello world\\n..."
getline   ：  遇到第一个字符就是 '\\n' → 立即返回空串
```

所以第一行 `getline` 永远拿到 `""`，后面的内容整体错位一行。修法有三种，选第一种：

| 写法 | 说明 |
|---|---|
| `cin.ignore(max, '\\n')` | **推荐**。丢弃到行尾（含换行） |
| `cin.get()` | 只吃一个字符，够用但表达不清 |
| `getline` 前单独读一行 | 也有效，多一次无用调用 |

反过来也成立：`getline` 之后接 `cin >>`，如果整行都被 `getline` 吃掉了，不会有残留问题。**只有 `>>` → `getline` 这个方向需要 ignore。**

## 高频追问

1. **如果输入行尾是 `\\r\\n`（Windows 换行）呢？** —— `getline` 按 `\\n` 切，`\\r` 会留在串尾。要做字符串比较就 `if (!s.empty() && s.back() == '\\r') s.pop_back();`
2. **`ignore` 能不能不带参数？** —— `cin.ignore()` 只丢一个字符，不够。
3. **能不能统一全用 `getline` 再解析？** —— 可以，而且更稳：所有行都 `getline`，数字用 `stoi` / `stringstream` 转。代价是慢一点。

## 易错点

- ❌ 不 ignore 直接 `getline` —— 第一行空串，全部错位
- ❌ `cin.sync()` 当 ignore 用 —— 行为不确定
- ❌ 每轮循环都 ignore —— 会把有效数据也吃掉

## 关联项目

无。

## 来源

`istream` 缓冲语义；`getline` 遇 `\\n` 立即返回
""",
    },
    {
        "title": "输入是逗号分隔的一串数，C++ 怎么解析？",
        "sub": "C++ 读写", "diff": 2,
        "body": """## 题目

**输入**：一行逗号分隔的整数，如 `1,2,3,4`（可能带空格 `1, 2, 3`）。
**输出**：升序排序后，用逗号连接输出。

```
输入样例
3,1,4,1,5

输出样例
1,1,3,4,5
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    getline(cin, line);

    vector<int> a;
    stringstream ss(line);
    string tok;
    while (getline(ss, tok, ',')) {        // 按逗号切
        if (tok.empty()) continue;
        // 去掉可能的前导空格
        size_t b = tok.find_first_not_of(" \\t");
        if (b == string::npos) continue;
        a.push_back(stoi(tok.substr(b)));
    }

    sort(a.begin(), a.end());
    for (size_t i = 0; i < a.size(); ++i) {
        if (i) cout << ',';
        cout << a[i];
    }
    cout << '\\n';
    return 0;
}
```

## 讲深一层

`getline(ss, tok, ',')` 是带自定义分隔符的版本。注意它的行为和 `cin >>` 完全不同：**不跳过空白，也不把分隔符当多个连续分隔处理**。

所以 `1, 2` 切出来是 `"1"` 和 `" 2"`——第二个带前导空格。`stoi` 其实会跳过前导空格，所以这里能过；但如果要做严格字符串比较，就得自己 trim。

输入形态对照：

| 分隔符 | 写法 |
|---|---|
| 空格/Tab/换行 | `cin >>` 或 `ss >>` |
| 逗号 | `getline(ss, tok, ',')` |
| 混合（逗号后带空格） | 先按逗号切，再 trim |
| 变长字段 | 手写双指针扫描，最可靠 |

## 高频追问

1. **`stoi` 遇到非法字符怎么办？** —— 抛 `invalid_argument`。机考里要么确保格式合法，要么用 `try/catch` 兜住。
2. **最后一个 token 后面有逗号会怎样？** —— 会切出一个空串，`skip` 掉即可。
3. **数据量很大时 `stringstream` 会不会太慢？** —— 会。几十万级建议手写指针扫描。

## 易错点

- ❌ 以为 `getline` 会 trim —— 不会，空格原样保留
- ❌ 用 `cin >>` 读逗号分隔 —— `>>` 不认逗号，会读失败
- ❌ 输出时末尾多一个逗号 —— 格式错

## 关联项目

无。

## 来源

`std::getline` 三分隔符版本语义
""",
    },
    {
        "title": "输出要求空格分隔，行末不能有多余空格，怎么写？",
        "sub": "C++ 读写", "diff": 1,
        "body": """## 题目

**输入**：一个整数 `n`，随后 `n` 个整数。
**输出**：原样输出，**数与数之间一个空格，行末不能有空格**。

```
输入样例
3
1 2 3

输出样例（注意 3 后面没有空格）
1 2 3
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    for (int i = 0; i < n; ++i) {
        int x; cin >> x;
        if (i) cout << ' ';        // 第一个不输出空格
        cout << x;
    }
    cout << '\\n';
    return 0;
}
```

## 讲深一层

「行末多余空格」是 OJ 评判里最常见的非算法失分点。有些 OJ 会忽略行末空白，有些**严格逐字符比对**——你没法预知，所以一律按严格标准写。

三种可行写法，按推荐排序：

| 写法 | 说明 |
|---|---|
| `if (i) cout << ' ';` | 最直观，零额外开销 |
| 先输出第一个，循环从 1 开始 | 等价，少一次判断 |
| 攒进 `vector` 再用 `join` 思路 | Python 更常用，C++ 略显重 |

反过来，如果用 Python 的 `' '.join(...)`，天然没有行末空格，这是 Python 在这件事上的优势。

## 高频追问

1. **每行最后输出 `\\n` 还是 `endl`？** —— `'\\n'`。`endl` 每次强制 flush，大数据量下慢几倍。
2. **多组用例之间有空白要求怎么办？** —— 严格照题面。常见是「每组之间一个空行」，但最后一行后面不要。
3. **最后一行要不要换行符？** —— 通常要，多数 OJ 容忍没有，但加上更安全。

## 易错点

- ❌ `cout << x << " ";` 收尾 —— 行末多一个空格
- ❌ 用 `endl` 换行 —— 性能问题
- ❌ 多组用例之间乱加空行 —— 格式错

## 关联项目

无。

## 来源

OJ 输出格式严格匹配惯例
""",
    },
    {
        "title": "输出要保留两位小数，C++ 怎么写才不被判格式错？",
        "sub": "C++ 读写", "diff": 1,
        "body": """## 题目

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

    cout << fixed << setprecision(2) << (s / n) << '\\n';
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
""",
    },
    {
        "title": "数据量到了十万级，C++ 读入太慢超时怎么办？",
        "sub": "C++ 读写", "diff": 2,
        "body": """## 题目

**输入**：`n` 个数（`n ≤ 1e6`），求最大值。
**输出**：最大值。

这是典型的「算法对但 IO 超时」场景。

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);   // 关 C/C++ 流同步
    cin.tie(nullptr);              // 解除 cin 与 cout 绑定

    int n; cin >> n;
    int mx = INT_MIN, x;
    for (int i = 0; i < n; ++i) { cin >> x; if (x > mx) mx = x; }
    cout << mx << '\\n';
    return 0;
}
```

再快一档是手写快读（百万级以上才需要）：

```cpp
static inline int read() {
    int x = 0, f = 1; char c = getchar();
    while (c < '0' || c > '9') { if (c == '-') f = -1; c = getchar(); }
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = getchar(); }
    return x * f;
}
```

## 讲深一层

三档速度，按数据量选：

| 做法 | 相对速度 | 适用 |
|---|---|---|
| 默认 `cin` | 1x | 1e4 以内 |
| `sync_with_stdio(false)` + `tie(nullptr)` | 3–5x | 1e5–1e6，**大多数机考够用** |
| 手写 `getchar` 快读 | 8–10x | 1e6 以上，或已知卡 IO |

原理：`sync_with_stdio(false)` 让 `cin` 不再每次和 `stdin` 同步缓冲区；`tie(nullptr)` 让 `cin` 读之前不再先 flush `cout`（默认是绑定的，每读一次可能刷一次输出）。

**注意 `tie(nullptr)` 必须在任何 IO 之前调用**，中途调用无效。

## 高频追问

1. **关了 sync 还能用 `scanf` 吗？** —— 能编译，但两套缓冲各自为政，输出顺序会乱。全用一套。
2. **`getchar_unlocked` 是什么？** —— POSIX 的非线程安全版本，更快，但 Windows/MSVC 没有。机考环境不确定就用 `getchar`。
3. **怎么知道是 IO 慢还是算法慢？** —— 看数据点：小数据过、大数据超时，多半是复杂度；所有点都临界超时，才怀疑 IO。

## 易错点

- ❌ 只关 sync 不开 tie —— 提速有限
- ❌ 用 `endl` —— 刚省下的时间又还回去
- ❌ 手写快读没处理负数和 EOF —— 边界全错

## 关联项目

无。

## 来源

C++ 流缓冲机制；竞赛快读惯例
""",
    },
    {
        "title": "输入里混着数字和字符串，C++ 怎么读不串行？",
        "sub": "C++ 读写", "diff": 2,
        "body": """## 题目

**输入**：第一行 `n`；随后 `n` 行，每行形如 `名字 分数`（名字不含空格）。
**输出**：按分数降序，输出 `名字 分数`。

```
输入样例
3
tom 90
amy 95
bob 88

输出样例
amy 95
tom 90
bob 88
```

## 口述答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    vector<pair<string,int>> v(n);
    for (int i = 0; i < n; ++i) cin >> v[i].first >> v[i].second;

    stable_sort(v.begin(), v.end(),
                [](auto& a, auto& b){ return a.second > b.second; });

    for (auto& p : v) cout << p.first << ' ' << p.second << '\\n';
    return 0;
}
```

## 讲深一层

`cin >> string` 读的是「到下一个空白为止」，所以名字里**不能有空格**。题面说「名字不含空格」就能直接用；如果名字可能含空格（如 `Li Ming`），就必须 `getline` 整行再切分——这是两道完全不同的题。

排序稳定性：
- `sort` 不稳定，同分元素的相对顺序不定
- `stable_sort` 稳定，保持输入顺序

题面若要求「同分按输入顺序」，必须用 `stable_sort`，或者排序时把原始下标作为第二关键字。

## 高频追问

1. **`cin >> string` 遇到空行怎么办？** —— 会跳过空白继续找下一个 token，不会返回空串。想读空行必须 `getline`。
2. **`pair` 的默认比较是什么？** —— 先比 `first` 再比 `second`。这里要按分数降序，所以必须自定义比较器。
3. **`auto&` 在 lambda 参数里为什么带 `&`？** —— 避免拷贝。用 `const auto&` 更严谨。

## 易错点

- ❌ 用 `sort` 但题面要求稳定 —— 同分顺序错
- ❌ 比较器写成 `>=` —— `sort` 要求严格弱序，`>=` 会越界崩溃
- ❌ 名字含空格却用 `cin >>` —— 只读到第一个词

## 关联项目

无。

## 来源

`istream::operator>>(string)` 与 `stable_sort` 语义
""",
    },

    # ==================== Python ====================
    {
        "title": "Python 机考第一行两个整数，怎么写最快？",
        "sub": "Python 读写", "diff": 1,
        "body": """## 题目

**输入**：第一行 `n m`，接下来 `n` 行每行 `m` 个整数。
**输出**：元素之和。

```
输入样例
2 3
1 2 3
4 5 6

输出样例
21
```

## 口述答案

```python
import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    total = 0
    for _ in range(n * m):
        total += int(next(it))
    print(total)

main()
```

## 讲深一层

Python 机考的核心思路是：**一次性读完全部输入，再按需要切片**。因为 `input()` 每调一次就是一次系统调用级别的开销，百万行时会明显拖慢。

三种读法对比：

| 写法 | 速度 | 适用 |
|---|---|---|
| `input()` 逐行 | 最慢 | 行数少，逻辑按行处理 |
| `sys.stdin.readline()` | 快 2–3 倍 | 需要按行处理 |
| `sys.stdin.read().split()` | 最快 | **数字为主的题，首选** |

`split()` 不传参数时按任意空白切分（空格、Tab、换行都算），所以上面完全不用管「换行在哪」，和 C++ 的 `cin >>` 等价。

## 高频追问

1. **`iter` + `next` 是必须的吗？** —— 不是，但用它按需取 token 比维护下标 `i` 更不容易越界。
2. **`sys.stdin.read()` 会不会内存爆？** —— 会。几十万 token 没问题，上千万就要改按行读。
3. **为什么包一层 `main()`？** —— 局部变量比全局变量快（`LOAD_FAST` vs `LOAD_GLOBAL`），数据量大时有可观差距。

## 易错点

- ❌ 用 `input()` 读百万行 —— 超时
- ❌ `split()` 后发现 token 数不够 —— 题面格式看错了，加断言能早发现
- ❌ 忘了 `int()` 转换 —— 字符串累加会变成拼接

## 关联项目

无。

## 来源

`sys.stdin.read` / `str.split` 语义
""",
    },
    {
        "title": "Python 一行给不定长整数，怎么读到行尾？",
        "sub": "Python 读写", "diff": 2,
        "body": """## 题目

**输入**：第一行 `n`；第二行 `n` 个整数（同一行）。
**输出**：最大值。

```
输入样例
5
3 1 4 1 5

输出样例
5
```

## 口述答案

```python
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    print(max(a[:n]))          # 只取前 n 个，防止行尾有脏数据

main()
```

## 讲深一层

`line.split()` 按空白切分，返回字符串列表；`map(int, ...)` 批量转整数。这是 Python 处理「一行多个数」的标准写法。

需要注意的边界：

| 情况 | 处理 |
|---|---|
| 行尾有空格 | `split()` 自动忽略，没问题 |
| 这行只有一个数 | 也能正常工作，返回长度 1 的列表 |
| 数跨了多行 | 这行读法就错了，要用 `sys.stdin.read().split()` |
| 数字之间有逗号 | 先 `split(',')` 再 `int`，并且要 `strip()` 空格 |

`sorted` 与内存：`list(map(...))` 会一次性建列表。如果只需要最大值，可以直接 `max(map(int, input().split()))`，省一个列表。

## 高频追问

1. **`input()` 和 `sys.stdin.readline()` 差别？** —— `input()` 会去掉行尾 `\\n`，`readline()` 保留，需要自己 `strip()`。前者还会尝试解析 exec 相关逻辑（Python 3 已简化），略慢。
2. **`split()` 不带参数和带参数的区别？** —— 不带参数按任意空白切且忽略空串；带参数（如 `split(',')`）按字面切，**会保留空串**。
3. **数据量很大时 `map` 和列表推导谁快？** —— `map(int, ...)` 通常快一点，且省内存（惰性）。

## 易错点

- ❌ `int(input())` 读一行多个数 —— 直接 ValueError
- ❌ 忘了 `strip()` 就用 `readline()` —— 末尾 `\\n` 进到数据里
- ❌ `split(',')` 后不 trim —— `' 2'` 转 int 虽然能过，但字符串比较会错

## 关联项目

无。

## 来源

`str.split` / `map` 语义
""",
    },
    {
        "title": "Python 读到文件结束怎么写？",
        "sub": "Python 读写", "diff": 1,
        "body": """## 题目

**输入**：多组数据，每组一行两个整数，直到文件结束。
**输出**：每组输出 `a+b`。

```
输入样例
1 2
3 4

输出样例
3
7
```

## 口述答案

```python
import sys

def main():
    out = []
    for line in sys.stdin:                 # 逐行迭代，读到 EOF 自然结束
        line = line.strip()
        if not line:
            continue                        # 跳过空行
        a, b = map(int, line.split())
        out.append(str(a + b))
    sys.stdout.write("\\n".join(out))

main()
```

## 讲深一层

`for line in sys.stdin` 是最 Pythonic 的读法：它按行迭代，遇到 EOF 自动停，不抛异常。比 `while True: input()` 加 `try/except EOFError` 干净得多。

几个常见变体：

| 题面 | 写法 |
|---|---|
| 直到文件结束 | `for line in sys.stdin:` |
| 第一行是组数 | `t = int(input()); for _ in range(t):` |
| 以 `0 0` 结束 | 循环里判断 `if a == 0 and b == 0: break` |
| 读到空行为止 | `while True: line = input(); if not line: break` |

注意 `for line in sys.stdin` 读到空行时 `line` 是 `'\\n'`，`strip()` 后变空串——**空行不是 EOF**，要自己判断。

## 高频追问

1. **`sys.stdin` 能迭代几次？** —— 只能一次。它是流，读完就没了。要复用先 `readlines()`。
2. **`input()` 版的 EOF 怎么处理？** —— `try: ... except EOFError: break`，比迭代版啰嗦。
3. **输出为什么要先攒起来？** —— 每行 `print` 都是一次写操作，攒起来一次性 `write` 快很多。

## 易错点

- ❌ 用 `while True` 不加 break 条件 —— 死循环
- ❌ 把空行当 EOF —— 提前退出
- ❌ 每组都 `print` —— 数据量大时慢

## 关联项目

无。

## 来源

文件对象迭代协议
""",
    },
    {
        "title": "Python 多组测试用例怎么组织，才不会串数据？",
        "sub": "Python 读写", "diff": 2,
        "body": """## 题目

**输入**：第一行 `T` 组数。每组一行 `n`，下一行 `n` 个数。
**输出**：每组输出这组数的和。

```
输入样例
2
3
1 2 3
2
10 20

输出样例
6
30
```

## 口述答案

```python
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    res = []
    for _ in range(T):
        n = int(data[idx]); idx += 1
        s = 0
        for _ in range(n):
            s += int(data[idx]); idx += 1
        res.append(str(s))
    print("\\n".join(res))

main()
```

## 讲深一层

多组用例最怕「上一组的数据留在变量里」。Python 比 C++ 好一点：函数内局部变量天然隔离，但两种情况仍会出事：

1. 可变默认参数：`def f(a=[])` —— 默认列表在多次调用间共享
2. 循环外定义的列表没清空：`buf = []` 在 `for` 外面

养成习惯：**每组需要的容器都在组内新建**。

下标指针写法（`idx`）比 `iter/next` 更好调试——出错时能打印 `idx` 看读到哪了。数据量超大时 `next()` 略快，但差别很小。

## 高频追问

1. **`idx` 越界怎么办？** —— 说明题面格式理解错了。机考时加一句 `assert idx <= len(data)`，本地能立刻发现问题。
2. **组间要输出空行怎么办？** —— `res.append(str(s)); if _ < T-1: res.append("")`，注意最后一组后面不加。
3. **能不能用 `iter` + `next`？** —— 能，更简洁但不好查错。两者都可接受。

## 易错点

- ❌ 累积变量定义在循环外 —— 第二组接着第一组
- ❌ 用可变对象当默认参数 —— 跨调用污染
- ❌ 组间空行多输出一个 —— 格式错

## 关联项目

无。

## 来源

多组用例通用模式
""",
    },
    {
        "title": "Python 要读一整行（含空格），怎么写？",
        "sub": "Python 读写", "diff": 1,
        "body": """## 题目

**输入**：第一行 `n`；随后 `n` 行，每行一个可能含空格的句子。
**输出**：逐行原样输出，前面加行号。

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

```python
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    for i in range(1, n + 1):
        s = input().rstrip("\\n")        # 只去换行，保留行内空格
        print(f"{i}: {s}")

main()
```

## 讲深一层

关键区别：`split()` 会把空格当分隔符**吃掉**，`rstrip("\\n")` 只去掉行尾换行符，行内空格完整保留。

对比三种去空白方式：

| 写法 | 行为 | 什么时候用 |
|---|---|---|
| `s.rstrip("\\n")` | 只去尾部换行 | **读整行内容时** |
| `s.strip()` | 去首尾所有空白（含空格） | 读数字/单 token 时 |
| 不去 | 保留 `\\n` | 几乎从不 |

如果一行里既有空格又不能用 `split()`，就得手工截取——比如「名字 + 一串数字」这种混合格式。

## 高频追问

1. **`rstrip("\\n")` 和 `rstrip()` 有区别吗？** —— 有。不带参数会去掉**所有**尾部空白，包括有意义的前导/尾随空格。读文本时必须带参数。
2. **`input()` 要不要再 `rstrip`？** —— 不用，`input()` 已经去掉行尾换行。但它不能用在需要保留行尾空格的场景（极少）。
3. **Windows 下读到 `\\r\\n` 怎么办？** —— `rstrip("\\r\\n")` 两个都去掉。

## 易错点

- ❌ 用 `split()[0]` 取整行 —— 只拿到第一个词
- ❌ 用 `strip()` 读句子 —— 句首句尾的空格被吃掉
- ❌ 忘了 `int(input())` 后行位置 —— `readline` 不会多读，这里安全

## 关联项目

无。

## 来源

`str.rstrip` 与 `input()` 语义
""",
    },
    {
        "title": "Python 输出要求空格分隔且行末不能有空格，怎么写？",
        "sub": "Python 读写", "diff": 1,
        "body": """## 题目

**输入**：`n` 个整数。
**输出**：原样输出，数与数之间一个空格，**行末无空格**。

```
输入样例
3
1 2 3

输出样例
1 2 3
```

## 口述答案

```python
import sys

def main():
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))[:n]

    print(" ".join(map(str, a)))                 # 推荐：天然无行末空格
    # print(*a)                                  # 也行，sep 默认就是空格
    # print(*a, sep=" ")                         # 显式写法

main()
```

## 讲深一层

Python 在这件事上比 C++ 省心：`' '.join(...)` 由分隔符**连接**元素，天然不会在末尾留下分隔符。

`print(*a)` 是把列表展开成位置参数，`sep` 默认就是空格，效果一样。两者选择：

| 写法 | 适用 |
|---|---|
| `' '.join(map(str, a))` | 元素需要转换或格式化时 |
| `print(*a)` | 元素已是字符串或直接可打印时，最简洁 |
| `print(*a, sep=", ")` | 自定义分隔符 |

注意 `print` 默认在末尾加 `\\n`，如果题面要求「最后一行不换行」，要 `print(..., end="")`。

## 高频追问

1. **元素是浮点要保留两位怎么办？** —— `' '.join(f"{x:.2f}" for x in a)`。
2. **`print(*a)` 会不会有性能问题？** —— 元素极多时展开成参数有开销，几万个还行，几十万建议用 `join`。
3. **要输出到同一行并追加怎么办？** —— `print(x, end=" ")`，但注意最后一次的尾随空格。

## 易错点

- ❌ `for x in a: print(x, end=" ")` —— 末尾多一个空格
- ❌ `print(a)` —— 打印成 `[1, 2, 3]`，带方括号和逗号
- ❌ 忘了 `map(str, ...)` —— `join` 只接受字符串

## 关联项目

无。

## 来源

`str.join` 与 `print` 的 `sep`/`end` 语义
""",
    },
    {
        "title": "Python 读百万级数据超时，怎么优化输入？",
        "sub": "Python 读写", "diff": 2,
        "body": """## 题目

**输入**：`n` 个数（`n ≤ 1e6`），求最大值。
**输出**：最大值。

典型「算法对但 IO 超时」场景。

## 口述答案

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    mx = max(map(int, data[1:n + 1]))
    sys.stdout.write(str(mx))

main()
```

## 讲深一层

关键在 `sys.stdin.buffer`：它拿到的是**字节流**，跳过文本解码这一层。

| 写法 | 相对速度 | 说明 |
|---|---|---|
| `input()` 逐行 | 1x | 每次都要解码 + 去换行 |
| `sys.stdin.readline()` | 2–3x | 仍走文本层 |
| `sys.stdin.read()` | 5x | 一次读完，文本层 |
| `sys.stdin.buffer.read()` | 8–10x | **字节层，最快** |

`buffer.read().split()` 得到的是 `bytes` 列表，`int(b'123')` 是合法的（Python 会自动转），所以后面照常处理。

另一个隐藏瓶颈是 `print`：每次 `print` 都要拼缓冲并可能 flush。循环里输出几万行时，攒成列表再 `'\\n'.join` 一次性写，能差出好几秒。

## 高频追问

1. **`bytes` 和 `str` 混用会出错吗？** —— `int()` 和比较都能用，但 `b'abc' == 'abc'` 是 `False`。只要不混着比字符串就没事。
2. **`sys.setrecursionlimit` 要不要设？** —— 写递归 DFS 时务必设，默认 1000 层，图/树题容易爆。设到 1e6 还要注意真爆栈时进程会崩。
3. **PyPy 会不会更快？** —— 循环密集的题快很多，但机考环境用什么由平台决定，不能假设。

## 易错点

- ❌ 用 `input()` 读百万行 —— 必超时
- ❌ 循环 `print` —— 输出成瓶颈
- ❌ `buffer.read()` 后又想 `split()` 按行处理 —— 换行已被切掉，得自己重新组装

## 关联项目

无。

## 来源

`sys.stdin.buffer` 与 CPython IO 开销
""",
    },
    {
        "title": "Python 要输出很多行，怎么避免 print 拖慢整体？",
        "sub": "Python 读写", "diff": 2,
        "body": """## 题目

**输入**：`n`（`n ≤ 2e5`）。
**输出**：`1` 到 `n`，每行一个。

```
输入样例
3

输出样例
1
2
3
```

## 口述答案

```python
import sys

def main():
    n = int(sys.stdin.readline())
    out = []
    for i in range(1, n + 1):
        out.append(str(i))
    sys.stdout.write("\\n".join(out))

main()
```

## 讲深一层

`print` 的开销不只是写数据，还包括参数解析、`sep`/`end` 处理、类型转换。二十万次调用能积累出秒级差距。

三种输出方式对比：

| 写法 | 适用 |
|---|---|
| 循环 `print` | 行数少（几百），可读性优先 |
| 攒列表 + `'\\n'.join` + 一次 `write` | **推荐**，通用且快 |
| 生成器 + `writelines` | 内存紧张时，逐块写 |

内存权衡：攒列表会占内存（二十万行约几 MB，可接受）；如果输出是百万行，改用分批写入：

```python
buf = []
for i in range(1, n + 1):
    buf.append(str(i))
    if len(buf) == 10000:
        sys.stdout.write("\\n".join(buf) + "\\n")
        buf.clear()
if buf:
    sys.stdout.write("\\n".join(buf) + "\\n")
```

## 高频追问

1. **`join` 之后要不要补最后一个换行？** —— 通常要，多数 OJ 容忍没有，但补上更安全。
2. **`print` 加 `flush=False` 有用吗？** —— 默认就不 flush，除非开了 `flush=True`，这个参数帮不上忙。
3. **`writelines` 比 `join` 快吗？** —— 差不多，但 `writelines` 不会自动加分隔符，要每行自带 `\\n`。

## 易错点

- ❌ 循环里 `print` 加 `flush=True` —— 每次都刷盘，最慢
- ❌ `join` 忘记元素是字符串 —— TypeError
- ❌ 分块写时忘了最后一块 —— 尾部数据丢失

## 关联项目

无。

## 来源

CPython `print` 实现与缓冲写入
""",
    },
]

FM = """---
id: {qid}
title: {title}
module: 04_algo
sub: {sub}
priority: P0
difficulty: {diff}
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 机考 ACM 模式通用写法整理
verified_at: 2026-11-09
tags: [ACM, 输入输出, 机考, {sub}]
auto: true
acm_seed: true
---

{body}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    removed = 0
    for f in CONTENT.glob("Q-*.md"):
        if re.search(r"^acm_seed: true", f.read_text(encoding="utf-8"), re.M):
            f.unlink()
            removed += 1
    if removed:
        print(f"清理旧 ACM 题卡 {removed} 张")

    nums = [int(m.group(1)) for f in CONTENT.glob("Q-*.md")
            if (m := re.match(r"Q-(\d+)", f.name))]
    nxt = max(nums + [ID_BASE]) + 1
    start = nxt

    for it in ITEMS:
        if nxt >= ID_BASE + SPAN:
            print(f"⚠ 号段用尽，停在 {nxt}")
            return 1
        qid = f"Q-{nxt:04d}"
        if not args.dry:
            (CONTENT / f"{qid}-acm-io.md").write_text(
                FM.format(qid=qid, title=it["title"], sub=it["sub"],
                          diff=it["diff"], body=it["body"]), encoding="utf-8")
        nxt += 1

    print(f"{'预览' if args.dry else '生成'} {len(ITEMS)} 道 → Q-{start:04d} ~ Q-{nxt-1:04d}")
    from collections import Counter
    c = Counter(i["sub"] for i in ITEMS)
    for k, v in c.items():
        print(f"  {k:12s}{v:3d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
