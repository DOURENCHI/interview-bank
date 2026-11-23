---
id: Q-0156
title: 程序整体是怎么跑起来的？主流程说一遍。
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

**问**：从启动到出报告，调用链是什么？

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

> main 先看参数个数，合法就解析出文件路径、关键词、起止时间；
> 然后调 analyze：打开文件，逐行 getline，每行先做关键词和时间两项筛选，
> 通过的才计入总数和分级统计；最后输出终端报告并写文件。
> 出错的分支都很早返回——参数不对、文件打不开、时间格式非法，各有对应退出码。

## 讲深一层

| 阶段 | 关键动作 | 失败处理 |
|---|---|---|
| 参数解析 | 检查个数、解析字段 | 返回用法错误码 |
| 打开文件 | ifstream | 返回打开失败码 |
| 逐行处理 | getline + 双筛选 + 统计 | — |
| 输出 | cout + ofstream | 检查流状态 |

设计特点是**早返回**：错误尽早退出，不带着错误往下跑。

## 高频追问

1. **为什么早返回？** —— 避免「带着错误继续跑」，最后报一个不相干的错。
2. **统计放哪？** —— 一组计数器，在筛选通过后累加。
3. **能不能并行？** —— 能按文件切分，但单文件单线程更简单。

## 易错点

- ❌ 只讲「读文件、统计、输出」三句
- ❌ 不提错误分支
- ✅ 强调「早返回」这个设计选择

## 关联项目

- `方向与规划/项目/Linux日志分析工具/Linux日志分析工具_项目说明书.pdf` §2.1 整体流程
