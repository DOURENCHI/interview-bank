---
id: Q-4303
title: "CAN 驱动用 DMA 要注意什么？Cache 一致性怎么处理？"
module: hardware
sub: 工程与调试
priority: P1
difficulty: 4
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

**背景**：CAN 驱动用 DMA 从控制器搬报文，偶尔收到旧数据或脏数据。
**问**：CAN 驱动用 DMA 要注意什么？Cache 一致性怎么处理？

## 口述答案

> 核心问题是 CPU 的 Cache 和 DMA 控制器互相看不见：DMA 直接读写内存，绕过 Cache。两种翻车方式——CPU 刚把接收缓冲写过一遍还在 Cache 里没落盘，DMA 读到的是内存里的旧值；反过来 DMA 写完新报文，CPU 读时命中 Cache 里的旧值。处理分两条路。一致性映射：用 `dma_alloc_coherent` 分配的缓冲本身是 uncached/同步属性，两边看到的一直是同一份，适合长期复用的环形缓冲区。流式映射：普通内存用 `dma_map_single` 交给 DMA，方向是"设备读"就在启动前 `dma_sync_single_for_device` 让 Cache 失效落盘，方向是"设备写"就在读之前 `dma_sync_single_for_cpu` 让 CPU 的旧 Cache 行作废——每轮都要同步，方向不能搞反。

## 讲深一层

| 方案 | API | 适用 |
|---|---|---|
| 一致性映射 | dma_alloc_coherent | 长期复用缓冲（描述符环） |
| 流式映射 | dma_map_single + sync_* | 单次收发缓冲 |

- 第三条路是硬件 IOMMU/IO-coherent 互联，SoC 一致则软件零成本，先查 datasheet
- 缓冲区要按 cache line 对齐，避免相邻数据被误伤

## 高频追问

1. coherent 内存为什么慢？——通常映射成非缓存，CPU 访问不走 Cache
2. 什么叫"方向搞反会怎样"？——该 invalidate 的做了 clean，旧值反而被写回

## 易错点

- 忘了每轮 sync，只在分配时映射一次
- 用 vmalloc 内存做 DMA——物理不连续

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 二面 | https://www.nowcoder.com/discuss/945100814861815808 | 社区经验 |
| 2026-10-12 发布 | 未注名 | 嵌入式软件 | 面经 | [抖音面经图文](https://www.douyin.com/note/7695722412604565160) | 社区经验 |

## 关联项目

- `嵌入式通信总线协议教程` §CAN/DMA

## 来源

牛客面经 地平线·嵌入式软件·二面：https://www.nowcoder.com/discuss/945100814861815808
