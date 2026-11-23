---
id: Q-0139
title: 介绍一下西门子杯这个项目，你具体负责哪部分？
module: project
sub: 西门子项目
priority: P0
difficulty: 2
roles: [系统工程]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/西门子/西门子杯_面试口述稿与问答.pdf
verified_at: 2026-11-09
tags: [项目深挖, 工业网络, MRP, 图文]
auto: true
proj_seed: true
---

## 题目

**赛制**：中国智能制造挑战赛 · 信息化网络化方向，华东赛区一等奖。
组委会以甲方身份发布智能工厂需求，参赛队以乙方身份出方案、进场实施、答辩。
决赛满分 120 = 上机 100 + 答辩 20。

**工具链**：TIA Portal（博图）+ Wireshark + PRONETA，控制器 S7-1200。

**问**：30 秒介绍，说清赛制、你的角色、你亲手做了什么。

<svg viewBox="0 0 860 300" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="mar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="300" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">MRP 环网：正常态与故障态</text>
<text x="20" y="48" font-size="12" fill="#665c49">IEC 62439-2 · 二层 · 正常时阻塞一个环口防广播风暴，故障时打开</text>
<text x="210" y="76" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">正常态</text>
<text x="650" y="76" font-size="13" font-weight="700" fill="#a63a2e" text-anchor="middle">故障态</text>
<rect x="30" y="88" width="360" height="148" rx="10" fill="#f3e9d2" stroke="#dbcba5"/>
<rect x="470" y="88" width="360" height="148" rx="10" fill="#f3e9d2" stroke="#dbcba5"/>
<circle cx="120" cy="120" r="14" fill="#fffcf3" stroke="#a63a2e" stroke-width="2"/><text x="120" y="124" font-size="11" font-weight="700" fill="#a63a2e" text-anchor="middle">M</text><circle cx="280" cy="120" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/><text x="280" y="124" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text><circle cx="280" cy="200" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/><text x="280" y="204" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text><circle cx="120" cy="200" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/><text x="120" y="204" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text><line x1="280" y1="134" x2="280" y2="186" stroke="#1b5e8c" stroke-width="1.8"/><line x1="266" y1="200" x2="134" y2="200" stroke="#1b5e8c" stroke-width="1.8"/><line x1="134" y1="120" x2="266" y2="120" stroke="#1b5e8c" stroke-width="1.8"/><line x1="120" y1="186" x2="120" y2="134" stroke="#a63a2e" stroke-width="1.8" stroke-dasharray="5 4"/><text x="150" y="164" font-size="11" fill="#a63a2e" text-anchor="middle">阻塞</text><circle cx="560" cy="120" r="14" fill="#fffcf3" stroke="#a63a2e" stroke-width="2"/><text x="560" y="124" font-size="11" font-weight="700" fill="#a63a2e" text-anchor="middle">M</text><circle cx="720" cy="120" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/><text x="720" y="124" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text><circle cx="720" cy="200" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/><text x="720" y="204" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text><circle cx="560" cy="200" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/><text x="560" y="204" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text><line x1="720" y1="134" x2="720" y2="186" stroke="#1b5e8c" stroke-width="1.8"/><line x1="706" y1="200" x2="574" y2="200" stroke="#1b5e8c" stroke-width="1.8"/><line x1="574" y1="120" x2="630" y2="120" stroke="#1b5e8c" stroke-width="1.8"/><line x1="660" y1="120" x2="706" y2="120" stroke="#1b5e8c" stroke-width="1.8"/><line x1="633" y1="110" x2="657" y2="130" stroke="#a63a2e" stroke-width="2.4"/><line x1="633" y1="130" x2="657" y2="110" stroke="#a63a2e" stroke-width="2.4"/><line x1="560" y1="186" x2="560" y2="134" stroke="#1b5e8c" stroke-width="1.8"/>
<text x="210" y="258" font-size="11" fill="#665c49" text-anchor="middle">左边被阻塞，环逻辑上是线型</text>
<text x="650" y="258" font-size="11" fill="#a63a2e" text-anchor="middle">上边断开，被阻塞的左边打开，绕行</text>
</svg>

## 口述答案

> 信息化网络化方向，华东赛区一等奖，我是团队负责人，答辩由我讲。
> 赛题是给智能工厂做工控网络的方案设计加实施——从需求分析、网络结构设计、设备选型，
> 到现场配置调试和答辩。
> 我主要负责 PLC 和工业交换机的配置，核心是用交换机做 MRP 环网冗余，
> 保证单点链路故障不影响产线通信，并做了故障注入验证。

「我主要负责 PLC 和工业交换机」这句必须说——团队项目里主动划边界反而可信。

## 讲深一层

| 阶段 | 内容 |
|---|---|
| 方案设计 | 厂区分析、需求分析、结构设计（要说明理由）、信息安全策略、设备选型 |
| 现场实施 | 交换机/无线/安全模块配置、PLC 配置、调试与故障诊断、抓包、验收 |
| 答辩 | 重点讲「为什么这么设计」，不是「配了什么」 |

## 高频追问

1. **几个人怎么分工？** —— 三人，我负责 PLC 与交换机，另两人做方案文档与可视化。
2. **这段经历对现在岗位有什么用？** —— 工业以太网、环网冗余、实时性约束，和车载以太网、机器人内部通信是同一类问题。
3. **答辩讲什么？** —— 为什么环网、为什么 MRP 不用生成树、为什么接入层用星型。

## 易错点

- ❌ 只讲「我们配了环网」 —— 像照着教程做
- ❌ 把团队成果全说成自己的 —— 一问细节就露
- ✅ 主动划边界，再说核心技术点

## 关联项目

- `方向与规划/项目/西门子/西门子杯_面试口述稿与问答.pdf` §2 30 秒版口述、§3 三分钟版口述
