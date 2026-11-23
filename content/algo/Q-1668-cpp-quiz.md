---
id: Q-1668
title: 这段 C++ 代码输出什么？（35 chrono 与时间 · 第 56 题）
module: algo
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

秒转毫秒是精度放大、无损，duration_cast 只是把 Rep 乘 1000。只有无损方向才允许隐式转换，所以 seconds 能直接赋给 milliseconds 变量，反向必须显式 cast 以防静默丢精度。超大跨度要注意溢出：hours 转 nanoseconds 会到 3.6e12 量级，接近 int64 上限。

## 高频追问

1. **为什么是 2000？** —— 1 秒等于 1000 毫秒，2 秒乘 1000 得 2000，count() 给毫秒数。
2. **能省掉 duration_cast 吗？** —— 可以，seconds → milliseconds 是无损放大，支持隐式转换；反过来必须写 cast。
3. **有什么溢出风险？** —— hours 转 nanoseconds 乘以 3.6e12，次数一多就超出 int64；长跨度建议用 double 精度或换单位。

## 易错点

- 忘记放大，答 2 选 B
- 少乘一个 10，答 200 选 C
- 用 int32 存毫秒时间戳，约 24.8 天就溢出成负数

## 关联项目

无（语言基础题）。

## 来源

`教学文档/C++实验台/C++考点实验台.html` · 35 chrono 与时间
