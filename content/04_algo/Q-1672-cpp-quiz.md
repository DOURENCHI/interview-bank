---
id: Q-1672
title: 这段 C++ 代码输出什么？（37 流与字符串处理 · 第 60 题）
module: 04_algo
sub: 语法与陷阱
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/C++实验台/C++考点实验台.html
verified_at: 2026-11-21
tags: [C++, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```cpp
cout << setw(6) << setfill('0') << 42
     << " " << fixed << setprecision(2) << 3.14159;
```

- **A.** 000042 3.14
- **B.** 42 3.14
- **C.** 000042 3.14159
- **D.** 00042 3.14

## 口述答案

答案是 **A. 000042 3.14**，实际输出 `000042 3.14`。

setw(6) + setfill('0') 补成 6 位得 000042；fixed 配合 setprecision(2) 是小数点后 2 位，得 3.14（不加 fixed 则是 2 位有效数字 3.1）。setw 只对下一项有效，setfill / fixed / precision 持续有效。

## 讲深一层

讲深一层：setw 是一次性域宽，只作用于紧接的下一项；setfill、fixed、setprecision 则是粘性的，会留在流状态里。setw 的参数是含符号和小数点的总宽度，所以 setw(6)<<-42 得 -00042；浮点默认右对齐，加 left 后补的 0 跑到右边。

## 高频追问

1. **只写 setprecision(2) 不加 fixed 输出什么？** —— 3.14159 得 3.1，此时 precision 指有效数字位数，不是小数位数。
2. **setw 对字符串生效吗？** —— 生效，按字符个数补到指定宽度；但一次性，循环里每次输出都要重新写 setw。
3. **想输出带前缀的十六进制怎么办？** —— `<< hex << showbase`，或 `std::format("{:#x}", 42)`；uppercase 控制字母大小写。

## 易错点

- 把 setw 当粘性：写 `cout<<setw(6)<<42<<43`，第二个 43 没有域宽，输出 `000042 43` 而不是 `000042 000043`
- 以为 setprecision(2) 就是两位小数：不配 fixed 时是两位有效数字，3.14159 输出 3.1 而非 3.14
- 用了 setfill('0') 忘记它会一直生效：后续所有输出都用 0 填充，窄字段处会冒出一串前导零

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 37 流与字符串处理
