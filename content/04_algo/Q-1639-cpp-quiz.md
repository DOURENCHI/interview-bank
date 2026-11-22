---
id: Q-1639
title: 这段 C++ 代码输出什么？（20 模板 · 第 27 题）
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

模板实参推导不做隐式转换（只剥离顶层 const、数组和函数退化），两个实参推出不同类型时推导直接失败；显式写 mx<double> 后 3 被隐式转成 3.0，比较得 5.5。mx(3, 5.5) 因此编译错误。返回类型也是 T，若写 mx<int>(3.9, 4.1)，两个实参先截断成 3 和 4，返回 4。

## 高频追问

1. **第一次为什么 T 是 int？** —— 3 和 5 都是 int，两个实参推出同一类型，T 取 int，返回 5。
2. **第二次 3 怎么变成 3.0 的？** —— 显式指定 T=double 后推导被跳过，形参类型已定，3 走标准转换变成 3.0，比较得 5.5。
3. **mx(3, 5.5) 呢？** —— 一个推 int 一个推 double，冲突导致编译失败；需写 mx<double>(3, 5.5) 或 mx(3.0, 5.5)。

## 易错点

- 以为第二处也按 int 截断，答 5 5 选 B
- 以为显式指定实参非法，答编译错误选 D
- 忽略返回类型是 T，用 mx<int>(3.9,4.1) 期望 4.1

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 20 模板
