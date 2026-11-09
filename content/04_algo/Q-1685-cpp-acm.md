---
id: Q-1685
title: 移动构造 的 ACM 输入输出怎么写？
module: 04_algo
sub: C++ ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: draft
source_type: self_doc
source_ref: 教学文档/C++实验台/C++考点实验台.html
verified_at: 2026-11-09
tags: [C++, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 C++ 程序对应的读入与输出写法是什么？

```cpp
class Buf {
public:
    int *data; size_t n;
    Buf(size_t n) : data(new int[n]), n(n) { cout << "new "; }
    Buf(const Buf &o) : data(new int[o.n]), n(o.n) { cout << "copy "; }
    Buf(Buf &&o) noexcept : data(o.data), n(o.n) { o.data = nullptr; o.n = 0; cout << "move "; }
    ~Buf() { delete[] data; }
};
int main() {
    Buf a(1000);
    Buf b = a;
    Buf c = std::move(a);
    cout << (a.data == nullptr) << ' ' << c.n;
}
```

输出样例：

```
new copy move 1 1000
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 26
