---
id: Q-1686
title: 综合实例：成绩管理（核心部分） 的 ACM 输入输出怎么写？
module: 04_algo
sub: C++ ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: indexed
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
class Student {
    string name;
    vector<int> scores;
public:
    Student(string n, vector<int> s) : name(move(n)), scores(move(s)) {}
    int total() const { return accumulate(scores.begin(), scores.end(), 0); }
    const string &getName() const { return name; }
    friend ostream &operator<<(ostream &os, const Student &s) {
        os << left << setw(8) << s.name;
        for (int x : s.scores) os << right << setw(5) << x;
        return os << right << setw(7) << s.total();
    }
};
int main() {
    vector<Student> all;
    string name; int a, b, c;
    while (cin >> name >> a >> b >> c) all.emplace_back(name, vector<int>{a, b, c});
    sort(all.begin(), all.end(), [](const Student &x, const Student &y) {
        if (x.total() != y.total()) return x.total() > y.total();
        return x.getName() < y.getName();
    });
    int rank = 1;
    for (const auto &s : all) cout << rank++ << ". " << s << '\n';
}
```

输入样例：

```
Alice 85 92 78
Bob 90 88 92
Carol 78 85 80
Dave 92 80 83
```

输出样例：

```
1. Bob        90   88   92    270
2. Alice      85   92   78    255
3. Dave       92   80   83    255
4. Carol      78   85   80    243
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

`教学文档/C++实验台/C++考点实验台.html` · 27
