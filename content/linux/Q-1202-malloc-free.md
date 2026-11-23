---
id: Q-1202
title: "malloc 申请的内存 free 之后还能继续访问吗？会发生什么？"
module: linux
sub: 系统与进程
priority: P0
difficulty: 2
roles: []
companies: []
qtype: principle
status: answered
source_type: nowcoder
source_ref: 牛客面经（华为·Linux 软件开发·一面）
verified_at: 2026-11-10
tags: [牛客面经, 华为]
appearances: ["华为·Linux 软件开发"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/947059125291118592
---

## 题目

**背景**：`p = malloc(64)` 用完后 `free(p)`，有人发现 free 之后 `p[0]` 还能读出旧值，得出"free 不清内存"的结论。
**问**：free 之后的内存还能继续访问吗？会发生什么？

## 口述答案

> 能访问到，但这是未定义行为。free 之后这块内存的所有权交还给分配器，glibc 会把它串进空闲链表（bin），并在块头部写管理信息，所以原来的一部分数据会被覆写。程序可能看起来正常——旧值还在，也可能随机崩溃——尤其后面又有 malloc 复用这块内存时。这就是 use-after-free：能不能复现完全看分配器的状态，最危险的是"测试时没事，上线就炸"。正确做法是 free 后立刻置 `p = NULL`，或直接用智能指针。

## 讲深一层

- glibc free 做的事：合并相邻空闲块、按大小入 bin（tcache/fastbin/unsorted）、在块内写 fd/bk 等管理字段
- "free 不清零"是性能取舍：清零要多一遍内存写，大块内存代价明显
- double free 会破坏 bin 链表，glibc 有 tcache double-free 检测，但绕过手段也存在

## 高频追问

1. 为什么 free 不顺手清零内存？——性能；清零是 calloc 的职责
2. 怎么在工程上防 use-after-free？——置空、智能指针、ASan
3. 野指针和悬垂指针的区别？

## 易错点

- 说"free 之后内存被回收所以读不到"——读得到，只是不该读
- 把 UB 说成"一定会段错误"

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 华为 | Linux 软件开发 | 一面 | https://www.nowcoder.com/discuss/947059125291118592 | 社区经验 |

## 关联项目

- `C++面向对象_从零手写教程` §智能指针

## 来源

牛客面经 华为·Linux 软件开发·一面：https://www.nowcoder.com/discuss/947059125291118592
