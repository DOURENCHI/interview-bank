---
id: Q-1917
title: Python 要输出很多行，怎么避免 print 拖慢整体？
module: algo
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
    sys.stdout.write("\n".join(out))

main()
```

## 讲深一层

`print` 的开销不只是写数据，还包括参数解析、`sep`/`end` 处理、类型转换。二十万次调用能积累出秒级差距。

三种输出方式对比：

| 写法 | 适用 |
|---|---|
| 循环 `print` | 行数少（几百），可读性优先 |
| 攒列表 + `'\n'.join` + 一次 `write` | **推荐**，通用且快 |
| 生成器 + `writelines` | 内存紧张时，逐块写 |

内存权衡：攒列表会占内存（二十万行约几 MB，可接受）；如果输出是百万行，改用分批写入：

```python
buf = []
for i in range(1, n + 1):
    buf.append(str(i))
    if len(buf) == 10000:
        sys.stdout.write("\n".join(buf) + "\n")
        buf.clear()
if buf:
    sys.stdout.write("\n".join(buf) + "\n")
```

## 高频追问

1. **`join` 之后要不要补最后一个换行？** —— 通常要，多数 OJ 容忍没有，但补上更安全。
2. **`print` 加 `flush=False` 有用吗？** —— 默认就不 flush，除非开了 `flush=True`，这个参数帮不上忙。
3. **`writelines` 比 `join` 快吗？** —— 差不多，但 `writelines` 不会自动加分隔符，要每行自带 `\n`。

## 易错点

- ❌ 循环里 `print` 加 `flush=True` —— 每次都刷盘，最慢
- ❌ `join` 忘记元素是字符串 —— TypeError
- ❌ 分块写时忘了最后一块 —— 尾部数据丢失

## 关联项目

无。

## 来源

CPython `print` 实现与缓冲写入
