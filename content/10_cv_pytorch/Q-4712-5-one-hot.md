---
id: Q-4712
title: "5 万词的词表，One-Hot 表示一个词的维度由什么决定？"
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
nc_url: https://www.nowcoder.com/discuss/945497946403971072
---

## 题目

**题目**（华为 AI 笔试）：某模型的词表中共有 5 万个词，用 One-Hot 向量表示其中某一个词。该向量的维度由什么决定？

## 口述答案

> 由**词表大小**决定：5 万词的 One-Hot 就是 5 万维，每个词对应一个位置为 1、其余全 0 的向量——维度等于词汇表容量，与单个词本身的长短、频率都无关。顺带把 One-Hot 的两个经典问题说全：一是维度大且稀疏，5 万维里只有一个 1，直接当输入层参数量爆炸，所以实践里紧跟一个 embedding 矩阵把它压到几百维稠密向量；二是任意两个词的 One-Hot 都正交，表达不出"猫和狗相近、猫和汽车更远"这类语义关系，embedding 恰好也解决这个问题——训练后的向量距离承载语义。

## 讲深一层

```
One-Hot:  V = 50000 维, 一个 1，其余 0
Embedding: E ∈ R^(50000 × d)，查表得 d 维稠密向量
```
- Embedding 层参数量 = 词表 × d；5 万 × 768 ≈ 3840 万，这就是为什么大模型词表不能随便加词

## 高频追问

1. One-Hot 直接喂网络有什么问题？——稀疏、无语义、维度灾难
2. Embedding 查表的实现本质是什么？——One-Hot 矩阵乘的等价物，实现为按索引取行

## 易错点

- 说维度由"句长"或"模型隐藏层"决定

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 华为 | AI 软件 | 笔试 | https://www.nowcoder.com/discuss/945497946403971072 | 社区经验 |

## 关联项目

- `深度学习基础` Q-4611

## 来源

牛客面经 华为·AI 软件·笔试（10 月 28 日）：https://www.nowcoder.com/discuss/945497946403971072
