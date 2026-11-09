---
id: Q-0136
title: 数据量小的时候你怎么防止过拟合？
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

**问**：医学影像标注通常只有几百例，U-Net 参数量又不小，怎么防过拟合？你实际用了哪几种？

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

> 待补充。给出实际用了哪几种，并说明各自效果差异（有消融最好）。

## 讲深一层

| 手段 | 作用 | 代价 |
|---|---|---|
| 数据增强 | 扩充多样性 | 过强会引入伪影 |
| 迁移学习 | 好的初始特征 | 域差异大时收益有限 |
| 强正则 | 抑制过拟合 | 可能欠拟合 |
| 小模型 / 深监督 | 降容量 | 精度上限下降 |
| K 折交叉验证 | 评估更可靠 | 成本 × K |

关键：**增强必须符合成像物理**。X 光弹性形变过度会让骨骼形态失真，模型学到假特征。

## 高频追问

待补充。

## 易错点

- ❌ 列一堆手段说不出哪个起作用 —— 需要消融
- ❌ 强增强不检查是否引入伪影
- ✅ 说清「验证集上过拟合的表现」：训练 loss 降、验证 Dice 不涨

## 关联项目

- `方向与规划/项目/跟骨/result`

## 来源

本人课题实践

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| — | — | — | — | 待填 | — |
