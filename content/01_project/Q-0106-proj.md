---
id: Q-0106
title: 踩过最隐蔽的一个坑是什么？
module: 01_project
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

**背景**：部署实施记录里整理了 27 条踩坑记录。

**问**：哪一条最隐蔽？为什么难发现？

<svg viewBox="0 0 860 230" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="ypar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="230" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">从权重到上车：四段链路</text>
<text x="20" y="48" font-size="12" fill="#665c49">每一段的产物格式不同，出问题时先定位是哪一段</text>

<rect x="20" y="70" width="150" height="66" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="95" y="96" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">① best.pt</text>
<text x="95" y="116" font-size="11" fill="#2d2a21" text-anchor="middle">PyTorch 权重</text>
<text x="95" y="130" font-size="11" fill="#665c49" text-anchor="middle">mAP50 0.680 (test)</text>

<rect x="196" y="70" width="150" height="66" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="271" y="96" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">② ONNX</text>
<text x="271" y="116" font-size="11" fill="#2d2a21" text-anchor="middle">9.41 MB</text>
<text x="271" y="130" font-size="11" fill="#665c49" text-anchor="middle">opset 固定 / 动态轴</text>

<rect x="372" y="70" width="150" height="66" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="447" y="96" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">③ engine</text>
<text x="447" y="116" font-size="11" fill="#2d2a21" text-anchor="middle">11.79 MB</text>
<text x="447" y="130" font-size="11" fill="#665c49" text-anchor="middle">绑显卡与 TRT 版本</text>

<rect x="548" y="70" width="150" height="66" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="623" y="96" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">④ C++ 推理</text>
<text x="623" y="116" font-size="11" fill="#2d2a21" text-anchor="middle">7.94 ms 端到端</text>
<text x="623" y="130" font-size="11" fill="#665c49" text-anchor="middle">CUDA / TRT EP</text>

<rect x="724" y="70" width="150" height="66" rx="8" fill="#f3e9d2" stroke="#dbcba5"/>
<text x="799" y="96" font-size="13" font-weight="700" fill="#1b5e8c" text-anchor="middle">⑤ ROS2 节点</text>
<text x="799" y="116" font-size="11" fill="#2d2a21" text-anchor="middle">自定义 msg</text>
<text x="799" y="130" font-size="11" fill="#665c49" text-anchor="middle">QoS SensorData</text>

<line x1="170" y1="103" x2="192" y2="103" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#ypar)"/>
<line x1="346" y1="103" x2="368" y2="103" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#ypar)"/>
<line x1="522" y1="103" x2="544" y2="103" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#ypar)"/>
<line x1="698" y1="103" x2="720" y2="103" stroke="#1b5e8c" stroke-width="1.6" marker-end="url(#ypar)"/>
<text x="20" y="172" font-size="12" fill="#a63a2e">最容易翻车的两处：</text>
<text x="20" y="192" font-size="12" fill="#2d2a21">· ONNX 导出漏动态轴 → engine 只能按固定分辨率跑，换输入就重建</text>
<text x="20" y="210" font-size="12" fill="#2d2a21">· engine 绑显卡型号与 TRT 版本 → 换机器必须重建，不能直接下发</text>
</svg>

## 口述答案

> 最隐蔽的是**推理静默回落到 CPU**。现象是结果全对，只是慢了十倍。
> 因为 ONNX Runtime 在 GPU provider 初始化失败时会自动降级用 CPU，**不报错、不警告**，
> 我的程序照常出结果，只有看时间才发现不对。
> 后来我在初始化后加了一句断言：检查实际生效的 provider 列表，不是 TRT 就直接退出。
> 这种 bug 靠肉眼永远发现不了——因为输出是对的。

## 讲深一层

为什么这类 bug 特别危险：

| 特征 | 后果 |
|---|---|
| 不报错 | 测试用例全过 |
| 结果正确 | 功能验证发现不了 |
| 只影响性能 | 不测时间就永远不知道 |

同类问题还有：`torch` 自动选 CPU、OpenCV 用了非优化后端、矩阵库回落到参考实现。
共同特征都是**「有快路径，但静默回落到慢路径」**。

防这类问题的通用手段：**启动时断言实际生效的加速路径**，而不是相信配置写了就对。

## 高频追问

1. **怎么查生效的 provider？** —— `session.get_providers()` 看返回列表。
2. **为什么初始化会失败还不报？** —— 设计上希望程序能跑起来，所以降级；但这个宽容在部署场景有害。
3. **还有别的静默降级吗？** —— 有。CUDA 版本不匹配时某些库也会悄悄用 CPU 实现。

## 易错点

- ❌ 只说「遇到过性能问题」 —— 说不出机制等于没解决
- ❌ 优化完不验证是否真的生效 —— 可能一直在跑 CPU
- ✅ 讲清「结果对所以没发现」这个反直觉点，最体现工程感

## 关联项目

- `YOLO_部署实施记录.html` §A3 踩过的坑一览（27 条）
- 同文档 §如果重做一遍，我会改五件事（第 2 条）

## 来源

本人项目实测

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
