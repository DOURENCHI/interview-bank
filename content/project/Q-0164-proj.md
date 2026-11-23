---
id: Q-0164
title: 为什么是单文件？不拆成模块吗？
module: project
sub: Linux 日志分析
priority: P0
difficulty: 2
roles: [SDK开发, 系统工程]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/Linux日志分析工具/Linux日志分析工具_项目说明书.pdf
verified_at: 2026-11-09
tags: [项目深挖, C++, Linux, 图文]
auto: true
proj_seed: true
---

## 题目

**问**：240 行全在 main.cpp 里，是不是不规范？

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

> 现在 240 行，拆了反而增加跳转成本——看一个函数要跳三个文件。
> 我的判断标准是**超过 500 行就该拆**，那时候按「参数解析 / 过滤 / 统计 / 报告」分层。
> 现在这个规模，单文件可读性反而更好。
> 但我也承认：如果要做单元测试，单文件就不好单独测某个函数了。

## 讲深一层

拆分的判断依据：

| 信号 | 含义 |
|---|---|
| 单文件超过 500 行 | 该按职责拆 |
| 需要独立测试某部分 | 抽成库 |
| 多人协作 | 分文件减少冲突 |
| 复用需求出现 | 抽公共模块 |

过早拆分的代价：文件跳转、编译依赖、接口设计成本。

## 高频追问

1. **怎么拆？** —— 参数解析、行处理、统计、报告输出四个模块。
2. **拆了能测吗？** —— 能，每个模块单独编测试。
3. **为什么不现在拆？** —— 规模不够，收益小于成本。

## 易错点

- ❌ 说「单文件更简单」 —— 要给判断标准
- ❌ 不知道什么时候该拆
- ✅ 给出「500 行」这个具体阈值

## 关联项目

- `方向与规划/项目/Linux日志分析工具/Linux日志分析工具_项目说明书.pdf` §6.2 Q12
