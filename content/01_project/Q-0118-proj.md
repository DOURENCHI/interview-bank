---
id: Q-0118
title: 介绍一下西门子杯这个项目，你具体负责哪部分？
module: 01_project
sub: 西门子项目
priority: P0
difficulty: 2
roles: [系统工程, 感知]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/西门子/西门子杯_面试口述稿与问答.pdf
verified_at: 2026-11-09
tags: [项目深挖, 工业网络, 图文]
auto: true
proj_seed: true
---

## 题目

**背景**：中国智能制造挑战赛 · 信息化网络化方向，华东赛区一等奖，团队负责人。

**赛制**：组委会以甲方身份发布智能工厂建设需求，参赛队以乙方身份出方案、进场实施、最后答辩。
决赛满分 120 = 上机 100 + 答辩 20。

**问**：30 秒介绍，说清赛制、你的角色、你亲手做了什么。

<svg viewBox="0 0 860 300" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="mar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="300" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">MRP 环网：正常态与故障态</text>
<text x="20" y="48" font-size="12" fill="#665c49">IEC 62439-2 · 二层 · 正常时阻塞一个环口防广播风暴，故障时打开</text>
<text x="150" y="76" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">正常态</text>
<text x="640" y="76" font-size="13" font-weight="700" fill="#a63a2e" text-anchor="middle">故障态</text>
<rect x="30" y="90" width="360" height="150" rx="10" fill="#f3e9d2" stroke="#dbcba5"/>
<rect x="470" y="90" width="360" height="150" rx="10" fill="#f3e9d2" stroke="#dbcba5"/>

<circle cx="90" cy="130" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="90" y="134" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">M</text>

<circle cx="210" cy="130" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="210" y="134" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text>

<circle cx="330" cy="130" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="330" y="134" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text>

<circle cx="210" cy="210" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="210" y="214" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text>

<circle cx="330" cy="210" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="330" y="214" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text>

<circle cx="530" cy="130" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="530" y="134" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">M</text>

<circle cx="650" cy="130" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="650" y="134" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text>

<circle cx="770" cy="130" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="770" y="134" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text>

<circle cx="650" cy="210" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="650" y="214" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text>

<circle cx="770" cy="210" r="14" fill="#fffcf3" stroke="#1b5e8c" stroke-width="2"/>
<text x="770" y="214" font-size="11" font-weight="700" fill="#1b5e8c" text-anchor="middle">C</text>

<line x1="104" y1="130" x2="196" y2="130" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="224" y1="130" x2="316" y2="130" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="330" y1="144" x2="330" y2="196" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="316" y1="210" x2="224" y2="210" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="210" y1="196" x2="210" y2="144" stroke="#dbcba5" stroke-width="1.6" stroke-dasharray="4 3"/>
<text x="272" y="172" font-size="11" fill="#a63a2e" text-anchor="middle">阻塞</text>
<line x1="544" y1="130" x2="636" y2="130" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="664" y1="130" x2="756" y2="130" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="770" y1="144" x2="770" y2="196" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="756" y1="210" x2="664" y2="210" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="636" y1="210" x2="544" y2="210" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="650" y1="196" x2="650" y2="144" stroke="#1b5e8c" stroke-width="1.6"/>
<line x1="210" y1="130" x2="210" y2="130" stroke="#a63a2e"/>
<text x="150" y="262" font-size="11" fill="#665c49" text-anchor="middle">环逻辑上是线型，数据走单一路径</text>
<text x="650" y="262" font-size="11" fill="#a63a2e" text-anchor="middle">断一处，被阻塞的口打开，反向绕通</text>
</svg>

## 口述答案

> 信息化网络化方向，华东赛区一等奖，我是团队负责人，答辩由我讲。
> 赛题是给智能工厂做工控网络的方案设计加实施——从需求分析、网络结构设计、设备选型，
> 到现场配置调试和答辩。
> 我主要负责 PLC 和工业交换机的配置，核心是用交换机构环网冗余，
> 保证单点链路故障不影响产线通信，并做了故障注入验证。

「我主要负责 PLC 和工业交换机」这句必须说——团队项目里主动划边界反而显得可信。

## 讲深一层

| 阶段 | 内容 |
|---|---|
| 方案设计 | 厂区分析、需求分析、结构设计（要说明理由）、信息安全策略、设备选型 |
| 现场实施 | 交换机/无线/安全模块配置、PLC 配置、调试与故障诊断、抓包、验收 |
| 方案答辩 | 重点讲「为什么这么设计」，不是「配了什么」 |

工具链：TIA Portal + Wireshark + PRONETA，控制器 S7-1200。

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

## 来源

本人竞赛经历（2021）

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
