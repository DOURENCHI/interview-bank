---
id: Q-1206
title: "TIME_WAIT 为什么要存在？为什么等 2MSL？"
module: 03_linux
sub: 网络编程
priority: P0
difficulty: 3
roles: []
companies: []
qtype: principle
status: answered
source_type: nowcoder
source_ref: 牛客面经（华为·Linux 软件开发·二面）
verified_at: 2026-11-10
tags: [牛客面经, 华为]
appearances: ["华为·Linux 软件开发"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/947059125291118592
---

## 题目

**背景**：接着 TIME_WAIT 问下去：为什么主动关闭方要停这么久？为什么恰好是 2MSL？
**问**：TIME_WAIT 为什么要存在？为什么等 2MSL？

## 口述答案

> 两个目的，各占一个 MSL。第一，保证最后一个 ACK 可靠送达：主动关闭方发完最后 ACK 就走的话，如果这个 ACK 丢了，对端会重传 FIN，没人应答它就只能 RST 收场，正常关闭流程走不完——留在 TIME_WAIT 就能重发 ACK。第二，让本连接的旧报文在网络里自然消亡：MSL 是报文的最大存活时间，等 2MSL 后旧连接的延迟报文必定已死，不会串进复用同四元组的新连接。所以时长 = "一来一回最多 2MSL"。

## 讲深一层

- MSL 典型 30 秒（Linux `TCP_LINGER2`/`ip_frag` 相关，RFC 建议 2 分钟）
- 想缩短：`SO_LINGER` 强制 RST 关闭（不推荐，丢数据风险）
- 四元组复用其实有 tcp_tw_reuse + 时间戳这条正路

## 高频追问

1. 如果最后一个 ACK 确认丢了，被动方会怎样？——重传 FIN，最多重试几次后放弃
2. 为什么不用"等对端 ACK 我的 ACK"？——ACK 本身不会被 ACK，会无限递归

## 易错点

- 只答"防止旧报文"漏了可靠关闭那一半
- 把 MSL 说成 TTL——TTL 是跳数，MSL 是时间

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 华为 | Linux 软件开发 | 二面 | https://www.nowcoder.com/discuss/947059125291118592 | 社区经验 |

## 关联项目

- `Linux操作系统速通教程` §网络

## 来源

牛客面经 华为·Linux 软件开发·二面：https://www.nowcoder.com/discuss/947059125291118592
