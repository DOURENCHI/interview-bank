# -*- coding: utf-8 -*-
"""生成岗位雷达公司池 companies/radar_companies.json（V1.7 公司池/源池/岗位池分离）。

来源合并：
  1. 内置评审候选表（六大类别，A/B/C 三档）
  2. companies/targets.json 核心池（tier=core）——已有的相关公司自动纳入
字段：company_id / company_name / category / directions / tier(A|B|C) /
      career_url / ats_type(zhiye|feishu|moka|unknown) / source(适配器配置) /
      enabled / note
只有 enabled=true 且带 source 配置的公司会被雷达扫描；
其余是「待核验」——用 tools/detect_ats.py 核验入口后补 source 再开。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 内置候选：[名称, 类别, 方向关键词, 建议档位, career_url(已知才填), ats_type, source, note]
CANDIDATES = [
    # ---- 具身智能 / 人形机器人 ----
    ("宇树科技", "具身智能/人形机器人", "机器人软件;推理部署;系统集成;运动控制", "A",
     "https://unitree.zhiye.com/campus", "zhiye",
     {"base": "https://unitree.zhiye.com", "portal_id": "d2c6fa34-0953-4dee-bc53-522382ea6e19", "category": "2"},
     "已验证：36 岗，JD 全文"),
    ("智元机器人", "具身智能/人形机器人", "机器人软件;推理部署;系统集成", "A", "", "unknown", None, "入口待核验"),
    ("优必选", "具身智能/人形机器人", "机器人软件;运动控制", "B", "", "unknown", None, "入口待核验"),
    ("傅利叶智能", "具身智能/人形机器人", "机器人软件;系统集成", "B", "", "unknown", None, "入口待核验"),
    ("乐聚机器人", "具身智能/人形机器人", "机器人软件", "C", "", "unknown", None, "观察"),
    ("银河通用机器人", "具身智能/人形机器人", "机器人软件;推理部署", "B", "", "unknown", None, "入口待核验"),
    ("星海图", "具身智能/人形机器人", "机器人软件;运动控制", "B", "", "unknown", None, "入口待核验"),
    ("灵心巧手", "具身智能/人形机器人", "机器人软件;灵巧手", "B", "", "unknown", None, "已有岗位模板种子"),
    # ---- 移动机器人 / AMR ----
    ("海康机器人", "移动机器人/AMR", "ROS2;导航;边缘部署", "B", "", "unknown", None, "入口待核验"),
    ("极智嘉", "移动机器人/AMR", "机器人软件;导航", "C", "", "unknown", None, "观察"),
    ("快仓智能", "移动机器人/AMR", "机器人软件;导航", "C", "", "unknown", None, "观察"),
    ("斯坦德机器人", "移动机器人/AMR", "ROS2;导航", "C", "", "unknown", None, "观察"),
    ("仙工智能", "移动机器人/AMR", "ROS2;导航;边缘部署", "C", "", "unknown", None, "观察"),
    # ---- 自动驾驶 / 智能驾驶 ----
    ("Momenta", "自动驾驶/智能驾驶", "C++SDK;推理部署;系统集成", "A",
     "https://momenta.jobs.feishu.cn/campus", "feishu",
     {"url": "https://momenta.jobs.feishu.cn/campus/?project=7664524042879830335", "label": "2027届校招", "type_label": "校招"},
     "已验证：主校招 7 岗"),
    ("Momenta", "自动驾驶/智能驾驶", "推理部署;端到端大模型", "A",
     "https://momenta.jobs.feishu.cn/campus", "feishu",
     {"url": "https://momenta.jobs.feishu.cn/campus", "label": "Mstar 顶才计划", "type_label": "校招"},
     "已验证：Mstar 10 岗"),
    ("地平线", "自动驾驶/智能驾驶", "C++SDK;推理部署;异构计算", "A", "", "unknown", None, "core 池；入口待核验"),
    ("毫末智行", "自动驾驶/智能驾驶", "C++SDK;感知部署", "C", "", "unknown", None, "观察"),
    ("元戎启行", "自动驾驶/智能驾驶", "推理部署;C++SDK", "B", "", "unknown", None, "入口待核验"),
    ("小马智行", "自动驾驶/智能驾驶", "C++SDK;感知部署", "B",
     "https://campus.pony.ai", "unknown", None, "入口已确认，接口待核验"),
    ("文远知行", "自动驾驶/智能驾驶", "C++SDK;推理部署", "B", "", "unknown", None, "入口待核验"),
    ("轻舟智航", "自动驾驶/智能驾驶", "C++SDK;感知部署", "C", "", "unknown", None, "观察"),
    ("百度 Apollo", "自动驾驶/智能驾驶", "C++SDK;推理部署", "B", "", "unknown", None, "入口待核验"),
    # ---- AI 芯片 / 边缘计算 ----
    ("黑芝麻智能", "AI芯片/边缘计算", "推理引擎;SDK;异构计算", "B", "", "unknown", None, "入口待核验"),
    ("芯驰科技", "AI芯片/边缘计算", "SDK;嵌入式", "C", "", "unknown", None, "观察"),
    ("爱芯元智", "AI芯片/边缘计算", "推理引擎;模型部署", "C", "", "unknown", None, "观察"),
    ("算能", "AI芯片/边缘计算", "推理引擎;边缘计算", "C", "", "unknown", None, "观察"),
    ("燧原科技", "AI芯片/边缘计算", "推理引擎;异构计算", "C", "", "unknown", None, "观察"),
    # ---- 工业自动化 / 机器人 ----
    ("埃斯顿自动化", "工业自动化/机器人", "C++;运动控制;机器人系统集成", "A",
     "https://estun1.zhiye.com/campus", "zhiye",
     {"base": "https://estun1.zhiye.com", "portal_id": "", "category": "2"},
     "已验证：21 岗，portalId 自动探测"),
    ("汇川技术", "工业自动化/机器人", "C++;运动控制;嵌入式", "B", "", "unknown", None, "入口待核验"),
    ("节卡机器人", "工业自动化/机器人", "机器人软件;运动控制", "C", "", "unknown", None, "观察"),
    ("遨博智能", "工业自动化/机器人", "机器人软件;运动控制", "C", "", "unknown", None, "观察"),
    ("珞石机器人", "工业自动化/机器人", "机器人软件;运动控制", "C", "", "unknown", None, "观察"),
    ("ABB", "工业自动化/机器人", "机器人软件;C++", "B", "", "unknown", None, "core 池；入口待核验"),
    ("发那科", "工业自动化/机器人", "运动控制;嵌入式", "C", "", "unknown", None, "观察"),
    # ---- 医疗 AI / 医疗设备 ----
    ("联影医疗", "医疗AI/医疗设备", "医学影像AI;推理部署;软件工程", "A", "", "unknown", None, "core 池；入口待核验"),
    ("迈瑞医疗", "医疗AI/医疗设备", "医学影像AI;嵌入式;软件工程", "A", "", "unknown", None, "core 池；入口待核验"),
    ("东软医疗", "医疗AI/医疗设备", "医学影像AI", "C", "", "unknown", None, "观察"),
    ("GE医疗", "医疗AI/医疗设备", "医学影像AI;软件工程", "C", "", "unknown", None, "观察"),
    ("飞利浦医疗", "医疗AI/医疗设备", "医学影像AI;软件工程", "C", "", "unknown", None, "观察"),
    # ---- 智能硬件 / 消费机器人（core 池延伸）----
    ("大疆创新", "智能硬件/无人机", "嵌入式;推理部署;机器人软件", "B",
     "https://careers.dji.com/zh-CN/campus", "unknown", None, "入口已确认，接口待核验"),
    ("追觅", "智能硬件/消费机器人", "机器人软件;算法", "B", "", "unknown", None, "core 池；入口待核验"),
]


def pid(name: str) -> str:
    return re.sub(r"\s+", "", name).lower()


def main() -> int:
    companies = []
    seen = set()
    for name, cat, dirs, tier, url, ats, source, note in CANDIDATES:
        cid = pid(name) + (("_" + pid(source["label"])) if source and source.get("label") else "")
        if cid in seen:                       # 同公司多源：Momenta 两个 portal
            companies[-1] = companies[-1] if False else companies[-1]
        seen.add(cid)
        companies.append({
            "company_id": cid,
            "company_name": name,
            "category": cat,
            "directions": dirs.split(";"),
            "tier": tier,
            "career_url": url,
            "ats_type": ats,
            "source": source,
            "enabled": bool(source),
            "note": note,
        })

    # targets.json 核心池合并（已存在的跳过）
    tj = ROOT / "companies" / "targets.json"
    if tj.exists():
        core = [c["name"] for c in
                json.loads(tj.read_text(encoding="utf-8")).get("companies", [])
                if c.get("tier") == "core"]
        have = {c["company_name"] for c in companies}
        for name in core:
            if name not in have:
                companies.append({
                    "company_id": pid(name), "company_name": name,
                    "category": "其他(core池)", "directions": [],
                    "tier": "B", "career_url": "", "ats_type": "unknown",
                    "source": None, "enabled": False, "note": "targets 核心池；入口待核验"})
                have.add(name)

    out = ROOT / "companies" / "radar_companies.json"
    out.write_text(json.dumps({"companies": companies}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    n_on = sum(1 for c in companies if c["enabled"])
    print(f"公司池 {len(companies)} 家（启用 {n_on}）→ {out.name}")
    from collections import Counter
    print("档位:", dict(Counter(c["tier"] for c in companies)))
    print("类别:", dict(Counter(c["category"] for c in companies)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
