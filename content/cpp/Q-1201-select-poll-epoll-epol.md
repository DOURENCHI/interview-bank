---
id: Q-1201
title: "select、poll、epoll 有什么区别？epoll 为什么高效？"
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

**背景**：单机要同时盯着上万个连接，早期用 `select`/`poll`，连接数一上来 CPU 全耗在轮询上。
**问**：select、poll、epoll 有什么区别？epoll 为什么高效？

## 口述答案

> 三者都是 IO 多路复用。`select` 用 fd 位图，上限 1024，每次调用都要全量拷贝进内核并线性扫一遍；`poll` 用数组去掉了上限，但仍然是全量拷贝加 O(n) 扫描。epoll 把"管 fd"和"等事件"拆开：`epoll_ctl` 把 fd 挂进内核红黑树（只注册一次），事件到达时内核回调把就绪 fd 挂到就绪链表，`epoll_wait` 只返回就绪的那几个。所以注册是 O(1) 一次性的，等待返回 O(就绪数) 而不是 O(总连接数)，连接多但活跃少时优势最大。

## 讲深一层

| 维度 | select | poll | epoll |
|---|---|---|---|
| fd 上限 | 1024 | 数组，无硬上限 | 无硬上限 |
| 每次调用 | 全量拷贝+全量扫描 | 全量拷贝+全量扫描 | 只返回就绪链表 |
| 内核数据结构 | 位图 | 数组 | 红黑树 + 就绪链表 |
| 复杂度 | O(n) | O(n) | O(1) 注册 + O(就绪) 等待 |

工作模式：LT（水平触发，没读完会一直提醒，默认）与 ET（边缘触发，只提醒一次，必须配非阻塞 fd 一次读完）。

## 高频追问

1. ET 和 LT 的区别？ET 为什么必须配非阻塞 fd？——ET 只通知一次，阻塞 fd 读不完会卡死在这次读上
2. epoll_wait 返回的 events 里怎么知道哪个 fd 出了什么事？
3. nginx/redis 用的是 LT 还是 ET？——nginx ET，redis LT

## 易错点

- 说 epoll"比 select 快"却说不出原因；关键是回调 + 就绪链表，把扫描从 O(n) 降到 O(就绪)
- 忘了 epoll 只在 Linux 有，跨平台要 poll/kqueue/IOCP

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 华为 | Linux 软件开发 | 二面 | https://www.nowcoder.com/discuss/947059125291118592 | 社区经验 |

## 关联项目

- `Linux操作系统速通教程` §网络编程；`华为机考` 无关

## 来源

牛客面经 华为·Linux 软件开发·二面：https://www.nowcoder.com/discuss/947059125291118592
