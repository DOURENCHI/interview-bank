---
id: Q-4306
title: "CAN 总线的错误处理有哪些？Bus-Off 是什么？怎么恢复？"
module: hardware
sub: 总线协议
priority: P1
difficulty: 3
roles: []
companies: []
qtype: principle
status: answered
source_type: nowcoder
source_ref: 牛客面经（地平线·嵌入式软件·二面）
verified_at: 2026-11-10
tags: [牛客面经, 地平线]
appearances: ["地平线·嵌入式软件"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/945100814861815808
---

## 题目

**背景**：总线上有节点掉线又自己恢复，面试官从错误帧一路问到 Bus-Off。
**问**：CAN 总线的错误处理有哪些？Bus-Off 是什么？怎么恢复？

## 口述答案

> CAN 的可靠性靠错误计数器驱动三个状态。每个节点有发送错误计数 TEC 和接收错误计数 REC：正常态（error active）可以主动发错误帧；错误计满 128 进入 error passive，只能发隐性错误帧、不得主动打扰总线；再涨到 256 就进 Bus-Off——控制器与总线逻辑断开，节点既不发也不收，防止一个坏节点拖垮全网。恢复机制是硬件定义的：Bus-Off 后控制器监测总线，连续检测到 128 次 11 位隐性位（约等于 128 帧空闲）后错误计数清零、允许重新加入；软件层面驱动可以设 `restart-ms` 让内核定时器自动重启控制器，或应用层显式 `ip link set can0 type can restart`，重启时要重新初始化波特率和过滤器。工程上还要记日志——频繁 Bus-Off 说明有节点在发坏帧或波特率不匹配。

## 讲深一层

| 状态 | TEC/REC | 行为 |
|---|---|---|
| error active | <128 | 正常，可发主动错误帧 |
| error passive | 128–255 | 只发被动错误帧 |
| bus off | ≥256 | 离线，等恢复条件 |

- 错误帧由硬件自动发送，软件只读计数（`ip -details -s link show can0`）

## 高频追问

1. 怎么区分是硬件问题还是软件问题？——看错误计数走势与是否固定某节点
2. MRP/Master 对 Bus-Off 的兜底？——上层超时 + 周期重发（结合西门子杯项目讲）

## 易错点

- 说 Bus-Off 后节点"立即自动恢复"——要等 128×11 隐性位，或软件干预
- 只答协议计数，没提驱动层的 restart 流程

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 二面 | https://www.nowcoder.com/discuss/945100814861815808 | 社区经验 |

## 关联项目

- `方向与规划/项目/西门子杯`（PROFINET/MRP 环网容错实践）

## 来源

牛客面经 地平线·嵌入式软件·二面：https://www.nowcoder.com/discuss/945100814861815808
