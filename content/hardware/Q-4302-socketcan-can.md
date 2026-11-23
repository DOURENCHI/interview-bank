---
id: Q-4302
title: "SocketCAN 在用户空间怎么收发 CAN 报文？过滤器怎么设？"
module: hardware
sub: 总线协议
priority: P1
difficulty: 3
roles: []
companies: []
qtype: principle
status: answered
source_type: nowcoder
source_ref: 牛客面经（地平线·嵌入式软件·一面）
verified_at: 2026-11-10
tags: [牛客面经, 地平线]
appearances: ["地平线·嵌入式软件"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/945100596145553408
---

## 题目

**背景**：Linux 上调试 CAN，面试官问用户空间那一层怎么写。
**问**：SocketCAN 在用户空间怎么收发 CAN 报文？过滤器怎么设？

## 口述答案

> SocketCAN 把 CAN 接口包装成网络套接字。收发的套路是：`socket(AF_CAN, SOCK_RAW, CAN_RAW)` 创建原始套接字，`ioctl(SIOCGIFINDEX)` 拿到 can0 的接口索引，`bind` 绑上去；之后每帧就是 `struct can_frame`——11 位（或 29 位扩展）的 can_id、8 字节以内的 DLC 和 data，`read/write` 直接收发，像操作 UDP 一样。过滤器有两种设置方式：运行时 `setsockopt(CAN_RAW_FILTER)` 传一个 `can_filter` 数组，每项是 can_id + can_mask，内核按"收到的 id & mask == filter.id & mask"逐条匹配，命中才投递；也可以用 setsockopt 关过滤收全量。过滤器在内核态生效，用户态 read 之前就被筛掉了，这是它比"收全量再软件筛"高效的原因。

## 讲深一层

```c
struct can_filter rfilter[1];
rfilter[0].can_id   = 0x123;
rfilter[0].can_mask = CAN_EFF_FLAG | CAN_RTR_FLAG | 0x7FF;
setsockopt(s, SOL_CAN_RAW, CAN_RAW_FILTER, &rfilter, sizeof(rfilter));
```
- can_mask 里被置 1 的位才参与比较；把 RTR/EFF 标志位也算进 mask
- 发送：`write(s, &frame, sizeof(frame))`；帧结构 8 字节上限是 CAN 经典帧的硬约束

## 高频追问

1. CAN FD 的帧结构差在哪？——DLC 最大 64 字节，用 canfd_frame
2. 多个进程同时 bind can0 会互相抢帧吗？——各套接字独立收一份，类似组播

## 易错点

- 用 `read` 收全量再在应用层过滤——内核过滤器白给的性能不要
- mask 忘了含 EFF/RTR 标志位，扩展帧被莫名丢弃

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 一面 | https://www.nowcoder.com/discuss/945100596145553408 | 社区经验 |

## 关联项目

- `嵌入式通信总线协议教程` §CAN

## 来源

牛客面经 地平线·嵌入式软件·一面：https://www.nowcoder.com/discuss/945100596145553408
