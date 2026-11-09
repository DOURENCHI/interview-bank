---
id: Q-0117
title: 介绍一下二维云台这个项目：硬件、软件栈、做到什么程度？
module: 01_project
sub: 二维云台
priority: P0
difficulty: 1
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

**背景**：基础版周期 3–6 周，难度自评 3/10，课程讲义 10 课已全部完成。

**硬件**：STM32F103C8T6（江协开发板）、SG90 舵机 × 2、双轴云台支架、外部 5V/2A 电源。

**软件**：Keil + 标准外设库（StdPeriph），不是 HAL。

**问**：技术栈怎么串的？核心难点在哪一层？

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

> 主控 STM32F103，标准库直接操作寄存器。执行是两个 SG90，做水平和俯仰。
> 软件分五步：定时器出 PWM 控单轴、封装角度接口并做限位、两轴独立控制、
> 串口接受角度指令、代码拆模块。
> 核心是**用定时器产生 50Hz PWM、靠脉宽定位**。难点不在代码量，
> 在供电和机械干涉这两件硬件上的事。

## 讲深一层

| 层 | 内容 | 关键点 |
|---|---|---|
| 主控 | STM32F103C8T6 | 标准外设库 |
| 执行 | SG90 × 2 | **180° 位置型** |
| 驱动 | 定时器 PWM | 50 Hz，0.5–2.5 ms |
| 交互 | 串口 | 接收目标角度 |
| 供电 | 外部 5V/2A | 不能从板子取电 |

## 高频追问

1. **为什么不用 HAL？** —— 项目定的是标准库，直接操作寄存器，对时序更可控。
2. **两轴联动吗？** —— 基础版独立控制，联动要坐标变换，属进阶。
3. **做到什么程度算完成？** —— 两轴按指令定位、有限位、连续运行不抖。

## 易错点

- ❌ 说成「摄像头云台」 —— 基础版没有视觉跟踪
- ❌ 把「独立控制」说成「协同控制」 —— 后者要解算
- ✅ 主动说规模和难度，别夸大

## 关联项目

- `方向与规划/项目/二维云台/二维云台项目_课程讲义.html` §1.1 项目基准、§1.2 项目路线（五个阶段）
