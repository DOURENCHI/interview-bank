---
id: Q-0101
title: 从 best.pt 到能在 C++ 里出结果，整条链路分几段？每段的产物和风险是什么？
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

**背景**：road-traffic 道路场景 12 类，模型 YOLO26n，RTX 5060 Laptop（8 GB），
测试集 mAP50 = 0.680。但这个权重只能在装了 PyTorch 的 Python 里跑，
要交付的是「别人不装 Python 也能跑」的目标检测程序。

**已知**：ONNX 9.41 MB，TensorRT FP16 engine 11.79 MB，分发包 exe + 44 个 DLL 共 78.7 MB。

**问**：中间经过哪几步？每一步的产物能不能直接给客户？

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

> 四段：pt 导 ONNX、ONNX 建 engine、C++ 用 Runtime 加载推理、包成 ROS2 节点。
> 每段产物格式不同，出问题先定位是哪段。
> 关键判断是 **engine 不能交付**——它绑显卡架构和 TensorRT 版本，换机器就加载失败。
> 所以我给的是 exe + DLL + ONNX，engine 在目标机首次运行时现场生成再缓存。

## 讲深一层

| 段 | 产物 | 大小 | 可移植 |
|---|---|---|---|
| ① pt | 权重 | — | 能 |
| ② ONNX | `.onnx` | 9.41 MB | 能，格式中立 |
| ③ engine | `.engine` | 11.79 MB | **不能** |
| ④ 可执行 | exe + 44 DLL | 78.7 MB | 能，需另带 CUDA 运行库 |

engine 本质更接近「编译产物」而不是模型文件。

## 高频追问

1. **现场建 engine 要多久？** —— 分钟量级，可做首启动预生成 + 进度提示。
2. **缓存放哪？** —— 用户目录，用显卡型号 + TRT 版本做 key。
3. **没 GPU 的机器？** —— 降级 CPU EP，但要提前告知性能预期。

## 易错点

- ❌ 把 engine 当模型文件下发 —— 客户机器跑不起来
- ❌ 只测 ONNX 不测导出后精度 —— 换后处理路径会掉点
- ✅ 主动讲「为什么不能交付 engine」，这是工程判断不是流程描述

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §交付形态：什么能交、什么不该交
- 同文档 §几笔「代价账」
