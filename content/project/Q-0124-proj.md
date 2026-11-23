---
id: Q-0124
title: 平滑转动为什么要「慢慢走」？直接跳到目标角度有什么问题？
module: project
sub: 二维云台
priority: P0
difficulty: 2
roles: [系统工程, 感知]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/二维云台/二维云台项目_课程讲义.html
verified_at: 2026-11-09
tags: [项目深挖, 嵌入式, 图文]
auto: true
proj_seed: true
---

## 题目

**场景**：让云台从 30° 转到 120°，直接写一次 CCR 会「啪」地弹过去。

**问**：为什么要分成很多小步？代价是什么？

<svg viewBox="0 0 860 250" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="gmar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="250" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">二维云台：开环控制，没有反馈</text>
<text x="20" y="48" font-size="12" fill="#665c49">SG90 舵机按脉宽定位，不回读角度 —— 这是它和闭环云台的根本差别</text>

<rect x="20" y="78" width="130" height="58" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="85" y="102" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">STM32F103</text>
<text x="85" y="120" font-size="11" fill="#665c49" text-anchor="middle">定时器 PWM</text>

<rect x="186" y="78" width="130" height="58" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="251" y="102" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">PWM 50Hz</text>
<text x="251" y="120" font-size="11" fill="#665c49" text-anchor="middle">0.5–2.5ms</text>

<rect x="352" y="78" width="130" height="58" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="417" y="102" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">SG90 舵机</text>
<text x="417" y="120" font-size="11" fill="#665c49" text-anchor="middle">180° 位置型</text>

<rect x="518" y="78" width="130" height="58" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="583" y="102" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">机械支架</text>
<text x="583" y="120" font-size="11" fill="#665c49" text-anchor="middle">水平 + 俯仰</text>

<rect x="684" y="78" width="130" height="58" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="749" y="102" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">限位保护</text>
<text x="749" y="120" font-size="11" fill="#665c49" text-anchor="middle">软件钳位</text>

<line x1="150" y1="107" x2="182" y2="107" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#gmar)"/>
<line x1="316" y1="107" x2="348" y2="107" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#gmar)"/>
<line x1="482" y1="107" x2="514" y2="107" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#gmar)"/>
<line x1="648" y1="107" x2="680" y2="107" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#gmar)"/>
<path d="M749,136 L749,170 L85,170 L85,138" fill="none" stroke="#a63a2e"
      stroke-width="1.4" stroke-dasharray="5 4"/>
<text x="417" y="188" font-size="11" fill="#a63a2e" text-anchor="middle">
缺反馈：角度靠脉宽推算，堵转/机械干涉都不自知</text>
<text x="20" y="216" font-size="12" fill="#2d2a21">所以两个必做：</text>
<text x="20" y="234" font-size="12" fill="#2d2a21">· 软件限位（钳位到 0–180° 内，避免打齿） · 独立 5V/2A 供电（舵机启动电流会拉垮板子供电）</text>
</svg>

## 口述答案

> 三个原因：**电流冲击**（一步到位时舵机全力加速，瞬时电流大，可能拉垮供电）、
> **机械冲击**（齿轮受力大，塑料齿容易扫齿）、**视觉抖动**（如果是摄像头会晃）。
> 做法是分步插值，每几毫秒走 1–2 度。代价是响应变慢，所以要按场景调速度。

## 讲深一层

| 方式 | 响应 | 冲击 | 适用 |
|---|---|---|---|
| 一步到位 | 最快 | 大 | 轻载、不心疼齿轮 |
| 线性插值 | 可调 | 小 | 通用 |
| 梯形/S 曲线 | 慢 | 最小 | 重载、要平稳 |

实现放在定时器中断里做增量，或主循环按时间片推。

## 高频追问

1. **步长怎么定？** —— 按允许最大角速度算，比如 60°/s 就是每 10 ms 走 0.6°。
2. **会丢步吗？** —— 开环下会，所以不能走太快。
3. **和 PWM 频率冲突吗？** —— 不冲突，PWM 是 50 Hz，插值更新可以更高频。

## 易错点

- ❌ 只说「平滑好看」
- ❌ 步长写死，不随距离调整
- ✅ 从电流、机械、视觉三个角度解释

## 关联项目

- `方向与规划/项目/二维云台/二维云台项目_课程讲义.html` §3.8 平滑转动：为什么要慢慢走
