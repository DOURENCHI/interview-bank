---
id: Q-1640
title: 这段 C++ 代码输出什么？（20 模板 · 第 27 题）
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
template <typename T>
T mx(T a, T b) { return a > b ? a : b; }
int main() {
    cout << mx(3, 5) << " " << mx<double>(3, 5.5);
}
```

- **A.** 5 5.5
- **B.** 5 5
- **C.** 3 5.5
- **D.** 编译错误

## 口述答案

答案是 **A. 5 5.5**，实际输出 `5 5.5`。

mx(3, 5) 推导出 T = int；显式写 mx<double> 后，3 被转换成 3.0。

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

`教学文档/C++实验台/C++考点实验台.html` · 20 模板
