#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题卡插图库：全部手写内联 SVG，不用位图、不用 mermaid。

约定（与教学文档一致）：
  - viewBox="0 0 860 <高>"，宽度自适应
  - 暖纸配色，与题库主题一致
  - 只用 SVG 元素，禁止 HTML 标签
  - 箭头用 <marker> + <path d="M0,0 L6,3 L0,6 z">
  - 每个图的 marker id 唯一，避免同页冲突
"""

C = {
    "bg": "#fffcf3", "soft": "#f3e9d2", "line": "#dbcba5",
    "tx": "#2d2a21", "mut": "#665c49",
    "blue": "#1b5e8c", "red": "#a63a2e", "green": "#2e6b3e",
    "orange": "#9a5a12", "purple": "#6b4fa8", "teal": "#12666e",
}

FONT = "-apple-system,'PingFang SC','Microsoft YaHei',sans-serif"


def _head(h: int, mid: str) -> str:
    return (f'<svg viewBox="0 0 860 {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="{FONT}" role="img">'
            f'<defs><marker id="{mid}" markerWidth="8" markerHeight="8" '
            f'refX="7" refY="3" orient="auto">'
            f'<path d="M0,0 L6,3 L0,6 z" fill="{C["blue"]}"/></marker></defs>')


# ---------------------------------------------------------------- 1. YOLO 部署链路
YOLO_PIPE = _head(230, "ypar") + f"""
<rect x="0" y="0" width="860" height="230" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">从权重到上车：四段链路</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">每一段的产物格式不同，出问题时先定位是哪一段</text>
""" + "".join(f"""
<rect x="{x}" y="70" width="150" height="66" rx="8" fill="{C['soft']}" stroke="{C['line']}"/>
<text x="{x+75}" y="96" font-size="13" font-weight="700" fill="{C['blue']}" text-anchor="middle">{t}</text>
<text x="{x+75}" y="116" font-size="11" fill="{C['tx']}" text-anchor="middle">{s1}</text>
<text x="{x+75}" y="130" font-size="11" fill="{C['mut']}" text-anchor="middle">{s2}</text>
"""
for x, t, s1, s2 in [
    (20, "① best.pt", "PyTorch 权重", "mAP50 0.680 (test)"),
    (196, "② ONNX", "9.41 MB", "opset 固定 / 动态轴"),
    (372, "③ engine", "11.79 MB", "绑显卡与 TRT 版本"),
    (548, "④ C++ 推理", "7.94 ms 端到端", "CUDA / TRT EP"),
    (724, "⑤ ROS2 节点", "自定义 msg", "QoS SensorData"),
]) + "".join(f"""
<line x1="{x1}" y1="103" x2="{x2}" y2="103" stroke="{C['blue']}" stroke-width="1.6" marker-end="url(#ypar)"/>"""
for x1, x2 in [(170, 192), (346, 368), (522, 544), (698, 720)]) + f"""
<text x="20" y="172" font-size="12" fill="{C['red']}">最容易翻车的两处：</text>
<text x="20" y="192" font-size="12" fill="{C['tx']}">· ONNX 导出漏动态轴 → engine 只能按固定分辨率跑，换输入就重建</text>
<text x="20" y="210" font-size="12" fill="{C['tx']}">· engine 绑显卡型号与 TRT 版本 → 换机器必须重建，不能直接下发</text>
</svg>"""


# ---------------------------------------------------------------- 2. 延迟演进
YOLO_LAT = _head(330, "ylat") + f"""
<rect x="0" y="0" width="860" height="330" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">端到端延迟演进（ms，本机实测）</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">条越长越慢。红色那条是反例：套了两层封装，比原生还慢</text>
""" + "".join(f"""
<text x="196" y="{y+4}" font-size="12" fill="{C['tx']}" text-anchor="end">{lab}</text>
<rect x="206" y="{y-11}" width="{w}" height="22" rx="4" fill="{col}" opacity="0.85"/>
<text x="{206+w+8}" y="{y+4}" font-size="12" font-weight="700" fill="{col}">{val}</text>
"""
for y, lab, w, val, col in [
    (82, "Python + PyTorch", 560, "14.96", C['mut']),
    (114, "Python + ORT", 476, "12.71", C['blue']),
    (146, "Python 套框架封装", 474, "12.65 反例", C['red']),
    (178, "C++ + CUDA EP", 498, "13.31", C['teal']),
    (210, "C++ + TensorRT EP", 297, "7.94", C['green']),
]) + f"""
<line x1="206" y1="70" x2="206" y2="228" stroke="{C['line']}" stroke-width="1"/>
<text x="20" y="262" font-size="12" fill="{C['tx']}">纯推理 vs 端到端要分开看：纯 TensorRT 只要 1.97 ms，但端到端 7.94 ms ——</text>
<text x="20" y="280" font-size="12" fill="{C['tx']}">中间的 6 ms 是采集、预处理、后处理、拷贝，优化推理只能解决其中一部分。</text>
<text x="20" y="306" font-size="11" fill="{C['red']}">纪律：不同次测量之间只比相对值，不跨口径比绝对值。</text>
</svg>"""


# ---------------------------------------------------------------- 3. 精度掉落
YOLO_ACC = _head(250, "yacc") + f"""
<rect x="0" y="0" width="860" height="250" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">每一步掉了多少精度（mAP50，valid 集 187 图 / 839 框）</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">真正掉点在 pt→ONNX，不在精度位宽上</text>
<line x1="60" y1="80" x2="800" y2="80" stroke="{C['line']}" stroke-width="2"/>
""" + "".join(f"""
<circle cx="{x}" cy="80" r="7" fill="{col}"/>
<text x="{x}" y="64" font-size="12" font-weight="700" fill="{col}" text-anchor="middle">{v}</text>
<text x="{x}" y="104" font-size="11" fill="{C['mut']}" text-anchor="middle">{lab}</text>
""" for x, v, lab, col in [
    (110, "0.6407", "原始 pt", C['mut']),
    (330, "0.6329", "ONNX", C['blue']),
    (550, "0.6327", "engine FP32", C['teal']),
    (750, "0.6323", "engine FP16", C['green']),
]) + f"""
<line x1="110" y1="140" x2="330" y2="140" stroke="{C['red']}" stroke-width="1.4" stroke-dasharray="4 3"/>
<text x="220" y="158" font-size="12" fill="{C['red']}" text-anchor="middle">−0.0078（换后处理路径）</text>
<line x1="330" y1="140" x2="750" y2="140" stroke="{C['green']}" stroke-width="1.4" stroke-dasharray="4 3"/>
<text x="540" y="158" font-size="12" fill="{C['green']}" text-anchor="middle">−0.0006（FP32→FP16 几乎无损）</text>
<text x="20" y="196" font-size="12" fill="{C['tx']}">面试时这句最有用：FP16 掉的那点精度，比更换后处理路径的影响小一个数量级。</text>
<text x="20" y="218" font-size="12" fill="{C['tx']}">所以「量化会不会掉点」的答案取决于基线 —— 基线本身换过实现，讨论量化就没意义。</text>
</svg>"""


# ---------------------------------------------------------------- 4. MRP 环网
MRP = _head(300, "mar") + f"""
<rect x="0" y="0" width="860" height="300" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">MRP 环网：正常态与故障态</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">IEC 62439-2 · 二层 · 正常时阻塞一个环口防广播风暴，故障时打开</text>
<text x="150" y="76" font-size="13" font-weight="700" fill="{C['blue']}" text-anchor="middle">正常态</text>
<text x="640" y="76" font-size="13" font-weight="700" fill="{C['red']}" text-anchor="middle">故障态</text>
<rect x="30" y="90" width="360" height="150" rx="10" fill="{C['soft']}" stroke="{C['line']}"/>
<rect x="470" y="90" width="360" height="150" rx="10" fill="{C['soft']}" stroke="{C['line']}"/>
""" + "".join(f"""
<circle cx="{x}" cy="{y}" r="14" fill="{C['bg']}" stroke="{C['blue']}" stroke-width="2"/>
<text x="{x}" y="{y+4}" font-size="11" font-weight="700" fill="{C['blue']}" text-anchor="middle">{n}</text>
""" for x, y, n in [(90,130,"M"),(210,130,"C"),(330,130,"C"),(210,210,"C"),(330,210,"C")]) + "".join(f"""
<circle cx="{x}" cy="{y}" r="14" fill="{C['bg']}" stroke="{C['blue']}" stroke-width="2"/>
<text x="{x}" y="{y+4}" font-size="11" font-weight="700" fill="{C['blue']}" text-anchor="middle">{n}</text>
""" for x, y, n in [(530,130,"M"),(650,130,"C"),(770,130,"C"),(650,210,"C"),(770,210,"C")]) + f"""
<line x1="104" y1="130" x2="196" y2="130" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="224" y1="130" x2="316" y2="130" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="330" y1="144" x2="330" y2="196" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="316" y1="210" x2="224" y2="210" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="210" y1="196" x2="210" y2="144" stroke="{C['line']}" stroke-width="1.6" stroke-dasharray="4 3"/>
<text x="272" y="172" font-size="11" fill="{C['red']}" text-anchor="middle">阻塞</text>
<line x1="544" y1="130" x2="636" y2="130" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="664" y1="130" x2="756" y2="130" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="770" y1="144" x2="770" y2="196" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="756" y1="210" x2="664" y2="210" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="636" y1="210" x2="544" y2="210" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="650" y1="196" x2="650" y2="144" stroke="{C['blue']}" stroke-width="1.6"/>
<line x1="210" y1="130" x2="210" y2="130" stroke="{C['red']}"/>
<text x="150" y="262" font-size="11" fill="{C['mut']}" text-anchor="middle">环逻辑上是线型，数据走单一路径</text>
<text x="650" y="262" font-size="11" fill="{C['red']}" text-anchor="middle">断一处，被阻塞的口打开，反向绕通</text>
</svg>"""


# ---------------------------------------------------------------- 5. Linux 日志数据流
LOGFLOW = _head(230, "lgar") + f"""
<rect x="0" y="0" width="860" height="230" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">日志工具的数据流：先筛后统计</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">顺序决定了报告里的数字和用户看到的筛选条件对不对得上</text>
""" + "".join(f"""
<rect x="{x}" y="74" width="146" height="62" rx="8" fill="{C['soft']}" stroke="{C['line']}"/>
<text x="{x+73}" y="99" font-size="13" font-weight="700" fill="{C['blue']}" text-anchor="middle">{t}</text>
<text x="{x+73}" y="119" font-size="11" fill="{C['mut']}" text-anchor="middle">{s}</text>
"""
for x, t, s in [
    (20, "getline 逐行读", "内存 O(1) 行"),
    (192, "关键词筛选", "过滤整行"),
    (364, "时间筛选", "HH:MM:SS 字符串比"),
    (536, "分级统计", "只统计通过的行"),
    (708, "报告输出", "终端 + 文件"),
]) + "".join(f"""
<line x1="{x1}" y1="105" x2="{x2}" y2="105" stroke="{C['blue']}" stroke-width="1.6" marker-end="url(#lgar)"/>"""
for x1, x2 in [(166, 188), (338, 360), (510, 532), (682, 704)]) + f"""
<rect x="192" y="152" width="318" height="46" rx="8" fill="#faede8" stroke="{C['red']}" stroke-dasharray="4 3"/>
<text x="351" y="172" font-size="11" fill="{C['red']}" text-anchor="middle">第一版把这两步写反了：先统计后筛选</text>
<text x="351" y="189" font-size="11" fill="{C['red']}" text-anchor="middle">结果筛了 300 行，报告总数还是 5000</text>
</svg>"""


# ---------------------------------------------------------------- 6. 二维云台开环
GIMBAL = _head(250, "gmar") + f"""
<rect x="0" y="0" width="860" height="250" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">二维云台：开环控制，没有反馈</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">SG90 舵机按脉宽定位，不回读角度 —— 这是它和闭环云台的根本差别</text>
""" + "".join(f"""
<rect x="{x}" y="78" width="130" height="58" rx="8" fill="{C['soft']}" stroke="{C['line']}"/>
<text x="{x+65}" y="102" font-size="12" font-weight="700" fill="{C['blue']}" text-anchor="middle">{t}</text>
<text x="{x+65}" y="120" font-size="11" fill="{C['mut']}" text-anchor="middle">{s}</text>
"""
for x, t, s in [
    (20, "STM32F103", "定时器 PWM"),
    (186, "PWM 50Hz", "0.5–2.5ms"),
    (352, "SG90 舵机", "180° 位置型"),
    (518, "机械支架", "水平 + 俯仰"),
    (684, "限位保护", "软件钳位"),
]) + "".join(f"""
<line x1="{x1}" y1="107" x2="{x2}" y2="107" stroke="{C['blue']}" stroke-width="1.6" marker-end="url(#gmar)"/>"""
for x1, x2 in [(150, 182), (316, 348), (482, 514), (648, 680)]) + f"""
<path d="M749,136 L749,170 L85,170 L85,138" fill="none" stroke="{C['red']}"
      stroke-width="1.4" stroke-dasharray="5 4"/>
<text x="417" y="188" font-size="11" fill="{C['red']}" text-anchor="middle">
缺反馈：角度靠脉宽推算，堵转/机械干涉都不自知</text>
<text x="20" y="216" font-size="12" fill="{C['tx']}">所以两个必做：</text>
<text x="20" y="234" font-size="12" fill="{C['tx']}">· 软件限位（钳位到 0–180° 内，避免打齿） · 独立 5V/2A 供电（舵机启动电流会拉垮板子供电）</text>
</svg>"""


# ---------------------------------------------------------------- 7. U-Net
UNET = _head(330, "unar") + f"""
<rect x="0" y="0" width="860" height="330" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">U-Net：下采样抓语义，上采样回分辨率，跳跃连接补细节</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">医学影像分割的主力结构，跟骨 X 光也是这条路线</text>
""" + "".join(f"""
<rect x="{x}" y="{y}" width="{w}" height="26" rx="4" fill="{C['blue']}" opacity="{op}"/>
<text x="{x+w+6}" y="{y+17}" font-size="10" fill="{C['mut']}">{t}</text>
"""
for x, y, w, op, t in [
    (60,  78, 150, "0.85", "512×512"),
    (60, 116, 110, "0.70", "256×256"),
    (60, 154,  74, "0.55", "128×128"),
    (60, 192,  46, "0.40", "64×64"),
    (60, 230,  26, "0.28", "32×32"),
]) + "".join(f"""
<rect x="{x}" y="{y}" width="{w}" height="26" rx="4" fill="{C['green']}" opacity="{op}"/>
<text x="{x+w+6}" y="{y+17}" font-size="10" fill="{C['mut']}">{t}</text>
"""
for x, y, w, op, t in [
    (300, 230,  26, "0.28", ""),
    (300, 192,  46, "0.40", ""),
    (300, 154,  74, "0.55", ""),
    (300, 116, 110, "0.70", ""),
    (300,  78, 150, "0.85", ""),
]) + "".join(f"""
<path d="M{178 if i==0 else 116+i*36},{80+i*38} L{300 if i==0 else 300},{80+i*38}"
      fill="none" stroke="{C['orange']}" stroke-width="1.3" stroke-dasharray="5 3"/>
"""
for i in range(4)) + f"""
<text x="470" y="120" font-size="12" font-weight="700" fill="{C['orange']}">橙色虚线 = 跳跃连接</text>
<text x="470" y="140" font-size="11" fill="{C['tx']}">把下采样前的高分辨率特征直接拼到上采样，</text>
<text x="470" y="157" font-size="11" fill="{C['tx']}">补回池化丢掉的边界信息。</text>
<text x="470" y="186" font-size="12" font-weight="700" fill="{C['red']}">跟骨的难点不在结构，在边界：</text>
<text x="470" y="204" font-size="11" fill="{C['tx']}">骨与软组织灰度接近，边缘本就模糊，</text>
<text x="470" y="221" font-size="11" fill="{C['tx']}">所以 Dice 高不代表边界准，要配 HD95。</text>
<text x="20" y="270" font-size="11" fill="{C['mut']}">蓝色 = 编码器（下采样，感受野变大）　绿色 = 解码器（上采样，恢复分辨率）</text>
</svg>"""


# ---------------------------------------------------------------- 8. 毕设四层链路
DIPLOMA = _head(240, "dpar") + f"""
<rect x="0" y="0" width="860" height="240" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">本科毕设：四层链路</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">题目的落脚点是「链路可行性验证」，不是「精度达标的测温仪」</text>
""" + "".join(f"""
<rect x="{x}" y="74" width="140" height="64" rx="8" fill="{C['soft']}" stroke="{C['line']}"/>
<text x="{x+70}" y="98" font-size="12" font-weight="700" fill="{C['blue']}" text-anchor="middle">{t}</text>
<text x="{x+70}" y="116" font-size="10" fill="{C['tx']}" text-anchor="middle">{s}</text>
<text x="{x+70}" y="130" font-size="10" fill="{C['mut']}" text-anchor="middle">{s2}</text>
"""
for x, t, s, s2 in [
    (20, "DHT11", "单总线 40 位", "0–50℃ ±2℃"),
    (184, "STM32F103", "寄存器配 GPIO", "关中断读脉宽"),
    (348, "RS485", "差分传输", "抗共模干扰"),
    (512, "4G DTU", "Cat.1 透传", "AT 指令 + 超时"),
    (676, "云端", "曲线与展示", "注册包判据"),
]) + "".join(f"""
<line x1="{x1}" y1="106" x2="{x2}" y2="106" stroke="{C['blue']}" stroke-width="1.6" marker-end="url(#dpar)"/>"""
for x1, x2 in [(160, 180), (324, 344), (488, 508), (652, 672)]) + f"""
<rect x="348" y="160" width="304" height="50" rx="8" fill="#faede8" stroke="{C['red']}"/>
<text x="500" y="180" font-size="11" fill="{C['red']}" text-anchor="middle">已知短板：量程 0–50℃，夏季沥青路面可达 60℃+</text>
<text x="500" y="198" font-size="11" fill="{C['red']}" text-anchor="middle">这不是精度问题，是「测不到」</text>
</svg>"""


# ---------------------------------------------------------------- 修正版 MRP（覆盖上方）
def _mrp_ring(ox: int, broken_top: bool, blocked_left: bool) -> str:
    nodes = [(ox + 90, 120, "M"), (ox + 250, 120, "C"),
             (ox + 250, 200, "C"), (ox + 90, 200, "C")]
    out = []
    for x, y, t in nodes:
        col = C["red"] if t == "M" else C["blue"]
        out.append(f'<circle cx="{x}" cy="{y}" r="14" fill="{C["bg"]}" '
                   f'stroke="{col}" stroke-width="2"/>')
        out.append(f'<text x="{x}" y="{y + 4}" font-size="11" font-weight="700" '
                   f'fill="{col}" text-anchor="middle">{t}</text>')
    out.append(f'<line x1="{ox + 250}" y1="134" x2="{ox + 250}" y2="186" '
               f'stroke="{C["blue"]}" stroke-width="1.8"/>')
    out.append(f'<line x1="{ox + 236}" y1="200" x2="{ox + 104}" y2="200" '
               f'stroke="{C["blue"]}" stroke-width="1.8"/>')
    if broken_top:
        out.append(f'<line x1="{ox + 104}" y1="120" x2="{ox + 160}" y2="120" '
                   f'stroke="{C["blue"]}" stroke-width="1.8"/>')
        out.append(f'<line x1="{ox + 190}" y1="120" x2="{ox + 236}" y2="120" '
                   f'stroke="{C["blue"]}" stroke-width="1.8"/>')
        out.append(f'<line x1="{ox + 163}" y1="110" x2="{ox + 187}" y2="130" '
                   f'stroke="{C["red"]}" stroke-width="2.4"/>')
        out.append(f'<line x1="{ox + 163}" y1="130" x2="{ox + 187}" y2="110" '
                   f'stroke="{C["red"]}" stroke-width="2.4"/>')
    else:
        out.append(f'<line x1="{ox + 104}" y1="120" x2="{ox + 236}" y2="120" '
                   f'stroke="{C["blue"]}" stroke-width="1.8"/>')
    if blocked_left:
        out.append(f'<line x1="{ox + 90}" y1="186" x2="{ox + 90}" y2="134" '
                   f'stroke="{C["red"]}" stroke-width="1.8" stroke-dasharray="5 4"/>')
        out.append(f'<text x="{ox + 120}" y="164" font-size="11" '
                   f'fill="{C["red"]}" text-anchor="middle">阻塞</text>')
    else:
        out.append(f'<line x1="{ox + 90}" y1="186" x2="{ox + 90}" y2="134" '
                   f'stroke="{C["blue"]}" stroke-width="1.8"/>')
    return "".join(out)


MRP = (_head(300, "mar") + f'''
<rect x="0" y="0" width="860" height="300" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">MRP 环网：正常态与故障态</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">IEC 62439-2 · 二层 · 正常时阻塞一个环口防广播风暴，故障时打开</text>
<text x="210" y="76" font-size="13" font-weight="700" fill="{C['blue']}" text-anchor="middle">正常态</text>
<text x="650" y="76" font-size="13" font-weight="700" fill="{C['red']}" text-anchor="middle">故障态</text>
<rect x="30" y="88" width="360" height="148" rx="10" fill="{C['soft']}" stroke="{C['line']}"/>
<rect x="470" y="88" width="360" height="148" rx="10" fill="{C['soft']}" stroke="{C['line']}"/>
''' + _mrp_ring(30, False, True) + _mrp_ring(470, True, False) + f'''
<text x="210" y="258" font-size="11" fill="{C['mut']}" text-anchor="middle">左边被阻塞，环逻辑上是线型</text>
<text x="650" y="258" font-size="11" fill="{C['red']}" text-anchor="middle">上边断开，被阻塞的左边打开，绕行</text>
</svg>''')


# ---------------------------------------------------------------- 修正版 U-Net（覆盖上方）
_EN = [(150, "512×512"), (110, "256×256"), (74, "128×128"), (46, "64×64"), (26, "32×32")]
_DC = [26, 46, 74, 110, 150]
_YS = [88, 126, 164, 202, 240]
_bits = []
for _i, (_w, _lb) in enumerate(_EN):
    _bits.append(f'<rect x="60" y="{_YS[_i]}" width="{_w}" height="26" rx="4" '
                 f'fill="{C["blue"]}" opacity="{0.85 - _i * 0.14:.2f}"/>')
    _bits.append(f'<text x="60" y="{_YS[_i] - 5}" font-size="10" '
                 f'fill="{C["mut"]}">{_lb}</text>')
for _i, _w in enumerate(_DC):
    _bits.append(f'<rect x="300" y="{_YS[_i]}" width="{_w}" height="26" rx="4" '
                 f'fill="{C["green"]}" opacity="{0.28 + _i * 0.14:.2f}"/>')
for _i in range(4):
    _x1 = 60 + _EN[_i][0]
    _bits.append(f'<path d="M{_x1},{_YS[_i] + 13} L300,{_YS[_i] + 13}" fill="none" '
                 f'stroke="{C["orange"]}" stroke-width="1.4" stroke-dasharray="5 3"/>')
_bits.append(f'<path d="M86,253 L300,253" fill="none" stroke="{C["blue"]}" stroke-width="1.8"/>')
_bits.append(f'<text x="193" y="272" font-size="10" fill="{C["blue"]}" text-anchor="middle">瓶颈</text>')

UNET = (_head(340, "unar") + f'''
<rect x="0" y="0" width="860" height="340" fill="{C['bg']}"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="{C['tx']}">U-Net：下采样抓语义，上采样回分辨率，跳跃连接补细节</text>
<text x="20" y="48" font-size="12" fill="{C['mut']}">医学影像分割的主力结构，跟骨 X 光也是这条路线</text>
<text x="135" y="76" font-size="12" font-weight="700" fill="{C['blue']}" text-anchor="middle">编码器</text>
<text x="375" y="76" font-size="12" font-weight="700" fill="{C['green']}" text-anchor="middle">解码器</text>
''' + "".join(_bits) + f'''
<text x="470" y="112" font-size="12" font-weight="700" fill="{C['orange']}">橙色虚线 = 跳跃连接</text>
<text x="470" y="132" font-size="11" fill="{C['tx']}">把下采样前的高分辨率特征直接拼到上采样，</text>
<text x="470" y="149" font-size="11" fill="{C['tx']}">补回池化丢掉的边界信息。</text>
<text x="470" y="178" font-size="12" font-weight="700" fill="{C['red']}">跟骨的难点不在结构，在边界：</text>
<text x="470" y="196" font-size="11" fill="{C['tx']}">骨与软组织灰度接近，边缘本就模糊，</text>
<text x="470" y="213" font-size="11" fill="{C['tx']}">所以 Dice 高不代表边界准，要配 HD95。</text>
<text x="20" y="306" font-size="11" fill="{C['mut']}">编码器逐层减半分辨率、通道加倍，解码器反向恢复；跳跃连接共 4 条，对应前 4 层。</text>
</svg>''')


FIGS = {
    "yolo_pipe": YOLO_PIPE,
    "yolo_lat": YOLO_LAT,
    "yolo_acc": YOLO_ACC,
    "mrp": MRP,
    "logflow": LOGFLOW,
    "gimbal": GIMBAL,
    "unet": UNET,
    "diploma": DIPLOMA,
}
