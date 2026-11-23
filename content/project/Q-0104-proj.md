---
id: Q-0104
title: FP16 掉了多少精度？为什么说「换后处理路径」的影响更大？
module: project
sub: YOLO 部署
priority: P0
difficulty: 3
roles: [系统工程, 感知]
companies: []
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html
verified_at: 2026-11-09
tags: [项目深挖, YOLO, 图文]
auto: true
proj_seed: true
---

## 题目

**实测**（valid 集 187 图 / 839 框）：

| 转换 | mAP50 | 变化 |
|---|---|---|
| pt → ONNX | 0.6407 → 0.6329 | **−0.0078** |
| ONNX → engine FP32 | 0.6329 → 0.6327 | −0.0002 |
| engine FP32 → FP16 | 0.6327 → 0.6323 | −0.0004 |

**问**：为什么降低数值精度几乎不掉点，换格式却掉了 0.0078？

<svg viewBox="0 0 860 250" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="yacc" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="250" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">每一步掉了多少精度（mAP50，valid 集 187 图 / 839 框）</text>
<text x="20" y="48" font-size="12" fill="#665c49">真正掉点在 pt→ONNX，不在精度位宽上</text>
<line x1="60" y1="80" x2="800" y2="80" stroke="#dbcba5" stroke-width="2"/>

<circle cx="110" cy="80" r="7" fill="#665c49"/>
<text x="110" y="64" font-size="12" font-weight="700" fill="#665c49" text-anchor="middle">0.6407</text>
<text x="110" y="104" font-size="11" fill="#665c49" text-anchor="middle">原始 pt</text>

<circle cx="330" cy="80" r="7" fill="#1b5e8c"/>
<text x="330" y="64" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">0.6329</text>
<text x="330" y="104" font-size="11" fill="#665c49" text-anchor="middle">ONNX</text>

<circle cx="550" cy="80" r="7" fill="#12666e"/>
<text x="550" y="64" font-size="12" font-weight="700" fill="#12666e" text-anchor="middle">0.6327</text>
<text x="550" y="104" font-size="11" fill="#665c49" text-anchor="middle">engine FP32</text>

<circle cx="750" cy="80" r="7" fill="#2e6b3e"/>
<text x="750" y="64" font-size="12" font-weight="700" fill="#2e6b3e" text-anchor="middle">0.6323</text>
<text x="750" y="104" font-size="11" fill="#665c49" text-anchor="middle">engine FP16</text>

<line x1="110" y1="140" x2="330" y2="140" stroke="#a63a2e" stroke-width="1.4" stroke-dasharray="4 3"/>
<text x="220" y="158" font-size="12" fill="#a63a2e" text-anchor="middle">−0.0078（换后处理路径）</text>
<line x1="330" y1="140" x2="750" y2="140" stroke="#2e6b3e" stroke-width="1.4" stroke-dasharray="4 3"/>
<text x="540" y="158" font-size="12" fill="#2e6b3e" text-anchor="middle">−0.0006（FP32→FP16 几乎无损）</text>
<text x="20" y="196" font-size="12" fill="#2d2a21">面试时这句最有用：FP16 掉的那点精度，比更换后处理路径的影响小一个数量级。</text>
<text x="20" y="218" font-size="12" fill="#2d2a21">所以「量化会不会掉点」的答案取决于基线 —— 基线本身换过实现，讨论量化就没意义。</text>
</svg>

## 口述答案

> 因为 ONNX 导出时后处理路径变了：原来在 PyTorch 里做的解码和 NMS，
> 导出后要么落到图里、要么挪到外面重写，实现一换结果就有细微差异。
> FP16 只降低数值精度、结构没变，所以掉 0.0004 基本可忽略。
> 结论：**掉点大头通常在实现路径，不在位宽**。所以「量化掉不掉点」得先问基线是什么。

## 讲深一层

三层验证（项目后期才建立）：

| 层 | 比什么 | 抓什么 |
|---|---|---|
| 框 | 数量、坐标 | 结构性问题 |
| 分数 | 置信度分布 | 数值精度问题 |
| 中间层 | 逐层张量 | 第一个发散的算子 |

只比框会漏「结果对但顺序不同」；只比分数会漏后处理差异。

## 高频追问

1. **FP16 为什么掉这么少？** —— 检测任务对数值扰动不敏感，TRT 会保留敏感层精度。
2. **INT8 呢？** —— 通常明显大于 FP16，需要校准集和逐层敏感度（本项目没做）。
3. **test 集为什么只用一次？** —— 用两次就是拿测试集调参，那个数不再是「没被调过」的结果。

## 易错点

- ❌ 报 FP16 无损 —— 有损，只是小
- ❌ 拿 valid 和 test 的数字混着说
- ✅ 讲出「掉点来自实现路径」这个反直觉结论

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §精度：每一步掉了多少
