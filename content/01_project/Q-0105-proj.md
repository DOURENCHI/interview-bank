---
id: Q-0105
title: 延迟你是怎么测的？为什么报 p99 而不是平均值？
module: 01_project
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

**实测**（1280×720，两轮 × 1000 帧）：

| 吞吐 | 中位 | p99 | 内存净增 |
|---|---|---|---|
| 101.6 / 100.5 FPS | 9.90 / 9.82 ms | **13.25 / 14.11 ms** | +4 ~ +6 MB |

**问**：中位 9.8 ms 看起来很稳，为什么还要看 p99？具体怎么测才不算错？

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

> 因为实时系统怕的是**抖动**。中位 9.8 ms 说明大部分帧稳，但 p99 到 14 ms 意味着
> 每 100 帧有 1 帧慢 40%——在 30 FPS 链路上就是卡顿或丢帧。
> 所以我报三个数：中位、p99、内存净增。跑两轮 1000 帧是为了看稳定性，
> 短时间测不出内存泄漏和热降频。

## 讲深一层

| 项 | 做法 | 原因 |
|---|---|---|
| 时钟 | `steady_clock` | 单调，不受系统时间调整影响 |
| 同步 | 计时前先 synchronize | GPU 异步，不同步测到的是提交时间 |
| 预热 | 丢弃前几十帧 | 首次有初始化开销 |
| 样本量 | 千帧级 | 少了看不出 p99 |
| 环境 | 记录温度/频率 | 笔记本会热降频 |

## 高频追问

1. **p99 高怎么优化？** —— 找长尾：内存分配、锁、频率波动。
2. **为什么看内存净增？** —— 每帧泄漏一点，几小时就 OOM。
3. **两轮差 0.86 ms 说明什么？** —— 可能热降频或后台干扰，本身就是发现。

## 易错点

- ❌ 只报平均 FPS —— 掩盖长尾
- ❌ 不 synchronize 就计时 —— 测的是提交时间
- ❌ 用 `system_clock` —— 系统时间一跳就错

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §视频流与长时间稳定性
