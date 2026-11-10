---
id: Q-4718
title: "DDP 和 DP 有什么区别？为什么说 DDP 不省显存？"
module: 10_cv_pytorch
sub: 训练
priority: P1
difficulty: 3
roles: []
companies: []
qtype: principle
status: answered
source_type: nowcoder
source_ref: 牛客面经（小鹏·深度学习平台研发·校招面试）
verified_at: 2026-11-10
tags: [牛客面经, 小鹏]
appearances: ["小鹏·深度学习平台研发"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/945709685955395584
---

## 题目

**背景**：小鹏面试官特意强调：别把 DDP 和 DP 搞混。
**问**：DDP 和 DP 有什么区别？为什么说 DDP 不省显存？

## 口述答案

> DP（DataParallel）是单进程多线程：一份模型放在 0 号卡，每个 batch 被散射到各卡前向，梯度全部拉回 0 号卡 reduce 后再广播。两个硬伤：主卡既存模型副本又承担汇总，显存和带宽是单点瓶颈；Python GIL 让主线程的 scatter/gather 串行化。DDP 是多进程：每张卡一个独立进程、一份等价模型，梯度用 Ring All-Reduce 环上均摊同步，没有主卡，绕开了 GIL，通信与反向计算还能重叠。但注意**DDP 不省显存**：每张卡都放完整的模型参数、梯度和优化器状态（Adam 是两份额外状态），省下的只是"数据怎么分"，不是"模型怎么放"。显存不够的解法是 FSDP/ZeRO——把参数、梯度、优化器状态切到各卡，用时再临时聚合；DDP 和它们解决的是两个维度的问题。

## 讲深一层

| | DP | DDP |
|---|---|---|
| 进程模型 | 单进程多线程 | 每卡一进程 |
| 梯度汇总 | 拉回主卡 reduce | Ring 均摊 |
| GIL | 受限 | 绕开 |
| 省显存 | ✗ | ✗（要 FSDP/ZeRO） |

## 高频追问

1. FSDP 和 DDP 的关系？——FSDP 在 DDP 的进程模型上加了参数分片与按需聚合
2. 什么模型规模必须放弃 DDP？——单卡装不下模型+激活时

## 易错点

- 面试时把两者说成一个东西——这是小鹏面试官点名的坑
- 把"数据并行"误解成"显存并行"

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 小鹏 | 深度学习平台研发 | 校招面试 | https://www.nowcoder.com/discuss/945709685955395584 | 社区经验 |

## 关联项目

- `深度学习基础` Q-4717

## 来源

牛客面经 小鹏·深度学习平台研发·校招面试：https://www.nowcoder.com/discuss/945709685955395584
