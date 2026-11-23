---
id: Q-0109
title: 只拷了 onnxruntime.dll，为什么 CUDA 还是不生效？
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

**场景**：做分发包时手工把 `onnxruntime.dll` 拷过去，程序能跑，但没有 GPU 加速。

**问**：缺了什么？怎么避免这类问题？

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

> 缺了 `onnxruntime_providers_shared.dll`。ORT 的 provider（CUDA、TensorRT）是插件式加载，
> 主 DLL 只是壳，provider 实现在单独的 DLL 里。
> 后来改成用 `onnxruntime*.dll` 通配符全拷，而不是逐个点名。
> 更彻底的是写脚本递归收集依赖，最后收集到 44 个 DLL。

## 讲深一层

| 做法 | 可靠性 | 成本 |
|---|---|---|
| 手工点名拷 | 低，漏一个就静默降级 | 人工 |
| 通配符 `onnxruntime*.dll` | 中 | 低 |
| 脚本递归收集 | 高 | 前期投入 |

关键：**缺 DLL 不一定报错**，可能只是少一个 provider，于是静默降级。

## 高频追问

1. **怎么知道还缺哪些 DLL？** —— 干净环境跑一遍看提示，或用 Dependencies 工具。
2. **为什么不静态链接？** —— 踩过坑，`-static-libstdc++` 会带来别的问题。
3. **44 个 DLL 太多？** —— 可以打包成安装程序，但不能省。

## 易错点

- ❌ 只拷主 DLL —— provider 不在里面
- ❌ 在开发机测一遍就以为好了 —— 开发机 PATH 里有
- ✅ 一定要在干净环境验证

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §A3 踩过的坑一览（第 4、9 条）
