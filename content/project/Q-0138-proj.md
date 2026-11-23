---
id: Q-0138
title: 为什么用 RS485 而不是普通 TTL 串口？
module: project
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

**场景**：设备要装在车上或野外，线缆要跑几十米。

**问**：TTL 串口不行吗？RS485 好在哪？

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

> RS485 是**差分传输**，两根线（A/B）上的共模干扰会被接收端相减抵掉，
> 抗干扰能力强，传输距离能到千米级；
> TTL 串口是单端信号，只能跑很短。
> 我的设备要装在车上或野外，线缆长度和环境干扰都是现实问题，所以选 RS485。
> 注意不要说成「RS485 更快」——真正的选型理由是**现场可靠性**。

## 讲深一层

| 维度 | TTL 串口 | RS485 |
|---|---|---|
| 信号 | 单端（对地） | 差分（A-B） |
| 距离 | 几十 cm 到几米 | 可达 1200 m |
| 抗干扰 | 弱 | 强（共模抑制） |
| 拓扑 | 点对点 | 总线可挂多设备 |
| 速率 | 高 | 随距离下降 |

## 高频追问

1. **差分为什么抗干扰？** —— 干扰同时叠加在两根线上，相减就抵消了。
2. **要加终端电阻吗？** —— 长线、高速时要加 120 Ω 匹配。
3. **RS485 和 RS232 区别？** —— 232 是单端、点对点、距离短。

## 易错点

- ❌ 说「RS485 更快」 —— 一般是 232 速率更高但距离短
- ❌ 忘了共模范围和接地
- ✅ 从「距离 + 干扰 + 拓扑」三个角度讲

## 关联项目

- `方向与规划/项目/毕设/本科毕设_面试口述稿与专业问答_完整版.pdf` §6.1 第一档 Q9
