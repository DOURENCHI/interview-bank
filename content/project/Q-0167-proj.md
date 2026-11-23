---
id: Q-0167
title: 这个项目为什么没有自动化测试？
module: project
sub: Linux 日志分析
priority: P0
difficulty: 3
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

**问**：这是最容易被戳的点，怎么答才不显得敷衍？

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

> 因为我当时是先跑通再补文档，`tests` 目录建了但是空的。
> 这是这个项目**最大的短板**，我不回避。
> 计划是用 shell 脚本做端到端断言：构造已知数据的小日志，跑工具，比对输出和退出码。
> 更彻底的做法是把「过滤」「统计」抽成独立函数做单元测试——
> 但那又回到「该不该拆文件」那个话题了。

## 讲深一层

这个项目的测试该测什么：

| 层 | 用例 |
|---|---|
| 参数 | 缺参数、多参数、非法时间格式 |
| 过滤 | 关键词命中/不命中、时间边界 |
| 统计 | 各级别计数、空文件 |
| 输出 | 报告文件内容、退出码 |

边界用例比正常用例更重要：空文件、超长行、跨天、格式异常。

## 高频追问

1. **为什么没写？** —— 优先级排错了，先做了功能。
2. **补的话要多久？** —— shell 断言脚本半天，单元测试要重构。
3. **没有测试你怎么保证正确？** —— 手工验证 + 已知数据比对，但这不可持续。

## 易错点

- ❌ 说「项目小不用测」 —— 小项目更是练测试的好机会
- ❌ 回避问题
- ✅ 承认 + 给出具体补法

## 关联项目

- `方向与规划/项目/Linux日志分析工具/Linux日志分析工具_项目说明书.pdf` §6.3 Q18（作者自述「最大短板」）、§1.3 功能清单与验证状态
