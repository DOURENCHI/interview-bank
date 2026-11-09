---
id: Q-0120
title: MRP 环网里，为什么 PROFINET 看门狗要设成 200ms 以上？
module: 01_project
sub: 西门子项目
priority: P0
difficulty: 3
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

**场景**：环网配好了，切换也正常，但一拔线 PLC 就报 IO 断连，环网像是白做了。

**问**：问题出在哪？

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

> 出在 PROFINET IO 的看门狗时间。看门狗是 PLC 判断「对方还活着」的超时阈值。
> MRP 的最大恢复时间就是 200 ms，如果看门狗设得比它短，切换这段时间 IO 已经判超时、连接被拆了——
> 环网还没切完，业务已经断。
> 所以规则是**看门狗 ≥ 环网恢复时间**，工程上取 200 ms 或更大。

## 讲深一层

本质是**两层超时的耦合**：

| 层 | 机制 | 量级 |
|---|---|---|
| 链路层 | MRP 检测并切换 | ≤200 ms |
| 应用层 | PROFINET 看门狗 | 可配，常见 100 ms 级 |

上层超时比下层恢复快，就出现「下层正在自愈，上层已经放弃」。这个规律可推广到所有重试/熔断/切换机制。

## 高频追问

1. **看门狗越大越好吗？** —— 不是，太大会让真故障反应迟钝。
2. **在哪配？** —— 设备属性里的更新时间 / 看门狗倍数。
3. **还有什么要注意？** —— 环网端口必须全双工、≥100 Mbps，否则切换时间不可控。

## 易错点

- ❌ 只配环网不看上层超时 —— 典型「配了但没用」
- ❌ 把看门狗当心跳间隔 —— 语义不同，它是超时阈值
- ✅ 记住 200 ms 这个数字和它跟 MRP 的关系

## 关联项目

- `西门子杯_面试口述稿与问答.pdf` §3 第三段 · 实施与配置

## 来源

PROFINET IO 看门狗机制

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
