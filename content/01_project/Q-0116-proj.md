---
id: Q-0116
title: 分发包跑 --ep trt 只得到 5.25ms，看着「能用但慢」，问题在哪？
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

**现象**：用分发包里的 exe 跑 `--ep trt`，测出 5.25 ms，比预期的 3.22 ms 慢不少。
参数明明传了。

**问**：可能是什么原因？

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

> 因为分发包里的 exe 是**加 `--ep` 参数之前的旧版本**（387 KB vs 443 KB），
> 它根本不认识这个参数，默默忽略了，实际跑的还是 CUDA EP。
> 我一开始以为是 TRT 性能不达预期，查了半天。
> 后来在打包脚本里记录**每个产物的 sha256**，跑测前先核对版本，才杜绝这类问题。

## 讲深一层

这类「测的不是你以为的那个东西」：

| 形态 | 表现 |
|---|---|
| 旧二进制 | 参数被忽略，行为是默认值 |
| 旧配置 | 改了源文件但没重新部署 |
| 缓存 | 读到上次的构建产物 |

对策：**给每个产物算 hash 并记录**，测前核对；或程序启动时打印版本号。

## 高频追问

1. **怎么快速判断 exe 版本？** —— 看大小、看启动打印的 version、算 sha256。
2. **为什么不加版本号参数？** —— 应该加，这是补救措施。
3. **CI 里怎么防？** —— 构建产物带 git commit hash。

## 易错点

- ❌ 测出异常数字先怀疑性能 —— 先确认测的是不是新版本
- ❌ 拷错文件不校验
- ✅ 产物带 hash/版本号是最省事的防线

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §A3 踩过的坑一览（第 22 条）
