---
id: Q-0126
title: 用一句话介绍你的 Linux 日志分析工具，它解决什么问题？
module: 01_project
sub: Linux 日志分析
priority: P0
difficulty: 1
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

**背景**：C++17 单文件约 237 行，公开仓库 `github.com/DOURENCHI/Linux-log-analyzer`，
环境 Ubuntu 22.04（WSL2）+ g++ 11.4。

**问**：一句话定位 + 它到底解决什么问题。

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

> 一个 C++17 写的命令行日志分析工具：逐行读日志，按关键词和时间范围筛选，
> 分类统计各级别条数，输出终端报告并写报告文件。
> 解决的问题是：日志动辄几十 MB，grep 只能筛不能统计，awk 能统计但每次都要现写，
> 这个工具把「筛选 + 分级统计 + 报告」固化成一条命令。
> 规模我如实说：约 240 行，从需求拆解到 Git 托管独立走完。

## 讲深一层

| 功能 | 输入 | 输出 |
|---|---|---|
| 关键词筛选 | 关键词 | 匹配行 |
| 时间筛选 | 起止时间 | 范围内行 |
| 级别统计 | — | 各级别条数 |
| 报告 | 报告路径 | 文本文件 |

用法：`./logtool <file> [keyword] [start] [end]`

## 高频追问

1. **为什么不用现成的 grep/awk？** —— 可以，但报告格式和分级统计每次要重写；这项目也练 C++ 文件流与字符串处理。
2. **240 行算项目吗？** —— 算，但要讲设计取舍，不是堆行数。
3. **跑在什么环境？** —— Ubuntu 22.04 / g++ 11.4 / C++17。

## 易错点

- ❌ 说成「日志分析平台」 —— 夸大
- ❌ 只讲功能不讲设计 —— 显得是练手
- ✅ 主动说规模，再把设计点讲透

## 关联项目

- `方向与规划/项目/Linux日志分析工具/Linux日志分析工具_项目说明书.pdf` §1 项目档案

## 来源

本人项目（2026-10-18 定稿）

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
