---
id: Q-0131
title: 40 位数据里每一位怎么区分 0 和 1？
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

**问**：DHT11 没有时钟线，靠什么编码？

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

> 靠**高电平持续时间**。每一位都以 50 µs 低电平起始，
> 之后高电平持续约 26 µs 表示 0、约 70 µs 表示 1。
> 所以驱动里必须有微秒级延时，不能用毫秒级或系统节拍去测。

## 讲深一层

| 位 | 低电平 | 高电平 |
|---|---|---|
| 0 | 50 µs | 26–28 µs |
| 1 | 50 µs | 70 µs |

判定通常取中间值（约 40 µs）作为阈值，而不是精确比对两个数——
因为每个器件有公差。

## 高频追问

1. **阈值取多少？** —— 大约 40 µs，具体可按实测调。
2. **延时不准会怎样？** —— 0 被读成 1 或反之，校验和能发现但定位不了。
3. **为什么不用输入捕获？** —— 可以，用定时器输入捕获测脉宽更准，但代码复杂。

## 易错点

- ❌ 说「靠高低电平区分」 —— 都是高电平，靠的是宽度
- ❌ 用 `HAL_Delay` 做微秒延时 —— 精度不够
- ✅ 记住 26 / 70 µs 这两个数

## 关联项目

- `方向与规划/项目/毕设/本科毕设_面试口述稿与专业问答_完整版.pdf` §6.1 第一档 Q2
