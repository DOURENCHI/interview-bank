---
id: Q-1222
title: "fork 创建子进程时地址空间怎么处理？什么是写时复制？"
module: 03_linux
sub: 系统与进程
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
appearances: ["地平线·嵌入式软件"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/945100596145553408
---

## 题目

**背景**：进程动辄几百 MB，fork 一个子进程难道真要复制几百 MB？面试官顺带问 exec。
**问**：fork 创建子进程时地址空间怎么处理？什么是写时复制？

## 口述答案

> fork 复制的是页表，不是物理页。父子进程的页表项指向同一批物理页，这些页全部被标成只读，这叫写时复制：谁真正执行"写"，MMU 触发缺页异常，内核才分配新页、拷贝内容、把这两页改回可写。好处有两个：fork 快（复制几百 MB 变成复制几 MB 页表）、省内存（不写的代码段永远共享）。这也解释了 `fork + exec` 为什么高效——fork 复制出来的页几乎立刻被 exec 整体替换，真复制反而是浪费。追问点通常有两个：一是 vfork 更极端，连页表都共享、父进程被挂起直到 exec；二是 COW 之后共享的还有文件映射、信号处理器等元信息。

## 讲深一层

```
fork()  → 复制页表，双方页标只读
父写    → 缺页 → 内核分配新页 → 拷贝 → 改写可写
子读    → 命中共享页，无拷贝
```
- `fork` 返回两次：父拿子 pid，子拿 0
- 多线程进程 fork 后子进程只剩调用线程——锁可能永久持着，exec 前只能做 async-signal-safe 的事

## 高频追问

1. 为什么 fork 后立刻 exec 时 COW 尤其划算？
2. 内核怎么知道某页是 COW？——页表项写保护 + 私有映射标志

## 易错点

- 说 fork 复制全部物理内存
- 不知道多线程 fork 的"只剩一个线程"陷阱

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 地平线 | 嵌入式软件 | 一面 | https://www.nowcoder.com/discuss/945100596145553408 | 社区经验 |

## 关联项目

- `Linux操作系统速通教程` §进程

## 来源

牛客面经 地平线·嵌入式软件·一面：https://www.nowcoder.com/discuss/945100596145553408
