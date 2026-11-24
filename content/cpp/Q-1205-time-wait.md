---
id: Q-1205
title: "服务器上出现大量 TIME_WAIT 是什么原因？怎么处理？"
module: cpp
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

**背景**：一台短连接压测网关，netstat 里几万个 TIME_WAIT，新连接偶尔报 `Cannot assign requested address`。
**问**：大量 TIME_WAIT 是什么原因？怎么处理？

## 口述答案

> TIME_WAIT 出现在**主动关闭**的一方，等 2MSL 后才消失。大量出现说明本机在高频主动断连接——典型是短连接：每次 HTTP 请求建一条 TCP、用完就关。危害是占端口和内存，客户端侧还会耗尽临时端口。处理顺序：先治本——改长连接（连接池/keep-alive），这是唯一正解；治标——服务端 `SO_REUSEADDR` 让绑定不等 TIME_WAIT，客户端开 `tcp_tw_reuse` 复用出方向连接、扩大 `ip_local_port_range`。`tcp_tw_recycle` 别提，NAT 下会出事，内核 4.12 已移除。

## 讲深一层

| 手段 | 作用 | 注意 |
|---|---|---|
| 长连接/连接池 | 治本，减少主动关闭 | 首选 |
| SO_REUSEADDR | 服务端重启立即绑端口 | 只影响 listen 绑定 |
| tcp_tw_reuse | 客户端复用出站 TIME_WAIT | 要开时间戳 |
| ip_local_port_range | 扩大临时端口 | 缓解不是解决 |

## 高频追问

1. 为什么 TIME_WAIT 在主动关闭方而不是被动方？
2. 服务端大量 CLOSE_WAIT 说明什么？——自己忘了 close，代码 bug

## 易错点

- 把 TIME_WAIT 归罪于服务端——主动关闭方才进 TIME_WAIT
- 建议开 tcp_tw_recycle——NAT 环境丢连接，已从内核移除

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 华为 | Linux 软件开发 | 二面 | https://www.nowcoder.com/discuss/947059125291118592 | 社区经验 |

## 关联项目

- `Linux操作系统速通教程` §网络

## 来源

牛客面经 华为·Linux 软件开发·二面：https://www.nowcoder.com/discuss/947059125291118592
