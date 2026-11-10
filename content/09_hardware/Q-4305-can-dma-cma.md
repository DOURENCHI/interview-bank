---
id: Q-4305
title: "给 CAN DMA 申请大块连续内存有哪些方式？CMA 是什么？"
module: 09_hardware
sub: 嵌入式软件
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

**背景**：CAN 环形缓冲区想要 4MB 物理连续内存，kmalloc 申请失败，面试官问还有什么办法。
**问**：给 DMA 申请大块连续内存有哪些方式？CMA 是什么？

## 口述答案

> 先说为什么难：系统跑久了物理内存被打碎，kmalloc 走伙伴系统要**物理连续**，大块很难凑出来。常规选项：kmalloc 适合小块；`__get_free_pages` 最高也就按 2^MAX_ORDER（一般 4MB）碰运气；vmalloc 是**虚拟连续、物理不连续**，CPU 访问没问题但普通 DMA 不能直接用。正解是 CMA——连续内存分配器：启动时从内存里划出一大块预留区，平时它允许被可移动页借用来当普通内存，等驱动要大块物理连续内存时，把借用的页迁走、腾出整块交给 DMA。驱动侧 `dma_alloc_coherent` 的底层就接在 CMA 上。设备树里用 reserved-memory 节点配置大小，内核参数 `cma=64M` 也能指定。代价是启动参数要规划好，划多了浪费内存、划少了照样分配失败。

## 讲深一层

- CMA 关键字：MIGRATE_CMA 页迁移类型；"平时可借、用时搬走"
- IOMMU 存在时，物理不连续也能 DMA——映射 IOMMU 页表即可，很多现代 SoC 走这条路

## 高频追问

1. CMA 的内存能被普通应用用到吗？——能， movable 页优先落在 CMA 区
2. dma_alloc_coherent 和 CMA 什么关系？——大体量分配走 CMA，小量走池

## 易错点

- 说 vmalloc 也能给 DMA 用——物理不连续，除非有 IOMMU
- 忘了 CMA 是"预留但可借"，说成"完全浪费一段内存"

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 二面 | https://www.nowcoder.com/discuss/945100814861815808 | 社区经验 |

## 关联项目

- `嵌入式通信总线协议教程` §DMA

## 来源

牛客面经 地平线·嵌入式软件·二面：https://www.nowcoder.com/discuss/945100814861815808
