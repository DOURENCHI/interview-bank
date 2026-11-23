---
id: Q-0140
title: 你们用的什么冗余协议？恢复时间多少？有哪几档？
module: project
sub: 西门子项目
priority: P0
difficulty: 3
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

**问**：协议名、标准号、恢复时间是硬指标，必须一次答对。

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

> **MRP**，Media Redundancy Protocol，标准号 **IEC 62439-2**，是 PROFINET 里定义的环网协议。
> 恢复时间按档位设置，有 **10 / 30 / 200 / 500 毫秒**四档，我们用默认的 200 毫秒档。
> 它工作在二层（MAC 层），选档位时按现场实时性要求定——档位越小对设备要求越高。

## 讲深一层

| 档位 | 适用 |
|---|---|
| 10 ms | 高实时场景，设备要求高 |
| 30 ms | 较严格 |
| **200 ms** | 默认，多数场景够用 |
| 500 ms | 宽松场景，环大或设备能力有限 |

环上设备增多，恢复时间会变长，所以要留余量。

## 高频追问

1. **为什么是四个固定档而不是任意值？** —— 标准规定的档位，全环必须统一。
2. **环上最多挂多少台？** —— 一般建议单环不超过 50 台。
3. **和 RSTP 的秒级比差多少？** —— 差一个数量级。

## 易错点

- ❌ 说「几十毫秒到几秒」 —— 说不出档位
- ❌ 记错标准号
- ✅ 四个档位背下来，这是硬指标

## 关联项目

- `方向与规划/项目/西门子/西门子杯_面试口述稿与问答.pdf` §6.1 Q1
