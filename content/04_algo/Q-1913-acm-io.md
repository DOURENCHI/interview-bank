---
id: Q-1913
title: Python 多组测试用例怎么组织，才不会串数据？
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
tags: [ACM, 输入输出, 机考, Python 读写]
auto: true
acm_seed: true
---

## 题目

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
    print("\n".join(res))

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
