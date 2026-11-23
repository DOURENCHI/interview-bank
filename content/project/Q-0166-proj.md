---
id: Q-0166
title: 如果是 10 GB 的日志，你这个程序还能跑吗？
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

**问**：这是压力测试式的追问，考察你对自己程序瓶颈的认知。

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

> 能跑，因为逐行读，内存不会爆。但有两个问题：
> 一是**单线程**，速度受限，10 GB 可能要跑几分钟到十几分钟；
> 二是**没有进度提示**，跑起来像卡死了。
> 改进方向：按块并行处理（注意行边界）、加进度输出、或者先按时间粗筛减少数据量。
> 内存方面没问题，这是当初选逐行读的直接收益。

## 讲深一层

| 维度 | 现状 | 瓶颈 |
|---|---|---|
| 内存 | O(1) | 无 |
| 速度 | 单线程 | I/O + 单核 CPU |
| 可用性 | 无进度 | 用户以为卡死 |
| 结果 | 一次性输出 | 中途失败要重跑 |

并行要注意：**按字节块切分必须处理行跨越块边界**的问题。

## 高频追问

1. **并行怎么不切错行？** —— 每个线程从块起点往后找到第一个换行符才开始。
2. **进度怎么打？** —— 定期输出已处理字节数 / 文件总大小。
3. **中途失败怎么办？** —— 写临时文件 + 完成后重命名，避免半成品。

## 易错点

- ❌ 只说「能跑」不提瓶颈
- ❌ 忽略「无进度提示」这个体验问题
- ✅ 从内存、速度、可用性三个维度答

## 关联项目

- `方向与规划/项目/Linux日志分析工具/Linux日志分析工具_项目说明书.pdf` §6.3 Q17
