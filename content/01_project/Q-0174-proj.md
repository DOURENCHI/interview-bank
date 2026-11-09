---
id: Q-0174
title: Dice、IoU、HD95 你各报哪个？为什么只报 Dice 不够？
module: 01_project
sub: 跟骨分割（科研）
priority: P1
difficulty: 3
roles: [AI算法, 感知]
companies: [联影医疗, 迈瑞医疗, 西门子医疗]
qtype: project
status: indexed
source_type: self_exp
source_ref: 方向与规划/项目/跟骨（数据集 / 预处理 / result，未成文）
verified_at: 2026-11-09
tags: [项目深挖, 医学影像, U-Net, 图文, 待填答案]
auto: true
proj_seed: true
---

## 题目

**问**：评价指标怎么选？论文里分割几乎都报 Dice，这样够吗？

<svg viewBox="0 0 860 340" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="unar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="340" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">U-Net：下采样抓语义，上采样回分辨率，跳跃连接补细节</text>
<text x="20" y="48" font-size="12" fill="#665c49">医学影像分割的主力结构，跟骨 X 光也是这条路线</text>
<text x="135" y="76" font-size="12" font-weight="700" fill="#1b5e8c" text-anchor="middle">编码器</text>
<text x="375" y="76" font-size="12" font-weight="700" fill="#2e6b3e" text-anchor="middle">解码器</text>
<rect x="60" y="88" width="150" height="26" rx="4" fill="#1b5e8c" opacity="0.85"/><text x="60" y="83" font-size="10" fill="#665c49">512×512</text><rect x="60" y="126" width="110" height="26" rx="4" fill="#1b5e8c" opacity="0.71"/><text x="60" y="121" font-size="10" fill="#665c49">256×256</text><rect x="60" y="164" width="74" height="26" rx="4" fill="#1b5e8c" opacity="0.57"/><text x="60" y="159" font-size="10" fill="#665c49">128×128</text><rect x="60" y="202" width="46" height="26" rx="4" fill="#1b5e8c" opacity="0.43"/><text x="60" y="197" font-size="10" fill="#665c49">64×64</text><rect x="60" y="240" width="26" height="26" rx="4" fill="#1b5e8c" opacity="0.29"/><text x="60" y="235" font-size="10" fill="#665c49">32×32</text><rect x="300" y="88" width="26" height="26" rx="4" fill="#2e6b3e" opacity="0.28"/><rect x="300" y="126" width="46" height="26" rx="4" fill="#2e6b3e" opacity="0.42"/><rect x="300" y="164" width="74" height="26" rx="4" fill="#2e6b3e" opacity="0.56"/><rect x="300" y="202" width="110" height="26" rx="4" fill="#2e6b3e" opacity="0.70"/><rect x="300" y="240" width="150" height="26" rx="4" fill="#2e6b3e" opacity="0.84"/><path d="M210,101 L300,101" fill="none" stroke="#9a5a12" stroke-width="1.4" stroke-dasharray="5 3"/><path d="M170,139 L300,139" fill="none" stroke="#9a5a12" stroke-width="1.4" stroke-dasharray="5 3"/><path d="M134,177 L300,177" fill="none" stroke="#9a5a12" stroke-width="1.4" stroke-dasharray="5 3"/><path d="M106,215 L300,215" fill="none" stroke="#9a5a12" stroke-width="1.4" stroke-dasharray="5 3"/><path d="M86,253 L300,253" fill="none" stroke="#1b5e8c" stroke-width="1.8"/><text x="193" y="272" font-size="10" fill="#1b5e8c" text-anchor="middle">瓶颈</text>
<text x="470" y="112" font-size="12" font-weight="700" fill="#9a5a12">橙色虚线 = 跳跃连接</text>
<text x="470" y="132" font-size="11" fill="#2d2a21">把下采样前的高分辨率特征直接拼到上采样，</text>
<text x="470" y="149" font-size="11" fill="#2d2a21">补回池化丢掉的边界信息。</text>
<text x="470" y="178" font-size="12" font-weight="700" fill="#a63a2e">跟骨的难点不在结构，在边界：</text>
<text x="470" y="196" font-size="11" fill="#2d2a21">骨与软组织灰度接近，边缘本就模糊，</text>
<text x="470" y="213" font-size="11" fill="#2d2a21">所以 Dice 高不代表边界准，要配 HD95。</text>
<text x="20" y="306" font-size="11" fill="#665c49">编码器逐层减半分辨率、通道加倍，解码器反向恢复；跳跃连接共 4 条，对应前 4 层。</text>
</svg>

## 口述答案

> 待补充。核心：Dice 对小目标梯度友好；但 Dice 高不代表边界准，要配 HD95。

## 讲深一层

关系：`Dice = 2·IoU / (1 + IoU)`，单调对应但数值不同。

| 指标 | 衡量什么 | 盲区 |
|---|---|---|
| Dice | 区域重叠 | 边界粗糙时仍可能很高 |
| IoU | 区域重叠（更严格） | 小目标梯度弱 |
| HD95 | **边界距离** | 对内部填充不敏感 |

医学影像常见做法：Dice + HD95 一起报，一个看区域一个看边界。

## 高频追问

> 待补充。

## 易错点

- ❌ 只报 Dice 不报边界指标
- ❌ 不说明是几折的均值 ± 标准差
- ✅ 分清「区域指标 vs 边界指标」

## 关联项目

- `方向与规划/项目/跟骨（数据集 / 预处理 / result，未成文）`（`result/`）
