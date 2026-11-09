---
id: Q-0138
title: 怎么证明模型学到的是骨头，而不是数据集的伪影？
module: 01_project
sub: 跟骨分割（科研）
priority: P0
difficulty: 3
roles: [系统工程, 感知]
companies: []
qtype: project
status: indexed
source_type: self_exp
source_ref: 方向与规划/项目/跟骨（数据集与预处理，未成文）
verified_at: 2026-11-09
tags: [项目深挖, 医学影像, 图文]
auto: true
proj_seed: true
---

## 题目

**背景**：X 光片常有体位标记、铅字、设备水印，模型可能「抄近路」。

**问**：怎么排查？

<svg viewBox="0 0 860 330" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif" role="img"><defs><marker id="unar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#1b5e8c"/></marker></defs>
<rect x="0" y="0" width="860" height="330" fill="#fffcf3"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="#2d2a21">U-Net：下采样抓语义，上采样回分辨率，跳跃连接补细节</text>
<text x="20" y="48" font-size="12" fill="#665c49">医学影像分割的主力结构，跟骨 X 光也是这条路线</text>

<rect x="60" y="78" width="150" height="26" rx="4" fill="#1b5e8c" opacity="0.85"/>
<text x="216" y="95" font-size="10" fill="#665c49">512×512</text>

<rect x="60" y="116" width="110" height="26" rx="4" fill="#1b5e8c" opacity="0.70"/>
<text x="176" y="133" font-size="10" fill="#665c49">256×256</text>

<rect x="60" y="154" width="74" height="26" rx="4" fill="#1b5e8c" opacity="0.55"/>
<text x="140" y="171" font-size="10" fill="#665c49">128×128</text>

<rect x="60" y="192" width="46" height="26" rx="4" fill="#1b5e8c" opacity="0.40"/>
<text x="112" y="209" font-size="10" fill="#665c49">64×64</text>

<rect x="60" y="230" width="26" height="26" rx="4" fill="#1b5e8c" opacity="0.28"/>
<text x="92" y="247" font-size="10" fill="#665c49">32×32</text>

<rect x="300" y="230" width="26" height="26" rx="4" fill="#2e6b3e" opacity="0.28"/>
<text x="332" y="247" font-size="10" fill="#665c49"></text>

<rect x="300" y="192" width="46" height="26" rx="4" fill="#2e6b3e" opacity="0.40"/>
<text x="352" y="209" font-size="10" fill="#665c49"></text>

<rect x="300" y="154" width="74" height="26" rx="4" fill="#2e6b3e" opacity="0.55"/>
<text x="380" y="171" font-size="10" fill="#665c49"></text>

<rect x="300" y="116" width="110" height="26" rx="4" fill="#2e6b3e" opacity="0.70"/>
<text x="416" y="133" font-size="10" fill="#665c49"></text>

<rect x="300" y="78" width="150" height="26" rx="4" fill="#2e6b3e" opacity="0.85"/>
<text x="456" y="95" font-size="10" fill="#665c49"></text>

<path d="M178,80 L300,80"
      fill="none" stroke="#9a5a12" stroke-width="1.3" stroke-dasharray="5 3"/>

<path d="M152,118 L300,118"
      fill="none" stroke="#9a5a12" stroke-width="1.3" stroke-dasharray="5 3"/>

<path d="M188,156 L300,156"
      fill="none" stroke="#9a5a12" stroke-width="1.3" stroke-dasharray="5 3"/>

<path d="M224,194 L300,194"
      fill="none" stroke="#9a5a12" stroke-width="1.3" stroke-dasharray="5 3"/>

<text x="470" y="120" font-size="12" font-weight="700" fill="#9a5a12">橙色虚线 = 跳跃连接</text>
<text x="470" y="140" font-size="11" fill="#2d2a21">把下采样前的高分辨率特征直接拼到上采样，</text>
<text x="470" y="157" font-size="11" fill="#2d2a21">补回池化丢掉的边界信息。</text>
<text x="470" y="186" font-size="12" font-weight="700" fill="#a63a2e">跟骨的难点不在结构，在边界：</text>
<text x="470" y="204" font-size="11" fill="#2d2a21">骨与软组织灰度接近，边缘本就模糊，</text>
<text x="470" y="221" font-size="11" fill="#2d2a21">所以 Dice 高不代表边界准，要配 HD95。</text>
<text x="20" y="270" font-size="11" fill="#665c49">蓝色 = 编码器（下采样，感受野变大）　绿色 = 解码器（上采样，恢复分辨率）</text>
</svg>

## 口述答案

> 待补充。这是医学影像面试的高频追问，答好很加分。

## 讲深一层

| 手段 | 做法 |
|---|---|
| 注意力可视化 | Grad-CAM 看关注区是否落在骨头上 |
| 消融伪影 | 遮挡可疑区域，看 Dice 是否骤降 |
| 跨中心验证 | 换一家医院的数据测 |
| 错误样本分析 | 挑失败案例分析共性 |

核心逻辑：**若模型依赖伪影，去掉伪影后性能应大幅下降**。

## 高频追问

待补充。

## 易错点

- ❌ 只做同分布测试就宣称泛化好
- ✅ 主动说「只验证过单中心，这是局限」

## 关联项目

- `方向与规划/项目/跟骨/result`

## 来源

医学影像的 shortcut learning 问题

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
