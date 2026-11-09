---
id: Q-0116
title: DHT11 的驱动难点在哪？为什么必须关中断？
module: 01_project
sub: 本科毕设·4G 测温
priority: P0
difficulty: 3
roles: [系统工程, 感知]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/毕设/本科毕设_面试口述稿与专业问答_完整版.pdf
verified_at: 2026-11-09
tags: [项目深挖, 毕设, 图文]
auto: true
proj_seed: true
---

## 题目

**背景**：DHT11 一次传 40 位，每位用高电平宽度区分 0 和 1（约 26 µs 为 0，约 70 µs 为 1）。

**问**：难点在哪？关中断是在防什么？

<svg viewBox="0 0 860 240" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="dpar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="240" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">本科毕设：四层链路</text>
<text x="20" y="48" font-size="12" fill="#665c49">题目的落脚点是「链路可行性验证」，不是「精度达标的测温仪」</text>

<rect x="20" y="74" width="140" height="64" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="90" y="98" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">DHT11</text>
<text x="90" y="116" font-size="10" fill="#2d2a21" text-anchor="middle">单总线 40 位</text>
<text x="90" y="130" font-size="10" fill="#665c49" text-anchor="middle">0–50℃ ±2℃</text>

<rect x="184" y="74" width="140" height="64" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="254" y="98" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">STM32F103</text>
<text x="254" y="116" font-size="10" fill="#2d2a21" text-anchor="middle">寄存器配 GPIO</text>
<text x="254" y="130" font-size="10" fill="#665c49" text-anchor="middle">关中断读脉宽</text>

<rect x="348" y="74" width="140" height="64" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="418" y="98" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">RS485</text>
<text x="418" y="116" font-size="10" fill="#2d2a21" text-anchor="middle">差分传输</text>
<text x="418" y="130" font-size="10" fill="#665c49" text-anchor="middle">抗共模干扰</text>

<rect x="512" y="74" width="140" height="64" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="582" y="98" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">4G DTU</text>
<text x="582" y="116" font-size="10" fill="#2d2a21" text-anchor="middle">Cat.1 透传</text>
<text x="582" y="130" font-size="10" fill="#665c49" text-anchor="middle">AT 指令 + 超时</text>

<rect x="676" y="74" width="140" height="64" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="746" y="98" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">云端</text>
<text x="746" y="116" font-size="10" fill="#2d2a21" text-anchor="middle">曲线与展示</text>
<text x="746" y="130" font-size="10" fill="#665c49" text-anchor="middle">注册包判据</text>

<line x1="160" y1="106" x2="180" y2="106" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#dpar)"/>
<line x1="324" y1="106" x2="344" y2="106" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#dpar)"/>
<line x1="488" y1="106" x2="508" y2="106" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#dpar)"/>
<line x1="652" y1="106" x2="672" y2="106" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#dpar)"/>
<rect x="348" y="160" width="304" height="50" rx="8" fill="#faede8" stroke="#a63a2e"/>
<text x="500" y="180" font-size="11" fill="#a63a2e" text-anchor="middle">已知短板：量程 0–50℃，夏季沥青路面可达 60℃+</text>
<text x="500" y="198" font-size="11" fill="#a63a2e" text-anchor="middle">这不是精度问题，是「测不到」</text>
</svg>

## 口述答案

> 难点不是读 GPIO，是**准确测出高电平持续了多久**。
> 所以三件事决定驱动稳不稳：微秒级延时精度、GPIO 在输入输出间切换的时机、中断会不会打断采样。
> 关中断是防第三件：一次中断进出加服务程序，足以让脉宽判错，而校验和只能告诉你错了，
> 不能告诉你是哪一位错的——整帧作废重读。

## 讲深一层

时序：

| 阶段 | 时长 |
|---|---|
| 主机起始 | 拉低 ≥18 ms |
| 主机释放 | 20–40 µs，切输入 |
| 从机响应 | 80 µs 低 + 80 µs 高 |
| 数据位 ×40 | 每位置 50 µs 低电平起始 |

数据 = 5 字节：湿度整数/小数、温度整数/小数、校验和。DHT11 小数位恒为 0，分辨率 1℃ / 1%RH。

## 高频追问

1. **校验和怎么算？** —— 前 4 字节相加取低 8 位，与第 5 字节比。
2. **为什么不能只靠校验和？** —— 它只能发现错，定位不了错在哪一位。
3. **官方规格是多少？** —— 0–50℃ ±2℃、20–90%RH ±5%RH、响应 6 s 量级。

## 易错点

- ❌ 说「精度 ±0.5℃」 —— 实际是 ±2℃
- ❌ 说「就是延时读电平」 —— 完全没体现难点
- ✅ 落到「延时精度 / 方向切换 / 中断干扰」三件事

## 关联项目

- `本科毕设_面试口述稿与专业问答_完整版.pdf` §5.1、§5.4

## 来源

本人本科毕设 + DHT11 数据手册

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
