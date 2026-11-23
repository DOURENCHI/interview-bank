---
id: Q-4710
title: "batch=1、序列 128、kv_heads=8、head_dim=64、FP16，一层 KV Cache 占多少显存？"
module: cv_pytorch
sub: LLM 基础与训练
priority: P0
difficulty: 2
roles: []
companies: []
qtype: principle
status: answered
source_type: nowcoder
source_ref: 牛客面经（华为·AI 软件·笔试）
verified_at: 2026-11-10
tags: [牛客面经, 华为]
appearances: ["华为·AI 软件"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/948632550891593728
---

## 题目

**题目**（华为 AI 笔试）：某层使用 KV cache：batch=1，已缓存序列长度 128，kv_heads=8，head_dim=64，K 与 V 都以 FP16（每元素 2 字节）存储。该层 KV cache 占用的显存约为多少？
A. 64 KB　B. 128 KB　C. 256 KB　D. 512 KB

## 口述答案

> 选 C，256 KB。KV Cache 同时存 K 和 V 两份，公式：2（K+V）× batch × seq_len × kv_heads × head_dim × 每元素字节数 = 2 × 1 × 128 × 8 × 64 × 2 = 262144 字节 = 256 KB。这道题真正的考点有三个，都是工程里天天算的：一是别忘了乘 2——K、V 各一份，漏乘正好差一半选到 B；二是注意 GQA 下是 kv_heads 而不是注意力头数（MHA 时两者相等，GQA 时 KV 头数只有几组）；三是会外推——这个数字要乘层数才是整模型的单层序列开销，再乘 batch 和上下文长度，就是"为什么长上下文显存爆炸"的定量解释。

## 讲深一层

```
KV/层 = 2 × B × S × kv_heads × head_dim × bytes
      = 2 × 1 × 128 × 8 × 64 × 2 = 262,144 B = 256 KB
40 层模型单请求 128 token → 10 MB
```
- FP8/INT8 KV：字节数减半，Decode 带宽直接减半
- MQA：kv_heads=1，再省 kv_heads 倍

## 高频追问

1. GQA 和 MQA 分别省在哪？——组数减少，KV 头数下降
2. batch 翻倍 KV 怎么变？——线性翻倍，这是吞吐与显存的交换点

## 易错点

- 漏乘 K/V 的 2
- 把 head_dim 换成 hidden_size 算重

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 华为 | AI 软件 | 笔试 | https://www.nowcoder.com/discuss/948632550891593728 | 社区经验 |

## 关联项目

- `大模型与推理` Q-4713/Q-4716

## 来源

牛客面经 华为·AI 软件·笔试（11 月 6 日）：https://www.nowcoder.com/discuss/948632550891593728
