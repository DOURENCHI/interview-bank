---
id: Q-4301
title: "U-Boot 在 Linux 启动过程中负责哪些工作？典型启动流程是什么？"
module: hardware
sub: 嵌入式 Linux
priority: P0
difficulty: 2
roles: []
companies: []
qtype: principle
status: answered
source_type: nowcoder
source_ref: 牛客面经（地平线·嵌入式软件·一面）
verified_at: 2026-11-10
tags: [牛客面经, 地平线]
appearances: ["地平线·嵌入式软件", "原力灵机·嵌入式软件"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/945100596145553408
---

## 题目

**背景**：拿到一块新板子，上电到 Linux 起来中间那几秒是黑盒，面试官让你把这段讲透。
**问**：U-Boot 在 Linux 启动过程中负责哪些工作？典型启动流程是什么？

## 口述答案

> 整条链路是：芯片内 ROM → SPL（二级程序加载器）→ U-Boot proper → 内核。ROM 只认片内 SRAM，所以 SPL 的任务是最小化初始化——配时钟、初始化 DDR——然后把真正的 U-Boot 搬进内存跑。U-Boot proper 接管后做四件事：一是把硬件配齐（DDR、时钟、串口、存储控制器、网口）；二是从 eMMC/NAND/SPI/网络里把内核镜像 zImage 和设备树 DTB 加载到内存指定地址；三是准备启动参数，主要是 bootargs（console、root 位置、rootfs 类型）写进寄存器或 DTB 的 chosen 节点；四是跳转到内核入口，把机器 ID 或 DTB 地址按启动协议传过去。之后内核自解压、初始化、挂 rootfs、起 init，控制权交给用户态。

## 讲深一层

| 阶段 | 运行位置 | 职责 |
|---|---|---|
| Boot ROM | 片内 ROM | 读 SPL，验签 |
| SPL | 片内 SRAM | 最小初始化 + 加载 U-Boot |
| U-Boot proper | DDR | 完整驱动、加载内核/DTB |
| Linux | DDR | 自解压、挂根文件系统 |

- `bootz ${kernel_addr} - ${fdt_addr}`：中间的 `-` 是占位，表示不传 initrd
- 安全启动：ROM/SPL/每级验签下一级，U-Boot 可关闭 JTAG、锁 OTP

## 高频追问

1. DTB 是干嘛的？——描述硬件的树，内核不再硬编码板级信息
2. bootargs 里 root= 起什么作用？——告诉内核根文件系统在哪

## 易错点

- 只答"引导内核"——要能拆出 SPL 这一阶段
- 忽略 U-Boot 还负责传 bootargs

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 一面 | https://www.nowcoder.com/discuss/945100596145553408 | 社区经验 |
| 2026-10-28 发布 | 原力灵机 | 嵌入式软件 | 面经 | [抖音面经图文](https://www.douyin.com/note/7701332217108491171) | 社区经验 |
| 2026-10-17 发布 | 未注名 | 嵌入式软件 | 面经 | [抖音面经图文](https://www.douyin.com/note/7697589995939868072) | 社区经验 |

## 关联项目

- `单片机原理图与PCB` §启动；`嵌入式通信总线协议教程`

## 来源

牛客面经 地平线·嵌入式软件·一面：https://www.nowcoder.com/discuss/945100596145553408
