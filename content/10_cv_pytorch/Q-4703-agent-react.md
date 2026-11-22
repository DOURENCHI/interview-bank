---
id: Q-4703
title: "Agent 范式 ReAct 的名字是哪两个英文单词拼起来的？"
module: 10_cv_pytorch
sub: Agent 与工具调用
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

**题目**（华为 AI 笔试）：Agent 范式 ReAct 的名字，是哪两个英文单词拼在一起？
A. Reasoning 与 Acting　B. Read 与 Act　C. Recall 与 Activation　D. Real 与 Action

## 口述答案

> 选 A。ReAct = Reasoning + Acting，出自 2022 年论文《ReAct: Synergizing Reasoning and Acting in Language Models》。它的核心循环是"想一步、做一步、看结果再想"：模型先输出一段推理（Thought），决定调用哪个工具（Action），拿到环境返回（Observation），再进入下一轮 Thought——推理和行动交替，而不是一次性规划到底。这名字的巧妙在于 ReAct 也谐音 react（对外界反馈作出反应），呼应"根据观察调整下一步"的设计。对比纯 CoT：CoT 只推理不与环境交互；对比纯 Act：只有动作没有推理链，容易盲目调用。

## 讲深一层

- 循环结构：Thought → Action → Observation → Thought → … → Final Answer
- 停止条件：模型输出 Final Answer，或达到最大轮数

## 高频追问

1. ReAct 和 Function Calling 什么关系？——Function Calling 是工具接口层，ReAct 是编排范式
2. ReAct 常见失败模式？——观察无关信息带偏推理，需要 prompt 里给few-off 示例约束

## 易错点

- 编成 "React 框架"——和前端 React 无关
- 只答"推理+行动"的中文，说不出英文原词

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 华为 | AI 软件 | 笔试 | https://www.nowcoder.com/discuss/945497946403971072 | 社区经验 |

## 关联项目

- `大模型与推理` Q-4707/Q-4708

## 来源

牛客面经 华为·AI 软件·笔试（10 月 28 日）：https://www.nowcoder.com/discuss/945497946403971072
