---
id: Q-0125
title: 工业信息安全你做到哪一步？边界在哪？
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

**场景**：赛题要求做「工业信息安全策略设计」，还配了信息安全模块。

**问**：实际做了什么？哪些只写在方案里没落地？

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

> 做了两件：网络分区（VLAN 隔离控制网与办公网）和边界防护（安全模块上配访问控制）。
> 没做的：主机加固、补丁管理、审计日志、入侵检测——赛期有限，这些只在方案里写了。
> 边界我会主动说清：**配置层面做到访问控制，体系层面只是方案**。
> 顺带一个点：工控安全的优先级是**可用性优先于机密性**，和办公网反过来——产线停机比数据泄露更严重。

## 讲深一层

IEC 62443 三个概念够用：

| 概念 | 含义 |
|---|---|
| Zone | 按安全需求划分的区域 |
| Conduit | 区之间的受控通道 |
| SL | 每个区要求的安全等级 |

## 高频追问

1. **为什么工控网不敢随便打补丁？** —— 补丁可能改行为、需停机验证。
2. **安全模块配了什么？** —— 访问控制列表 + 区域间流量限制。
3. **对机器人岗有用吗？** —— 有，内部通信和远程运维涉及同样的分区问题。

## 易错点

- ❌ 把方案里写的都当成做过的 —— 一问细节就崩
- ❌ 说「完整的纵深防御」 —— 明显夸大
- ✅ 主动划边界：「配置层做到 X，体系层只是方案」

## 关联项目

- `西门子杯_面试口述稿与问答.pdf` §7 边界与风险

## 来源

IEC 62443；本人竞赛方案

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
