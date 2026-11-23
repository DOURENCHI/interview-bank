---
id: Q-0121
title: 定时器的 PSC 和 ARR 两个数是怎么推出来的？
module: project
sub: 二维云台
priority: P0
difficulty: 3
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

**目标**：产生 50 Hz PWM，高电平 0.5–2.5 ms 可调，主频 72 MHz。

**问**：预分频 PSC 和自动重装 ARR 各取多少？为什么这么取？

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

> 两步推导。先定计数单位：72 MHz 分频到 1 MHz，PSC = 72 − 1 = 71，
> 每个计数就是 1 µs。
> 再定周期：20 ms = 20000 µs，所以 ARR = 20000 − 1 = 19999。
> 好处是**比较值 CCR 直接就是微秒数**——写 1500 就对应 1.5 ms，不用心算换算。

## 讲深一层

| 参数 | 公式 | 值 |
|---|---|---|
| PSC | f_clk / f_cnt − 1 | 71 |
| ARR | T × f_cnt − 1 | 19999 |
| CCR | 脉宽(µs) | 500–2500 |

都减 1 是因为计数器从 0 开始数，数到 ARR 共 ARR+1 个状态。

## 高频追问

1. **为什么分频到 1 MHz？** —— 1 µs 分辨率刚好够，再细没必要。
2. **单位选错会怎样？** —— 周期和脉宽同时错，舵机乱转。
3. **要更高分辨率？** —— 用 0.5 µs 单位（PSC=35），SG90 用不上。

## 易错点

- ❌ 忘了减 1
- ❌ 把 ARR 当成毫秒 —— 单位是计数次数
- ✅ 记住「PSC 定单位、ARR 定周期、CCR 定脉宽」

## 关联项目

- `方向与规划/项目/二维云台/二维云台项目_课程讲义.html` §2.3 三个数字的推导（本课最核心）
