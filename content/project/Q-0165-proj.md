---
id: Q-0165
title: 退出码怎么设计的？为什么这件事重要？
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

**场景**：这个工具会被脚本调用，脚本怎么知道它成功了没有？

**问**：退出码怎么设计？

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

> 退出码是命令行工具的**对外契约**。脚本里 `cmd && next` 或 `if cmd; then` 全靠它判断。
> 我设计成 0 成功，参数个数不对、时间格式非法、文件打不开、报告写失败分别给不同非零值。
> 如果永远返回 0，脚本就无法区分「正常跑完」和「其实没读到文件」，自动化流程会静默出错。
> 关键原则：**出错立刻返回非零，不要跑完再返 0**。

## 讲深一层

| 码 | 含义 | 惯例 |
|---|---|---|
| 0 | 成功 | 统一 |
| 1 | 一般错误 | 通用兜底 |
| 2 | 用法错误 | grep/bash 都用 2 |
| 126/127 | 无法执行 / 命令不存在 | **shell 保留** |
| 128+n | 被信号 n 终止 | **shell 保留** |

自定义错误别占保留值。

## 高频追问

1. **C++ 里怎么返回？** —— `return code;` from main。
2. **和异常怎么配合？** —— main 里 catch 全部转成错误码。
3. **怎么测？** —— `./tool ...; echo $?`。

## 易错点

- ❌ 所有错误都 return 1
- ❌ 出错后继续跑完再返 0 —— 假成功最危险
- ✅ 文档列出每个码的含义

## 关联项目

- `方向与规划/项目/Linux日志分析工具/Linux日志分析工具_项目说明书.pdf` §2.3 设计点（3）、§6.2 Q14
