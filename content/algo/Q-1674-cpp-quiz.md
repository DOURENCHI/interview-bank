---
id: Q-1674
title: 这段 C++ 代码输出什么？（38 多线程与状态机 · 第 62 题）
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
int st = 0; string in = "abab", out;
for (char c : in) {
  if (st == 0) { out += toupper(c); st = 1; }
  else { out += c; st = 0; }
}
cout << out;
```

- **A.** AbAb
- **B.** ABAB
- **C.** aBaB
- **D.** abab

## 口述答案

答案是 **A. AbAb**，实际输出 `AbAb`。

两个状态交替：状态 0 把字符转大写并切到 1，状态 1 原样输出并切回 0，所以 a→A、b→b、a→A、b→b。状态机题的关键是把「当前状态 + 输入 → 次状态」列清楚再推。

## 讲深一层

讲深一层：状态只在 0/1 间翻转，本质是「按下标奇偶处理」——偶数位转大写、奇数位原样。初值 st 改成 1，输出立刻变 aBaB；输入换成 "abc" 则得 AbC。toupper 返回 int，对 ASCII 安全，但对负值字节（如 UTF-8 中文）是未定义行为，需先转 unsigned char。

## 高频追问

1. **输入是 "ABC" 会怎样？** —— 状态 0 对 A 调 toupper 仍是 A，输出 ABC；toupper 对大写字母幂等。
2. **st 换成 bool 或 enum 有区别吗？** —— 两个状态等价；状态变多时建议 enum class，避免非法值。
3. **想实现「每个单词首字母大写」怎么改？** —— 状态应记录「上一个字符是否为空格」，遇空格置 0，而不是简单奇偶翻转。

## 易错点

- 把 st==1 分支也写成 toupper：输出 ABAB，四个字符全变大写
- 忘记在分支里翻转 st：每轮都进 st==0，输出 ABAB 而不是 AbAb
- 对 char 直接 toupper 不转 unsigned char：遇到非 ASCII 字节是 UB，可能乱码或崩溃

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 38 多线程与状态机
