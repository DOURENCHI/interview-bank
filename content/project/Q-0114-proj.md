---
id: Q-0114
title: 分段计时加起来 7.21ms，端到端却是 7.94ms，差的 0.73ms 在哪？
module: project
sub: YOLO 部署
priority: P0
difficulty: 3
roles: [系统工程, 感知]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html
verified_at: 2026-11-09
tags: [项目深挖, YOLO, 图文]
auto: true
proj_seed: true
---

## 题目

**现象**：把预处理、推理、后处理分别计时相加得 7.21 ms，实测端到端 7.94 ms，差 0.73 ms。

**问**：这 0.73 ms 是什么？

<svg viewBox="0 0 860 330" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="ylat" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="330" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">端到端延迟演进（ms，本机实测）</text>
<text x="20" y="48" font-size="12" fill="#665c49">条越长越慢。红色那条是反例：套了两层封装，比原生还慢</text>

<text x="196" y="86" font-size="12" fill="#2d2a21" text-anchor="end">Python + PyTorch</text>
<rect x="206" y="71" width="560" height="22" rx="4" fill="#665c49" opacity="0.85"/>
<text x="774" y="86" font-size="12" font-weight="700" fill="#665c49">14.96</text>

<text x="196" y="118" font-size="12" fill="#2d2a21" text-anchor="end">Python + ORT</text>
<rect x="206" y="103" width="476" height="22" rx="4" fill="#1b5e8c" opacity="0.85"/>
<text x="690" y="118" font-size="12" font-weight="700" fill="#1b5e8c">12.71</text>

<text x="196" y="150" font-size="12" fill="#2d2a21" text-anchor="end">Python 套框架封装</text>
<rect x="206" y="135" width="474" height="22" rx="4" fill="#a63a2e" opacity="0.85"/>
<text x="688" y="150" font-size="12" font-weight="700" fill="#a63a2e">12.65 反例</text>

<text x="196" y="182" font-size="12" fill="#2d2a21" text-anchor="end">C++ + CUDA EP</text>
<rect x="206" y="167" width="498" height="22" rx="4" fill="#12666e" opacity="0.85"/>
<text x="712" y="182" font-size="12" font-weight="700" fill="#12666e">13.31</text>

<text x="196" y="214" font-size="12" fill="#2d2a21" text-anchor="end">C++ + TensorRT EP</text>
<rect x="206" y="199" width="297" height="22" rx="4" fill="#2e6b3e" opacity="0.85"/>
<text x="511" y="214" font-size="12" font-weight="700" fill="#2e6b3e">7.94</text>

<line x1="206" y1="70" x2="206" y2="228" stroke="#dbcba5" stroke-width="1"/>
<text x="20" y="262" font-size="12" fill="#2d2a21">纯推理 vs 端到端要分开看：纯 TensorRT 只要 1.97 ms，但端到端 7.94 ms ——</text>
<text x="20" y="280" font-size="12" fill="#2d2a21">中间的 6 ms 是采集、预处理、后处理、拷贝，优化推理只能解决其中一部分。</text>
<text x="20" y="306" font-size="11" fill="#a63a2e">纪律：不同次测量之间只比相对值，不跨口径比绝对值。</text>
</svg>

## 口述答案

> 主要是**段与段之间的开销没被计入**：每轮约 7 MB 的内存分配与释放、
> 缓存失效、函数调用与数据传递的间隙。
> 分段计时只统计每段内部耗时，段间是空的。
> 后来做了 buffer 复用（把每帧都申请释放的缓冲改成复用），这部分就降下来了。

## 讲深一层

分段计时为什么天然偏小：

| 漏算项 | 说明 |
|---|---|
| 分配/释放 | 每帧 malloc/free 的开销 |
| 缓存影响 | 上段写的数据下段要重新载入 |
| 同步开销 | 线程间等待 |
| 计时粒度 | 打点本身的精度 |

原则：**分段用来看占比，端到端用来对外报数**，两者不能互相替代。

## 高频追问

1. **怎么做 buffer 复用？** —— 预分配固定缓冲，每帧覆盖写。
2. **复用的风险？** —— 多线程下要保证不冲突。
3. **怎么验证就是这部分？** —— 做完复用后重测，差值缩小就对上了。

## 易错点

- ❌ 拿分段相加当端到端
- ❌ 忽略分配释放的开销
- ✅ 两个数字都报，并解释差异

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §A3 踩过的坑一览（第 15 条）
