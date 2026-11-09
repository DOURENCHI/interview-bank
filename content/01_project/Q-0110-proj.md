---
id: Q-0110
title: SG90 怎么用 PWM 控制角度？50Hz 这个频率是怎么定的？
module: 01_project
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

**问**：脉宽和角度的对应关系是什么？为什么是 50 Hz？

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

> SG90 是位置型舵机，控制信号是周期 20 ms（50 Hz）的 PWM，高电平宽度决定角度：
> 0.5 ms 对应 0°，2.5 ms 对应 180°，中间线性对应。
> 50 Hz 不是随便定的，是舵机内部的电位器反馈回路需要的刷新周期——
> 太快没有必要，太慢会抖动。用 STM32 的定时器配 20 ms 周期、改比较值就能改脉宽。

## 讲深一层

定时器参数怎么算（以 72 MHz 主频为例）：

| 参数 | 取值 | 说明 |
|---|---|---|
| 预分频 PSC | 71 | 72 MHz / 72 = 1 MHz，即计数周期 1 µs |
| 自动重装 ARR | 19999 | 20000 × 1 µs = 20 ms |
| 比较值 CCR | 500–2500 | 直接对应 0.5–2.5 ms |

好处：**CCR 的数值就是微秒数**，写起来直观。

## 高频追问

1. **为什么是 0.5–2.5 ms 而不是 1–2 ms？** —— 不同型号略有差异，SG90 常见 0.5–2.5 ms 对应 0–180°。
2. **用软件延时产生 PWM 行不行？** —— 行但抖，且占 CPU。定时器硬件输出才稳。
3. **多路舵机怎么办？** —— 同一路定时器的不同通道，共用周期、各自比较值。

## 易错点

- ❌ 说是「调频率控制角度」 —— 频率固定，调的是**占空比/脉宽**
- ❌ PSC/ARR 算错一位 —— 角度整体偏移
- ✅ 说清「1 µs 计数单位让 CCR 等于微秒数」这个技巧

## 关联项目

- `二维云台项目_课程讲义.html` 第 2 课 · 单轴舵机控制

## 来源

本人项目 + SG90 数据手册

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
