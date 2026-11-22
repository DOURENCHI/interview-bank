---
id: Q-1646
title: 这段 C++ 代码输出什么？（28 迭代器与 string · 第 34 题）
module: 04_algo
sub: 模板与 STL
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
string s = "hello@sina.com";
cout << s.substr(0, s.find('@'));
```

- **A.** hello
- **B.** hello@
- **C.** hello@sina.com
- **D.** 编译错误

## 口述答案

答案是 **A. hello**，实际输出 `hello`。

find 返回 '@' 的下标 5；substr(0, 5) 的第二个参数是长度、不是结束下标，所以取前 5 个字符。find 找不到时返回 string::npos，不能当下标用。

## 讲深一层

substr(pos,len) 的第二个参数是长度而非结束下标，pos=5、len=5 取出 0..4 的 "hello"。pos 大于 size() 会抛 out_of_range；len 超过剩余长度则自动截到末尾，所以 substr(0,100) 安全。find 找不到时返回 string::npos，那是 size_t 最大值，不能当下标用。

## 高频追问

1. **为什么不是 hello@？** —— 长度 5 只覆盖 0 到 4，'@' 位于下标 5，被排除在外。
2. **find 返回的是什么？** —— '@' 首次出现的下标 5；找不到时返回 string::npos，不是 -1 这种有效下标。
3. **substr(6) 呢？** —— 省略长度表示取到末尾，得 "sina.com"；substr(100) 因越界抛 out_of_range。

## 易错点

- 把第二个参数当结束下标，答 hello@ 选 B
- 以为 find 失败返回 0，从而 substr(0,0) 得空串
- 用 find 的返回值直接做下标而不判 npos，越界崩溃

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 28 迭代器与 string
