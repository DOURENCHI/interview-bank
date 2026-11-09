---
id: Q-1667
title: 这段 C++ 代码输出什么？（34 类型转换与模板 · 第 54 题）
module: 04_algo
sub: C++语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
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
template<class T> T add(T a, T b){ return a + b; }
int main() {
  cout << add<int>(2,3) << " " << add<double>(1.5,2.5);
}
```

- **A.** 5 4
- **B.** 5 4.0
- **C.** 5 4.5
- **D.** 编译错误

## 口述答案

答案是 **A. 5 4**，实际输出 `5 4`。

显式指定 T 后分别实例化 int 与 double 版本，结果是 5 和 4.0；cout 默认不显示末尾的 .0，所以输出 5 4。推导必须一致，add(2, 2.5) 会编译失败。

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

`教学文档/C++实验台/C++考点实验台.html` · 34 类型转换与模板
