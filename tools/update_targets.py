#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重建 companies/targets.json：核心池（有档案）+ 观察池（仅索引与筛选）。

来源：D:/工程/方向与规划/方向/公司池_苏南优先_19列_五城实习版.xlsx（183 行去重）
     + 常见互联网公司补充。
可重复执行：核心池的 aliases / extra 保留原值，只补 tier 与 nc_keywords。

nc_keywords 的匹配规则（tools/nc_collect.py）：
  · 纯小写关键词走忽略大小写匹配；含大写字母或 \\b 的走大小写敏感
  · JSON 顺序即匹配顺序，"子串更具体"的公司必须排在前面（如 联影智能 → 联影医疗）
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TF = ROOT / "companies" / "targets.json"

ROLE_NAME = {
    "A": "A SDK / 基础软件", "B": "B 系统集成", "C": "C 推理部署",
    "D": "D 感知算法", "E": "E 嵌入式", "F": "F 机器人软件",
}

def C(name, keys, roles, main, extra=None):
    return {"name": name, "tier": "watch", "nc_keywords": keys, "roles": roles,
            "main": ROLE_NAME[main], "extra": extra or []}

# 观察池：来自公司池 xlsx（类别 = xlsx 的 7 大类）+ 常见互联网补充
WATCH = [
    # ---- 1 医疗影像与手术机器人 ----
    C("联影智能", ["联影智能"], ["D"], "D"),
    C("GE医疗", ["GE医疗", "GE HealthCare", "GE Healthcare"], ["B", "D"], "D"),
    C("东软医疗", ["东软医疗", "东软"], ["B", "D"], "D"),
    C("推想医疗", ["推想医疗", "推想科技"], ["D"], "D"),
    C("数坤科技", ["数坤"], ["D"], "D"),
    C("深睿医疗", ["深睿"], ["D"], "D"),
    C("微创医疗", ["微创医疗", "微创机器人"], ["B", "E"], "B"),
    C("华大基因", ["华大基因"], ["D"], "D"),
    C("亿嘉和", ["亿嘉和", "佗道"], ["D", "E", "F"], "D"),
    C("祥生医疗", ["祥生"], ["D"], "D"),
    C("敏捷医疗", ["敏捷医疗", "AGIBOT医疗"], ["F", "D"], "F"),
    C("霆升医疗", ["霆升"], ["D", "F"], "D"),
    C("鑫君特", ["鑫君特"], ["F"], "F"),
    C("铸正机器人", ["铸正"], ["F"], "F"),
    # ---- 2 机器人与具身智能 ----
    C("海康机器人", ["海康机器人"], ["F", "E", "D"], "F"),
    C("图达通", ["图达通", "Innovusion"], ["D", "E"], "D"),
    C("埃斯顿", ["埃斯顿"], ["F", "E"], "F"),
    C("因克斯智能", ["因克斯"], ["F", "E", "D"], "F"),
    C("穿山甲机器人", ["穿山甲机器人", "穿山甲科技"], ["F", "E"], "F"),
    C("箸境智能", ["箸境"], ["F", "D"], "F"),
    C("星海图", ["星海图"], ["F", "D"], "F"),
    C("宇树科技", ["宇树", "Unitree"], ["F", "E"], "F"),
    C("智元机器人", ["智元"], ["F", "D"], "F"),
    C("傅利叶智能", ["傅利叶"], ["F", "E"], "F"),
    C("银河通用", ["银河通用"], ["F", "D"], "F"),
    C("优必选", ["优必选", "UBTECH"], ["F"], "F"),
    C("云深处科技", ["云深处"], ["F", "D"], "F"),
    C("新松机器人", ["新松"], ["F"], "F"),
    C("节卡机器人", ["节卡"], ["F"], "F"),
    C("非夕机器人", ["非夕", "Flexiv"], ["F"], "F"),
    C("越疆科技", ["越疆"], ["F"], "F"),
    C("逐际动力", ["逐际动力"], ["F"], "F"),
    C("加速进化", ["加速进化"], ["F"], "F"),
    C("大疆", ["大疆", "DJI"], ["E", "D", "F"], "E"),
    # ---- 3 AI芯片与硬科技 ----
    C("英伟达", ["英伟达", "NVIDIA"], ["C", "A"], "C"),
    C("英特尔", ["英特尔", "Intel"], ["A", "C"], "C"),
    C("AMD", ["AMD"], ["C", "A"], "C"),
    C("高通", ["高通", "Qualcomm"], ["C", "E"], "C"),
    C("Arm中国", ["安谋", "Arm中国"], ["E", "A"], "E"),
    C("德州仪器", ["德州仪器"], ["E"], "E"),
    C("意法半导体", ["意法半导体", "STMicroelectronics"], ["E"], "E"),
    C("英飞凌", ["英飞凌", "Infineon"], ["E"], "E"),
    C("三星", ["三星", "Samsung"], ["E", "C"], "E"),
    C("西部数据", ["西部数据", "Western Digital"], ["E"], "E"),
    C("联发科", ["联发科", "MediaTek", "MTK"], ["E", "C"], "E"),
    C("长鑫存储", ["长鑫"], ["E"], "E"),
    C("登临科技", ["登临"], ["C", "A"], "C"),
    C("日联科技", ["日联"], ["D"], "D"),
    C("苏州科达", ["苏州科达", "科达（603660）"], ["D", "E"], "D"),
    C("硅山技术", ["硅山"], ["C", "E"], "C"),
    C("罗克韦尔", ["罗克韦尔", "Rockwell"], ["B", "E"], "B"),
    # ---- 4 工业AI与自动化 ----
    C("西门子（工业）", ["西门子(?!医疗)"], ["B", "A"], "B"),
    C("博世", ["博世", "Bosch"], ["B", "E", "D"], "B"),
    C("施耐德电气", ["施耐德"], ["B", "E"], "B"),
    C("汇川技术", ["汇川"], ["E", "B", "F"], "E"),
    C("海康威视", ["海康威视"], ["D", "E", "C"], "D"),
    C("大华股份", ["大华"], ["D", "E"], "D"),
    C("霍尼韦尔", ["霍尼韦尔", "Honeywell"], ["B", "E"], "B"),
    C("美的集团", ["美的集团", "美的机器人"], ["E", "F", "B"], "E"),
    C("三一重工", ["三一"], ["E", "F"], "E"),
    C("卡尔蔡司", ["蔡司", "ZEISS"], ["B", "D", "E"], "B"),
    C("发那科", ["发那科", "FANUC"], ["F", "E"], "F"),
    C("库卡", ["库卡", "KUKA"], ["F", "E"], "F"),
    C("松下", ["松下", "Panasonic"], ["E"], "E"),
    C("佳能", ["佳能", "Canon"], ["E", "D"], "E"),
    C("海尔", ["海尔"], ["E"], "E"),
    C("格力", ["格力"], ["E"], "E"),
    C("中联重科", ["中联重科"], ["E", "F"], "E"),
    # ---- 5 互联网与软件 ----
    C("字节跳动", ["字节跳动", "ByteDance", "抖音"], ["A", "C", "D"], "A"),
    C("阿里巴巴", ["阿里巴巴", "阿里", "淘宝"], ["A", "C", "D"], "A"),
    C("腾讯", ["腾讯"], ["A", "C", "D"], "A"),
    C("百度", ["百度", "Apollo"], ["A", "C", "D"], "C"),
    C("美团", ["美团"], ["A", "C"], "A"),
    C("京东", ["京东"], ["A", "E"], "A"),
    C("快手", ["快手"], ["A", "C"], "A"),
    C("网易", ["网易", "有道"], ["A", "E", "D"], "A"),
    C("小米汽车", ["小米汽车"], ["C", "E", "B"], "C"),
    C("小米集团", ["小米"], ["A", "E", "D"], "E"),
    C("商汤科技", ["商汤", "SenseTime"], ["D", "C"], "D"),
    C("蚂蚁集团", ["蚂蚁"], ["A", "B"], "A"),
    C("携程", ["携程"], ["A"], "A"),
    C("滴滴", ["滴滴"], ["A", "C", "D"], "C"),
    C("拼多多", ["拼多多", "PDD"], ["A"], "A"),
    C("小红书", ["小红书"], ["A", "C", "D"], "A"),
    C("哔哩哔哩", ["B站", "bilibili", "哔哩哔哩"], ["A", "C"], "A"),
    C("OPPO", ["OPPO"], ["E", "A"], "E"),
    C("vivo", ["vivo", "VIVO"], ["E", "A"], "E"),
    C("荣耀", ["荣耀终端", "HONOR", "荣耀手机"], ["E", "A"], "E"),
    C("科大讯飞", ["讯飞", "iFlytek", "科大讯飞"], ["A", "D", "C"], "D"),
    C("智加科技", ["智加"], ["C", "D"], "C"),
    C("满帮集团", ["满帮"], ["A"], "A"),
    C("同程旅行", ["同程"], ["A"], "A"),
    C("思必驰", ["思必驰"], ["D", "A"], "D"),
    C("帆软软件", ["帆软"], ["A"], "A"),
    C("焦点科技", ["焦点科技"], ["A"], "A"),
    C("汇通达", ["汇通达"], ["A"], "A"),
    C("朗新科技", ["朗新"], ["A", "E"], "A"),
    # ---- 6 汽车与智能驾驶 ----
    C("理想汽车", ["理想汽车", "Li Auto"], ["C", "B", "E"], "C"),
    C("比亚迪", ["比亚迪", "BYD"], ["E", "B", "D"], "E"),
    C("上汽集团", ["上汽"], ["E", "B", "C"], "B"),
    C("零跑汽车", ["零跑"], ["C", "E"], "C"),
    C("赛力斯", ["赛力斯"], ["B", "E"], "B"),
    C("长安汽车", ["长安汽车"], ["B", "E", "C"], "B"),
    C("长城汽车", ["长城汽车"], ["E", "B"], "E"),
    C("奇瑞集团", ["奇瑞"], ["E", "B"], "E"),
    C("广汽集团", ["广汽"], ["B", "E"], "B"),
    C("吉利汽车", ["吉利", "极氪"], ["B", "E", "C"], "B"),
    C("东风汽车", ["东风汽车"], ["B", "E"], "B"),
    C("大陆集团", ["大陆集团", "Continental"], ["E", "B"], "E"),
    C("德赛西威", ["德赛西威", "均胜", "华阳集团"], ["E", "B"], "E"),
    C("大众CARIAD", ["CARIAD", "大众安徽"], ["B", "A"], "B"),
    C("梅赛德斯-奔驰", ["奔驰", "梅赛德斯"], ["B", "E", "A"], "B"),
    C("宝马", ["宝马", "BMW"], ["B", "E", "A"], "B"),
    # ---- 7 通信与ICT ----
    C("中兴通讯", ["中兴"], ["E", "A", "C"], "E"),
    C("烽火通信", ["烽火"], ["E", "A"], "E"),
    # ---- 8 国际外企补充 ----
    C("微软", ["微软", "Microsoft"], ["A", "C"], "A"),
    C("索尼", ["索尼", "Sony"], ["E", "D"], "E"),
    C("谷歌", ["Google", "谷歌"], ["A", "C"], "A"),
]

# 核心池：已有档案的 10 家（tier=core），nc_keywords 对齐采集器
CORE_KW = {
    "Momenta":   ["Momenta", "魔门塔"],
    "华为":      ["华为", "huawei", "海思", "车BU"],
    "地平线":    ["地平线", "Horizon Robotics", "征程"],
    "蔚来":      ["蔚来", "NIO"],
    "小鹏":      ["小鹏", "xpeng"],
    "ABB":       ["\\bABB\\b"],
    "西门子医疗": ["西门子医疗", "Healthineers"],
    "联影医疗":  ["联影"],
    "迈瑞医疗":  ["迈瑞", "mindray"],
    "追觅":      ["追觅", "dreame", "青庭"],
}
# 修剪旧档案带来的过宽别名（实测会误伤："moment"撞英文词、"nio"撞 union、
# "abb"撞小写、"西门子"撞工业西门子、"2012"撞无关文本、"工业机器人"太泛）
PRUNE = {"Momenta": ["moment"], "蔚来": ["nio"], "ABB": ["abb", "工业机器人", "\\bABB\\b"],
         "西门子医疗": ["siemens", "西门子"], "华为": ["2012"]}
# 核心池在旧文件里的历史名字（改名/全称差异）
OLD_NAMES = {"小鹏": ["小鹏汽车"], "追觅": ["追觅科技"]}


def main() -> int:
    old = json.loads(TF.read_text(encoding="utf-8"))
    role_name = {r["key"]: r["name"] for r in old["roles"]}

    # 幂等：核心池只认 CORE_KW 里的名字；旧文件里的 watch 条目全部丢弃重建
    companies = []
    for c in old["companies"]:
        key = next((k for k in CORE_KW
                    if c["name"] == k or c["name"] in OLD_NAMES.get(k, [])), None)
        if key is None:
            continue
        c2 = dict(c)
        c2["tier"] = "core"
        c2["name"] = key
        kws = list(dict.fromkeys(
            [key] + c.get("aliases", []) + CORE_KW.get(key, [])))
        for bad in PRUNE.get(key, []):
            kws = [k for k in kws if k != bad]          # 精确匹配，防止误删本名（ABB）
        c2["nc_keywords"] = kws
        c2["main"] = role_name.get(c["roles"][0], c.get("main", ""))
        companies.append(c2)

    # 观察池插入到核心池里"会吞掉它"的公司之前
    # 目前只有一对：联影智能 必须在 联影医疗 之前
    lian = next(i for i, c in enumerate(companies) if c["name"] == "联影医疗")
    watch_before, watch_after = [], []
    for w in WATCH:
        (watch_before if w["name"] == "联影智能" else watch_after).append(w)
    companies = (companies[:lian] + watch_before + companies[lian:] + watch_after)

    for c in companies:
        if c["tier"] != "core" and not c["main"].startswith(tuple(role_name.values())):
            c["main"] = role_name[c["roles"][0]]

    old["companies"] = companies
    old["_comment"] = (
        "公司 / 岗位筛选的机器可读映射 + 牛客采集器的公司注册表。"
        "tier: core=有档案且采集（10家）; watch=仅索引与筛选（来自 公司池_苏南优先 xlsx + 常见互联网补充）。"
        "source_type 一律是 inferred：按 JD 与技术方向推导，不代表该公司真实考过。"
        "真实面经请写进题卡的 appearances 字段。新增公司：复制一条条目、给 nc_keywords、"
        "注意把它排在会吞掉其关键词的公司之前。")
    TF.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n_core = sum(1 for c in companies if c["tier"] == "core")
    print(f"targets.json 已重建：{len(companies)} 家（core {n_core} / watch {len(companies)-n_core}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
