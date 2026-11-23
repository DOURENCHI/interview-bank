---
id: Q-0108
title: 检测框坐标的「绝对误差」看着很大，这一定说明精度差吗？
module: project
sub: YOLO 部署
priority: P0
difficulty: 2
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

**现象**：比对输出时发现框坐标的绝对误差有好几个像素，看着明显不对。

**问**：这个数字该怎么读？

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

> 要看坐标的量级。YOLO 输出的框坐标是 **0–640 像素量级**，不是 0–1 归一化。
> 几个像素的绝对误差换算成相对误差不到 1%，完全正常。
> 所以我改看相对误差，以及**结果层**的差异（框数、类别、置信度），而不是原始坐标的绝对值。
> 这是「误差要和量纲一起看」的常识，但很容易被忽略。

## 讲深一层

| 指标 | 适合判断 |
|---|---|
| 绝对误差 | 同量纲下比较 |
| 相对误差 | 跨量纲、跨分辨率 |
| 结果层差异（框数/类别/mAP） | 真正影响业务 |

mAP 的下降才是最终判据，坐标误差只是中间过程量。

## 高频追问

1. **0.5 像素误差算大吗？** —— 相对 640 是 0.08%，可忽略。
2. **为什么结果层更重要？** —— 业务只关心检测对不对。
3. **什么时候该看绝对值？** —— 同分辨率、同量纲下做回归对比。

## 易错点

- ❌ 看到绝对误差大就下结论
- ❌ 不换算量纲直接比
- ✅ 先问「坐标是归一化还是像素」

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §A3 踩过的坑一览（第 3 条）
