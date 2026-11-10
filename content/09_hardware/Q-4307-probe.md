---
id: Q-4307
title: "驱动里的 probe 函数负责什么？设备和驱动怎么匹配？"
module: 09_hardware
sub: 嵌入式软件
priority: P0
difficulty: 2
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

**背景**：写平台驱动时总要实现一个 probe 函数，面试官问它是被谁、什么时候调的。
**问**：驱动里的 probe 函数负责什么？设备和驱动怎么匹配？

## 口述答案

> probe 是"设备与驱动配对成功后"驱动的入口，负责把这个设备真正带起来：从设备树/ACPI 读硬件资源（寄存器地址 reg、中断号 interrupts、时钟 clocks），`platform_get_resource`/`devm_platform_ioremap_resource` 映射寄存器，申请中断并挂处理函数，使能时钟，初始化硬件，最后注册到子系统（字符设备、net_device、can_netdev 等），并把私有数据 `platform_set_drvdata` 存好供其他回调取用。匹配机制在总线层：`driver_register` 把驱动挂到总线的驱动链表，每来一个设备（`device_register`，通常由设备树解析产生）就调用总线的 match 函数——平台总线最常见的是拿设备的 compatible 字符串去对驱动的 of_match_table，对上就调 probe；匹配失败就等下一个驱动。probe 里几乎都要用 devm_ 系列接口，绑定设备生命周期，remove 时自动释放。

## 讲深一层

```
DT: compatible = "vendor,can"
  → of_match_table 命中 → probe()
      ioremap 寄存器 / request_irq / clk_prepare_enable
      注册 can_netdev → 用户态 ifconfig can0 出现
remove(): 反向释放
```
- 匹配优先级：of_match_table > id_table > driver.name
- 推迟探测：依赖的时钟/供电没就绪返回 -EPROBE_DEFER，核心稍后重试

## 高频追问

1. -EPROBE_DEFER 是什么场景？——依赖的 provider 还没注册
2. probe 和 init 函数的区别？——init 注册驱动，probe 每个设备各调一次

## 易错点

- compatible 写错一个字符，设备树不匹配 probe 永远不执行
- 用非 devm 接口在 probe 里出错路径漏释放

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 二面 | https://www.nowcoder.com/discuss/945100814861815808 | 社区经验 |

## 关联项目

- `Linux操作系统速通教程` §驱动

## 来源

牛客面经 地平线·嵌入式软件·二面：https://www.nowcoder.com/discuss/945100814861815808
