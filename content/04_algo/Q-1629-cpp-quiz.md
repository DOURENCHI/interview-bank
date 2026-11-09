---
id: Q-1629
title: 这段 C++ 代码输出什么？（10 预处理 · 第 16 题）
module: 04_algo
sub: C++语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/C++实验台/C++考点实验台.html
verified_at: 2026-11-09
tags: [C++, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```cpp
#define SQ(x) x * x
int main() {
    cout << SQ(1 + 2);
}
```

- **A.** 9
- **B.** 5
- **C.** 7
- **D.** 3

## 口述答案

答案是 **B. 5**，实际输出 `5`。

宏是文本替换：1 + 2 * 1 + 2 = 5。正确写法是 ((x) * (x))。

## 讲深一层

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 10 预处理
