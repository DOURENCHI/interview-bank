---
id: Q-0129
title: 日志级别怎么识别？为什么匹配串要带空格？
module: 01_project
sub: Linux 日志分析
priority: P0
difficulty: 2
roles: [系统工程, 感知]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/Linux日志分析工具/Linux日志分析工具_项目说明书.pdf
verified_at: 2026-11-09
tags: [项目深挖, Linux, 图文]
auto: true
proj_seed: true
---

## 题目

**场景**：日志里级别有多种写法：`[INFO]`、`INFO:`、` INFO `。

**问**：怎么识别？为什么带空格？这个做法有什么问题？

<svg viewBox="0 0 860 230" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="lgar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="230" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">日志工具的数据流：先筛后统计</text>
<text x="20" y="48" font-size="12" fill="#665c49">顺序决定了报告里的数字和用户看到的筛选条件对不对得上</text>

<rect x="20" y="74" width="146" height="62" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="93" y="99" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">getline 逐行读</text>
<text x="93" y="119" font-size="11" fill="#665c49" text-anchor="middle">内存 O(1) 行</text>

<rect x="192" y="74" width="146" height="62" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="265" y="99" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">关键词筛选</text>
<text x="265" y="119" font-size="11" fill="#665c49" text-anchor="middle">过滤整行</text>

<rect x="364" y="74" width="146" height="62" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="437" y="99" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">时间筛选</text>
<text x="437" y="119" font-size="11" fill="#665c49" text-anchor="middle">HH:MM:SS 字符串比</text>

<rect x="536" y="74" width="146" height="62" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="609" y="99" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">分级统计</text>
<text x="609" y="119" font-size="11" fill="#665c49" text-anchor="middle">只统计通过的行</text>

<rect x="708" y="74" width="146" height="62" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="781" y="99" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">报告输出</text>
<text x="781" y="119" font-size="11" fill="#665c49" text-anchor="middle">终端 + 文件</text>

<line x1="166" y1="105" x2="188" y2="105" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#lgar)"/>
<line x1="338" y1="105" x2="360" y2="105" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#lgar)"/>
<line x1="510" y1="105" x2="532" y2="105" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#lgar)"/>
<line x1="682" y1="105" x2="704" y2="105" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#lgar)"/>
<rect x="192" y="152" width="318" height="46" rx="8" fill="#faede8" stroke="#a63a2e" stroke-dasharray="4 3"/>
<text x="351" y="172" font-size="11" fill="#a63a2e" text-anchor="middle">第一版把这两步写反了：先统计后筛选</text>
<text x="351" y="189" font-size="11" fill="#a63a2e" text-anchor="middle">结果筛了 300 行，报告总数还是 5000</text>
</svg>

## 口述答案

> 用 string::find 找级别子串，带空格是为了**避免误匹配**——不加空格，`INFORMATION` 里的 INFO 也会命中。
> 但这是个已知的不健壮设计：它依赖级别两侧恰好有空格，格式一变（比如 `[INFO]`）就失效。
> 更好的做法是按分隔符解析字段，或者用正则加词边界。
> 这条我写进了改进计划——**能主动说出局限，比硬说没问题可信**。

## 讲深一层

| 方案 | 健壮性 | 成本 |
|---|---|---|
| 整行 find(" INFO ") | 低 | 极低 |
| 按分隔符切字段 | 中 | 需要解析逻辑 |
| 正则 `\b(INFO)\b` | 高 | 正则开销 |
| 结构化日志（JSON） | 最高 | 依赖格式 |

## 高频追问

1. **std::regex 支持 \b 吗？** —— 支持。
2. **find 和正则谁快？** —— find 快很多，日志量大时差异明显。
3. **一行出现两个级别词？** —— 子串匹配取第一个，可能取错。

## 易错点

- ❌ 说「find 找 INFO 就行」 —— 没考虑误匹配
- ❌ 被问格式变化答不上 —— 应主动承认是局限
- ✅ 把「当时怎么做 / 现在会怎么做」分开讲

## 关联项目

- `Linux日志分析工具_项目说明书.pdf` §5 后续改进计划（第 3 条）

## 来源

本人项目说明书

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
