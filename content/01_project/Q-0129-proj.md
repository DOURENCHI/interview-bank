---
id: Q-0129
title: 介绍一下你的本科毕设，四层链路分别是什么？
module: 01_project
sub: 本科毕设·4G 测温
priority: P0
difficulty: 2
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

**背景**：题目「基于 4G 通信的道路温度获取方法」，落脚点是**链路可行性验证**，
不是精度达标的测温仪。

**问**：四层分别是什么？你亲手做了什么？

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

> 一句话：把路面温度采上来、用 4G 发到云端、能在网页上看曲线。
> 四层：DHT11 贴地测温、STM32F103 主控、RS485 接 4G Cat.1 DTU、云端展示。
> 我的工作量不在「采一个温度」，而在把链路打通并可控——
> DHT11 单总线时序严，我用寄存器配 GPIO 做方向切换、采样时关中断；
> DTU 那层封了 AT 指令收发函数，必须匹配到期望应答才算成功。

## 讲深一层

| 层 | 器件/协议 | 关键点 |
|---|---|---|
| 测量 | DHT11 | 单总线，40 位，脉宽编码 |
| 主控 | STM32F103 | 寄存器配 GPIO、微秒延时、关中断 |
| 传输 | RS485 | 差分，抗共模干扰，可长线 |
| 通信 | 4G Cat.1 DTU | AT 指令 + 超时判据 + 注册包 |
| 应用 | 云端 | 曲线、时间戳依赖 RTC |

## 高频追问

1. **为什么用 RS485 不用 TTL？** —— 差分抗干扰，距离可达千米级。
2. **Cat.1 和 NB-IoT 怎么选？** —— Cat.1 约 5/10 Mbps，适合小数据量要实时；NB-IoT 百 kbps 级适合抄表。
3. **怎么确认连上云了？** —— DTU 注册后云端回固定注册包 `0xAF 0x20 0x7E 0x00 0x01 0x5A`。

## 易错点

- ❌ 说「DHT11 是红外测温」 —— 论文里笔误过，面试说错是硬伤
- ❌ 只讲功能不讲难点 —— 像课程实验
- ✅ 带出「时序严 + 超时判据 + 量程短板」三件真事

## 关联项目

- `方向与规划/项目/毕设/本科毕设_面试口述稿与专业问答_完整版.pdf` §5 四个模块的技术细节
