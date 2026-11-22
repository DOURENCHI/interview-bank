---
id: Q-1666
title: 这段 C++ 代码输出什么？（34 类型转换与模板 · 第 54 题）
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

显式写 add<int> 会跳过推导，实参走隐式转换（可能有损），T 同时决定形参和返回类型，所以第二次返回的是 double 4.0，只是 cout 默认不打印末尾的 .0。add(2, 2.5) 两个实参分别推出 int 和 double，冲突直接编译失败。想保留小数应写 add<double>(2, 2.5)。

## 高频追问

1. **第二个为什么显示 4？** —— 实际值是 4.0，ostream 默认格式省略末尾的 .0 和小数点，加 showpoint 才会显示。
2. **add(2, 2.5) 能编译吗？** —— 不能，T 被同时推成 int 和 double，模板实参推导失败。
3. **怎么让它打印 4.0？** —— cout << showpoint 或 fixed 配合 setprecision，输出格式问题而非计算问题。

## 易错点

- 以为 cout 默认带 .0，答 5 4.0 选 B
- 以为显式指定 <int> 不合法，答编译错误选 D
- 以为第二次返回 4.5，把 1.5+2.5 算错

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 34 类型转换与模板
