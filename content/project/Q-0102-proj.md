---
id: Q-0102
title: 端到端 7.94ms、纯推理 3.22ms，中间那 4.7ms 花在哪？
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

**实测**（本机，1280×720，两轮 × 1000 帧）：

| 路径 | 纯推理 | 端到端 |
|---|---|---|
| Python + PyTorch | 11.70 | 14.96 |
| Python + ONNX Runtime | 7.10 | 12.71 |
| C++ + CUDA EP | 6.23 | 13.31 |
| C++ + TensorRT EP | 3.22 | **7.94** |
| 纯 TensorRT（不走 ORT） | 1.97 | — |

**问**：端到端里除推理外还有什么？为什么纯推理省了 1.25 ms，端到端没同比例降？

<svg viewBox="0 0 860 330" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="ylat" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="330" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">端到端延迟演进（ms，本机实测）</text>
<text x="20" y="48" font-size="12" fill="#665c49">条越长越慢。红色那条是反例：套了两层封装，比原生还慢</text>

<text x="196" y="86" font-size="12" fill="#2d2a21" text-anchor="end">Python + PyTorch</text>
<rect x="206" y="71" width="560" height="22" rx="4" fill="#665c49" opacity="0.85"/>
<text x="774" y="86" font-size="12" font-weight="700" fill="#665c49">14.96</text>

<text x="196" y="118" font-size="12" fill="#2d2a21" text-anchor="end">Python + ORT</text>
<rect x="206" y="103" width="476" height="22" rx="4" fill="#1b5e8c" opacity="0.85"/>
<text x="690" y="118" font-size="12" font-weight="700" fill="#1b5e8c">12.71</text>

<text x="196" y="150" font-size="12" fill="#2d2a21" text-anchor="end">Python 套框架封装</text>
<rect x="206" y="135" width="474" height="22" rx="4" fill="#a63a2e" opacity="0.85"/>
<text x="688" y="150" font-size="12" font-weight="700" fill="#a63a2e">12.65 反例</text>

<text x="196" y="182" font-size="12" fill="#2d2a21" text-anchor="end">C++ + CUDA EP</text>
<rect x="206" y="167" width="498" height="22" rx="4" fill="#12666e" opacity="0.85"/>
<text x="712" y="182" font-size="12" font-weight="700" fill="#12666e">13.31</text>

<text x="196" y="214" font-size="12" fill="#2d2a21" text-anchor="end">C++ + TensorRT EP</text>
<rect x="206" y="199" width="297" height="22" rx="4" fill="#2e6b3e" opacity="0.85"/>
<text x="511" y="214" font-size="12" font-weight="700" fill="#2e6b3e">7.94</text>

<line x1="206" y1="70" x2="206" y2="228" stroke="#dbcba5" stroke-width="1"/>
<text x="20" y="262" font-size="12" fill="#2d2a21">纯推理 vs 端到端要分开看：纯 TensorRT 只要 1.97 ms，但端到端 7.94 ms ——</text>
<text x="20" y="280" font-size="12" fill="#2d2a21">中间的 6 ms 是采集、预处理、后处理、拷贝，优化推理只能解决其中一部分。</text>
<text x="20" y="306" font-size="11" fill="#a63a2e">纪律：不同次测量之间只比相对值，不跨口径比绝对值。</text>
</svg>

## 口述答案

> 端到端 = 采集 + 预处理 + 推理 + 后处理 + 结果拷贝 + 输出。
> 预处理（resize、归一化、HWC→CHW）和后处理（NMS、框还原）都是 CPU 串行工作，
> 推理越快，它们占比越高——阿姆达尔定律在部署里的直接体现。
> 我做完预处理优化后瓶颈换了位置，正好印证：优化要看边际收益，不是看单项绝对值。

## 讲深一层

| 段 | 优化手段 | 代价 |
|---|---|---|
| 预处理 | 硬件 resize、GPU 上归一化、零拷贝 | 改链路，可能引入精度差异 |
| 推理 | 量化、算子融合、换后端 | 精度、可移植性 |
| 后处理 | NMS 向量化、减候选框 | 可能漏检 |

还有一项容易漏：**每轮约 7 MB 的内存分配释放**。用分段计时相加会漏掉这部分，
导致分段和比端到端少 0.73 ms（踩坑第 15 条）。

## 高频追问

1. **怎么定位瓶颈？** —— 分段打点 + `steady_clock`，不要只测总时间。
2. **为什么分段和小于端到端？** —— 段间空隙、分配释放、缓存失效没被计入。
3. **流水线能解决吗？** —— 能重叠，但要双缓冲和线程同步，复杂度换吞吐。

## 易错点

- ❌ 只报总延迟不拆段 —— 被问「慢在哪」答不出
- ❌ 拿纯推理当端到端对外说 —— 数字好看但失真
- ❌ 拿分段相加当端到端 —— 会少算段间开销

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html` §整条链路的延迟演进
- 同文档 §预处理优化：改了之后瓶颈换位置了
