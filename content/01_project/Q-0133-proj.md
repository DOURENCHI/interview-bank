---
id: Q-0133
title: 这个项目有什么局限？给你两周先改什么？
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

**场景**：说明书里自己列了改进计划。

**问**：局限在哪？优先级怎么排？

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

> 三条：时间跨天会算错、级别识别依赖空格、README 里有些功能没逐条实测。
> 优先级我选**跨天 > 级别识别 > 功能验证**，依据是「后果严重性 × 触发概率」：
> 跨天错误直接让结果错，凌晨日志很常见；级别识别是健壮性问题；功能验证成本最低但影响可信度。
> 两周计划：时间改造半天、级别重构两天、剩下补测试和 README 对齐。

## 讲深一层

| 问题 | 后果 | 概率 | 优先级 |
|---|---|---|---|
| 跨天算错 | 结果错 | 高 | 高 |
| 级别识别失效 | 统计错 | 中 | 中 |
| 功能未验证 | 可信度受损 | 高 | 中高（成本最低） |

注意第三条的「后果」不是功能错误，而是可信度——面试场景下它其实最该先做。

## 高频追问

1. **为什么没做跨天？** —— 测试数据都在同一天，覆盖不足。
2. **怎么补测？** —— 边界用例：跨天、空文件、超长行、格式异常。
3. **两周够吗？** —— 够改前两条，测试期间才是主要工作量。

## 易错点

- ❌ 说「没什么局限」 —— 不诚实
- ❌ 只列局限不给优先级 —— 没判断力
- ✅ 用「后果 × 概率」论证，并承认覆盖不足

## 关联项目

- `Linux日志分析工具_项目说明书.pdf` §5 后续改进计划

## 来源

本人项目说明书

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
