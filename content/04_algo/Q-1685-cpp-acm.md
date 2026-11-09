---
id: Q-1685
title: shared_ptr 引用计数 的 ACM 输入输出怎么写？
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
struct Obj { ~Obj() { cout << "delete\n"; } };
int main() {
    auto a = make_shared<Obj>();
    cout << a.use_count() << '\n';
    {
        auto b = a;
        cout << a.use_count() << '\n';
    }
    cout << a.use_count() << '\n';
    a.reset();
    cout << "end\n";
}
```

输出样例：

```
1
2
1
delete
end
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

`教学文档/C++实验台/C++考点实验台.html` · 25
