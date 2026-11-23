---
id: Q-0118
title: 舵机凭什么能「转到指定角度」？和普通直流电机差在哪？
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

**问**：同样是电机，为什么直流电机只能调速、舵机能定位？

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

> 因为舵机内部是一个**闭环系统**：直流电机 + 减速齿轮组 + 电位器 + 控制电路。
> 电位器测出当前角度，控制电路把它和目标脉宽对应的角度比较，差多少就驱动电机转多少，到位就停。
> 所以从外面看是「给脉宽、出角度」，内部其实在闭环。
> 而普通直流电机没有位置反馈，只能靠电压调转速。

## 讲深一层

舵机内部四件：

| 部件 | 作用 |
|---|---|
| 直流电机 | 提供动力 |
| 减速齿轮组 | 降速增扭 |
| 电位器 | 角度反馈 |
| 控制电路 | 比较目标与实际，驱动电机 |

这也解释了两件事：为什么堵转时电流大（一直想转但转不动）、
为什么连续旋转型要拆掉限位（改成速度控制）。

## 高频追问

1. **电位器坏了会怎样？** —— 乱转或不动，因为它以为位置一直不对。
2. **死区是什么？** —— 目标与实际差小于死区就不动，防止来回抖动。
3. **为什么力矩小？** —— 塑料齿轮 + 小电机，堵转扭矩只有 1.8 kg·cm 级。

## 易错点

- ❌ 说「舵机就是电机」 —— 忽略内部闭环
- ❌ 说「舵机是开环」 —— 舵机内部闭环，MCU 与舵机之间才是开环
- ✅ 分清两个层次

## 关联项目

- `方向与规划/项目/二维云台/二维云台项目_课程讲义.html` §1.2 舵机凭什么能「转到指定角度」
