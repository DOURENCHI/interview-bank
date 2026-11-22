---
id: Q-4304
title: "CAN 驱动突然 Kernel Panic，你怎么定位？"
module: 09_hardware
sub: 工程与调试
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

**背景**：现场设备 CAN 驱动偶发 Kernel Panic，重启后日志没了，无法稳定复现。
**问**：CAN 驱动突然 Kernel Panic，你怎么定位？

## 口述答案

> 分三步。第一步是**留住现场**：内核 panic 后默认不落盘，要提前配 pstore/ramoops，把 oops 写进保留内存，重启后从 `/sys/fs/pstore` 拿回完整寄存器与调用栈；没有 pstore 就串口抓 console。第二步是**解符号**：拿 PC 地址和栈回溯里的地址，用 `addr2line -e vmlinux` 或 `objdump -d` 定位到函数和行号，前提是内核编译时带 KALLSYMS 和调试信息，版本必须与现场一致。第三步是**收敛根因**：CAN 驱动常见嫌疑是中断处理里访问已释放的缓冲、DMA 映射没同步就读、错误计数路径的空指针；按嫌疑点加日志、开 KASAN/lockdep 在复现环境压测。我自己的经验是把"随机 Panic"变成"必现"才是突破口——用故障注入（断线、高负载、错误帧风暴）逼近现场条件。

## 讲深一层

- pstore/ramoops 原理：DT 里预留一段 RAM，panic 时内核把 console/oops 写进去，复位不擦除
- `CONFIG_KASAN` 找越界/UAF，`CONFIG_LOCKDEP` 找锁序问题；两者开销大只上复现机

## 高频追问

1. 拿到的只有地址没有 vmlinux 怎么办？——用同版本内核 + KALLSYMS 的 System.map 粗定位
2. panic 和 oops 的区别？——oops 之后进程被杀系统还能跑，panic 直接停机

## 易错点

- 现场重启用 printk 复现——日志早丢了，先配 pstore
- 用了和现场不同配置的 vmlinux 解符号，行号全错

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 二面 | https://www.nowcoder.com/discuss/945100814861815808 | 社区经验 |

## 关联项目

- `Linux操作系统速通教程` §调试

## 来源

牛客面经 地平线·嵌入式软件·二面：https://www.nowcoder.com/discuss/945100814861815808
