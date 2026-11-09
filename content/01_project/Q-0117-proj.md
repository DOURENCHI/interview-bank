---
id: Q-0117
title: 这个方案的局限是什么？为什么用 DHT11 而不是红外测温？
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

**问**：方案的边界在哪？如果重做会怎么改？

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

> 最明确的局限是**量程**：DHT11 只有 0–50℃，而夏季沥青路面能到 60℃ 以上，
> 这不是精度问题，是**测不到**。
> 当初选它的理由是：接触式要埋设、破坏路面，红外精度高但成本上去了，
> 本科阶段的可控条件下，我把重心放在验证「采集—4G—云端」这条链路的可行性。
> 所以论文题目是「获取方法」，结论里也写明了这个边界。
> 要继续做，先解决量程（红外或热电偶），再补标准仪器比对。

## 讲深一层

| 方式 | 精度 | 成本 | 主要问题 |
|---|---|---|---|
| DHT11（本方案） | ±2℃ | 极低 | 量程 0–50℃，超了测不到 |
| 红外测温 | 较高 | 中高 | 受发射率与环境辐射影响，要标定 |
| 埋热电偶 | 高 | 中 | 施工破坏路面 |

## 高频追问

1. **这数据能用来干嘛？** —— 趋势观测和链路验证，不能做标定级测量。
2. **给你三个月先改什么？** —— 先解决量程，再做标准仪器比对量化误差。
3. **为什么不一上来就用红外？** —— 成本与标定门槛，本科阶段先打通链路是合理取舍。

## 易错点

- ❌ 硬说「精度够用」 —— 一算 60℃ 就超量程
- ❌ 把「测不到」说成「测不准」 —— 量程和精度是两个问题
- ✅ 主动承认边界 + 给改进路径，是加分不是减分

## 关联项目

- `本科毕设_面试口述稿与专业问答_完整版.pdf` §7 边界与风险

## 来源

本人本科毕设

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
