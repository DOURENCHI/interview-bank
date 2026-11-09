---
id: Q-0108
title: 这个部署项目你最后悔的是什么？重做会改哪几件事？
module: 01_project
sub: YOLO 部署
priority: P0
difficulty: 3
roles: [系统工程, 感知]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html
verified_at: 2026-11-09
tags: [项目深挖, YOLO, 图文]
auto: true
proj_seed: true
---

## 题目

**问**：项目做完了，回头看哪些决策是错的？

<svg viewBox="0 0 860 250" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="yacc" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="250" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">每一步掉了多少精度（mAP50，valid 集 187 图 / 839 框）</text>
<text x="20" y="48" font-size="12" fill="#665c49">真正掉点在 pt→ONNX，不在精度位宽上</text>
<line x1="60" y1="80" x2="800" y2="80" stroke="#dbcba5" stroke-width="2"/>

<circle cx="110" cy="80" r="7" fill="#665c49"/>
<text x="110" y="64" font-size="12" font-weight="700" fill="#665c49" text-anchor="middle">0.6407</text>
<text x="110" y="104" font-size="11" fill="#665c49" text-anchor="middle">原始 pt</text>

<circle cx="330" cy="80" r="7" fill="#1b5e8c"/>
<text x="330" y="64" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">0.6329</text>
<text x="330" y="104" font-size="11" fill="#665c49" text-anchor="middle">ONNX</text>

<circle cx="550" cy="80" r="7" fill="#12666e"/>
<text x="550" y="64" font-size="12" font-weight="700" fill="#12666e" text-anchor="middle">0.6327</text>
<text x="550" y="104" font-size="11" fill="#665c49" text-anchor="middle">engine FP32</text>

<circle cx="750" cy="80" r="7" fill="#2e6b3e"/>
<text x="750" y="64" font-size="12" font-weight="700" fill="#2e6b3e" text-anchor="middle">0.6323</text>
<text x="750" y="104" font-size="11" fill="#665c49" text-anchor="middle">engine FP16</text>

<line x1="110" y1="140" x2="330" y2="140" stroke="#a63a2e" stroke-width="1.4" stroke-dasharray="4 3"/>
<text x="220" y="158" font-size="12" fill="#a63a2e" text-anchor="middle">−0.0078（换后处理路径）</text>
<line x1="330" y1="140" x2="750" y2="140" stroke="#2e6b3e" stroke-width="1.4" stroke-dasharray="4 3"/>
<text x="540" y="158" font-size="12" fill="#2e6b3e" text-anchor="middle">−0.0006（FP32→FP16 几乎无损）</text>
<text x="20" y="196" font-size="12" fill="#2d2a21">面试时这句最有用：FP16 掉的那点精度，比更换后处理路径的影响小一个数量级。</text>
<text x="20" y="218" font-size="12" fill="#2d2a21">所以「量化会不会掉点」的答案取决于基线 —— 基线本身换过实现，讨论量化就没意义。</text>
</svg>

## 口述答案

> 两件。第一，**一开始就该用三层验证模板**（比框、比分数、比中间层），
> 我第一版只比框，出问题查了两轮才发现是没做 fuse。
> 第二，**第一版就该写 provider 断言**，那个静默回落 CPU 的 bug 让结果全对但慢十倍，
> 靠肉眼永远发现不了。
> 共同点是：这两件事都是「先花半小时搭好检查机制」就能省下后面几小时排查。

## 讲深一层

「重做会改什么」这类问题的答法：**不要说功能，要说机制**。

| 层次 | 例子 |
|---|---|
| 功能层（弱） | 我会加个 GUI |
| 机制层（强） | 我会先搭验证模板和断言 |

面试官想听的是后者，因为它体现的是**工程判断**而非功能想象。

## 高频追问

1. **三层验证具体怎么做？** —— 建一个脚本，同时 dump 三层结果并比对。
2. **断言会不会影响生产？** —— 放在 debug 构建或启动自检里，不影响热路径。
3. **还有别的机制上的改进吗？** —— 把延迟打点做成可开关的埋点，而不是临时加计时代码。

## 易错点

- ❌ 说「没什么后悔的」 —— 显得没反思
- ❌ 只讲功能层面的改进 —— 层次不够
- ✅ 讲机制，并说清「早花半小时省几小时」

## 关联项目

- `YOLO_部署实施记录.html` §如果重做一遍，我会改五件事

## 来源

本人项目复盘

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
