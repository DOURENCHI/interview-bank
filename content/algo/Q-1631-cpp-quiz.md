---
id: Q-1631
title: 这段 C++ 代码输出什么？（12 构造与析构 · 第 19 题）
module: algo
sub: 对象与继承
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
struct T {
    char c;
    T(char c) : c(c) { cout << c; }
    ~T() { cout << char(c - 32); }
};
int main() {
    T a('a');
    { T b('b'); }
    T c('c');
}
```

- **A.** abBcCA
- **B.** abcCBA
- **C.** abBcAC
- **D.** abcABC

## 口述答案

答案是 **A. abBcCA**，实际输出 `abBcCA`。

构造输出小写，析构输出大写。b 在花括号结束时析构；main 结束时，c 先于 a 析构（先构造的后析构）。

## 讲深一层

局部对象在作用域结束时逆序析构：b 在花括号处先析构输出 B，main 结束时 c 再 a，输出 C、A。构造正序、析构逆序是同一条栈规则，与是否同一作用域无关。char(c-32) 只对小写字母成立，构造时若传 'A' 会得到控制字符而非大写。

## 高频追问

1. **输出顺序怎么排？** —— 构造 a、b 得 ab，块结束析构 b 得 B，构造 c 得 c，main 结束析构 c、a 得 CA，合起来 abBcCA。
2. **为什么 c 先于 a 析构？** —— 两者同处 main 作用域，后构造的先析构，a 最后销毁。
3. **循环里创建对象呢？** —— 每轮迭代结束就析构一次，析构次数与构造次数相等，不会攒到循环外。

## 易错点

- 认为所有对象都在 main 结束统一析构，答 abcCBA 选 B
- 漏掉花括号让 b 提前析构，答 abcAC 之类
- 以为析构顺序与构造顺序相同，答 abcABC 选 D

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 12 构造与析构
