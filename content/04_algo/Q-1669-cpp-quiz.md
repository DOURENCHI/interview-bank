---
id: Q-1669
title: 这段 C++ 代码输出什么？（35 chrono 与时间 · 第 56 题）
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
cout << chrono::duration_cast<chrono::milliseconds>(
       chrono::seconds(2)).count();
```

- **A.** 2000
- **B.** 2
- **C.** 200
- **D.** 20

## 口述答案

答案是 **A. 2000**，实际输出 `2000`。

秒转毫秒是放大，不丢精度，2s = 2000ms；反方向（毫秒转秒）才可能截断。ROS2 里 rclcpp::Duration 与 std::chrono 互转时也要先统一单位。

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

`教学文档/C++实验台/C++考点实验台.html` · 35 chrono 与时间
