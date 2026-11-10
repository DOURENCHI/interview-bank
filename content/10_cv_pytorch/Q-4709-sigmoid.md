---
id: Q-4709
title: "Sigmoid 的导数最大能取到多少？在哪取到？"
module: 10_cv_pytorch
sub: 基础
priority: P1
difficulty: 1
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

**题目**（华为 AI 笔试）：Sigmoid 函数 σ(x) = 1/(1+e^-x) 的导数 σ'(x) 最大能取到多少？
A. 1　B. 0.5　C. 0.25　D. 1/e

## 口述答案

> 选 C，0.25。Sigmoid 的导数有个漂亮的闭式：σ'(x) = σ(x)(1-σ(x))。令 t = σ(x) ∈ (0,1)，问题变成求 t(1-t) 的最大值——开口向下的抛物线，顶点在 t = 1/2，最大值 1/2 × 1/2 = 1/4，对应 x = 0。这个结论连着一串考点：Sigmoid 最大梯度只有 0.25，深层网络层层相乘梯度衰减极快，这就是梯度消失的定量来源之一；而 t(1-t) 在 t 趋近 0 或 1 时趋近 0，对应两端饱和区"学不动"。

## 讲深一层

- σ'(x) = σ(x)(1-σ(x)) 的推导：σ = 1/(1+e^-x)，两边求导化简即得
- Tanh 导数最大 1（x=0 处），比 Sigmoid 强一档，这是 Tanh 常做隐层激活的原因之一

## 高频追问

1. 为什么 Sigmoid 容易梯度消失？——两端饱和时 σ' → 0
2. 交叉熵 + Sigmoid 组合为什么能缓解？——梯度里 σ' 被约掉，误差项直接是 (σ-y)

## 易错点

- 凭"最大斜率看起来挺陡"选 1——代数上就是 0.25

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 华为 | AI 软件 | 笔试 | https://www.nowcoder.com/discuss/948632550891593728 | 社区经验 |

## 关联项目

- `深度学习基础` Q-4701

## 来源

牛客面经 华为·AI 软件·笔试（11 月 6 日）：https://www.nowcoder.com/discuss/948632550891593728
