---
id: Q-0128
title: 程序下载失败，你怎么排查？先接线还是先看配置？
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

**场景**：Keil 点下载，报找不到设备或连接失败。

**问**：排查顺序是什么？最容易忽略的是哪一步？

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

> 顺序是**先接线再配置**：先确认 SWD 的 GND、SWCLK、SWDIO 三根线接对、
> 板子供电正常，再看 Keil 里的调试器型号和端口有没有选错。
> 最容易忽略的是 **BOOT0 状态**——如果 BOOT0 被拉高，芯片从系统存储器启动，
> 程序当然跑不起来，看起来像「下载成功了但没运行」。
> 另外下载器被别的程序占用也会连不上。

## 讲深一层

常见原因对照：

| 现象 | 原因 |
|---|---|
| 找不到设备 | 接线错、没供电、调试器没识别 |
| 下载成功但不运行 | BOOT0 拉高、复位电路异常 |
| 时好时坏 | 线太长、接触不良、电源不稳 |
| 被占用 | 另一个 IDE/调试会话没关 |

## 高频追问

1. **SWD 最少几根线？** —— GND、SWCLK、SWDIO 三根，加上 VCC 参考。
2. **BOOT0 正常应该怎样？** —— 接地，从 Flash 启动。
3. **串口下载和 SWD 区别？** —— 串口要进 bootloader（BOOT0 拉高），慢且不能在线调试。

## 易错点

- ❌ 一上来就改 Keil 配置
- ❌ 忽略 BOOT0
- ✅ 硬件优先、配置其次，这是嵌入式排查的基本顺序

## 关联项目

- `方向与规划/项目/二维云台/二维云台项目_课程讲义.html` §0.6 下载：先接线，再配置、§0.7 下载失败排查表
