---
id: Q-0107
title: 对比 pt 和 ONNX 的输出差异很大，为什么怀疑是「没做 fuse」？
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

**现象**：拿原始 `.pt` 和导出的 ONNX 比对检测结果，数值差异大得可疑。

**问**：可能是什么原因？对比前该做什么？

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

> 大概率是**对比的基线不对**：`.pt` 没做 `model.fuse()`，而导出 ONNX 时
> Conv+BN 会被融合成一层。两个图结构不同，输出自然有差。
> 正确做法是对比前先 `model.fuse()`，让两边结构一致，剩下的差异才是导出引入的。
> 这是「先对齐基线再比」的通用原则。

## 讲深一层

fuse 做了什么：把 Conv 和紧跟的 BatchNorm 合并成一个卷积，
权重按 `W' = W * γ / sqrt(σ² + ε)` 重算，BN 偏置并入 Conv 偏置。

| 对比方式 | 差异来源 |
|---|---|
| 未 fuse vs 已 fuse 的 ONNX | 结构性差异，无意义 |
| 已 fuse pt vs ONNX | 导出引入的差异，有意义 |

## 高频追问

1. **fuse 会掉精度吗？** —— 数值上有微小差异，但数学上等价。
2. **怎么确认 fuse 生效了？** —— 打印模型结构，看 BN 层是否消失。
3. **还有别的基线错位吗？** —— 有，输入归一化方式不同、letterbox 参数不同。

## 易错点

- ❌ 直接比 pt 和 ONNX —— 基线不同，结论不可信
- ❌ 看到差异大就怀疑量化 —— 先排除结构差异
- ✅ 说清「先对齐基线再比」

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §A3 踩过的坑一览（第 2 条）
