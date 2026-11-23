---
id: Q-1629
title: 这段 C++ 代码输出什么？（10 结构体 · 第 17 题）
module: algo
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
struct A { char c; int i; char d; };
int main() {
    cout << sizeof(A);
}
```

- **A.** 6
- **B.** 8
- **C.** 12
- **D.** 16

## 口述答案

答案是 **C. 12**，实际输出 `12`。

内存对齐：c 后补 3 字节让 i 对齐到 4 的倍数，d 后再补 3 字节让总大小是 4 的倍数。

## 讲深一层

对齐两条规则：每个成员的偏移必须是其自身对齐值的倍数，结构体总大小必须是最大对齐值的倍数。c 占 0，i 要 4 对齐所以补 3 字节到偏移 4，d 在 8，尾部再补 3 字节凑到 12。把声明改成 char c; char d; int i; 只需 8 字节。#pragma pack(1) 可压到 6。

## 高频追问

1. **12 是怎么凑出来的？** —— 1 字节 c + 3 填充 + 4 字节 i + 1 字节 d + 3 尾部填充 = 12。
2. **为什么调换顺序能变小？** —— char c; char d; int i; 时两个 char 挤在偏移 0、1，int 从 4 开始，总大小 8，省掉一块填充。
3. **怎么验证和取消对齐？** —— 用 offsetof 打印各成员偏移；#pragma pack(1) 或 __attribute__((packed)) 去掉填充，但可能带来非对齐访问开销。

## 易错点

- 直接把成员大小相加，1+4+1=6，选 A
- 只补一次尾部对齐，答 8 选 B
- 以为填充只在结构体末尾发生，忽略 i 前的 3 字节

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 10 结构体
