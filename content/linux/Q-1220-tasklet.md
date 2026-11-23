---
id: Q-1220
title: "Tasklet 里要访问共享数据怎么保证临界区安全？为什么不能用 mutex？"
module: linux
sub: 内核与驱动
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

**背景**：一个 tasklet 里要更新与中断共享的统计结构，第一反应是上 mutex。
**问**：Tasklet 里要访问共享数据怎么保证临界区安全？为什么不能用 mutex？

## 口述答案

> 不能上 mutex，原因一句话：tasklet 运行在软中断上下文，**不可睡眠**，而 mutex 拿不到锁会睡——睡在中断上下文会触发调度，而"中断返回"本身被卡住，可能直接死等。正确做法分两种情况：如果数据只被 tasklet 之间共享，同一个 tasklet 在系统里天然串行（同一个 tasklet 不会同时在两个 CPU 上跑），只需防它与其他 CPU 上别的 tasklet 并发，用普通 `spin_lock` 就够；如果还与硬中断共享，必须 `spin_lock_irqsave`——保存中断状态并关本地中断再拿锁，防止本核中断进来重入同一把锁。要点是记住 tasklet 的执行环境：软中断、禁睡眠、无进程上下文。

## 讲深一层

| 共享对象 | 保护手段 |
|---|---|
| 仅 tasklet 之间 | spin_lock |
| tasklet + 硬中断 | spin_lock_irqsave |
| tasklet + 进程上下文 | spin_lock_bh（关软中断） |
| 需要睡眠的处理 | 挪到 workqueue |

## 高频追问

1. workqueue 和 tasklet 的本质区别？——workqueue 在进程上下文，可以睡
2. 为什么同一 tasklet 不会并发？——调度时保证同哈希链上串行

## 易错点

- 在中断/软中断上下文用 mutex——内核会报 "scheduling while atomic"
- 该用 irqsave 的地方只用了 spin_lock——本核重入死锁

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 一面 | https://www.nowcoder.com/discuss/945100596145553408 | 社区经验 |

## 关联项目

- `Linux操作系统速通教程` §中断

## 来源

牛客面经 地平线·嵌入式软件·一面：https://www.nowcoder.com/discuss/945100596145553408
