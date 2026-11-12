#!/usr/bin/env python3
"""岗位雷达：低频增量监控目标公司官方招聘门户（CareerOS V1.7：覆盖率升级）。

V1.7：公司池驱动——扫描对象来自 companies/radar_companies.json（enabled=true 且带 source），
不再硬编码；岗位按四层岗位族关键词自动打标（families），命中排除词的岗位直接跳过并计数；
快照附 pool_stats（公司覆盖率）与 families 统计。

用法：
  python tools/job_radar.py --scan         # 扫描全部监控源 → sources/jobs_radar.json + radar_report.md
  python tools/job_radar.py --reclassify   # 离线重算招聘性质分类（校招/实习/社招），不联网

V1.8 招聘性质分类：
  * 每条岗位带 job_class / class_basis / class_conf / class_evidence，区分「校招 / 实习 / 社招 / 未标明」
  * 证据优先级：岗位标题明确 > 来源批次标签 > 校园招聘入口推定 > 来源未标注
  * 实习岗同步修正 type，并清掉由入口批次误推的 grad_year（实习不限届别）
  * 快照附 class_stats / class_basis_stats，页面按性质分类展示全部岗位

V1.6 数据质量规则：
  * job_key = company : source_job_id : norm_city : batch —— 同岗多城市/多批次不误合并
  * 每条岗位带 first_seen / last_seen / status(open|suspect|closed) / consecutive_missing
  * 采集失败 ≠ 岗位下线：失败源不参与 missing 判断；连续 2 次成功扫描未见 → suspect
  * JD 变更做语义分类（职责/任职要求/硬性条件含届别学历/地点/名称），保留最近 3 条变更记录
  * 每源独立 source_status（success/failed + error），快照含最近实际扫描时间

合规边界（写在代码里）：
  * 每源每次只发少量请求（zhiye 1~2 个 POST；feishu 一次页面渲染）
  * 只读公开职位列表页，不登录、不绕验证码、不重试轰炸
  * 提交进仓库的只有：岗位名/城市/JD 摘要/链接/发现日期
适配器：
  zhiye   智业云（北森）门户 —— requests 直连 /api/Jobad/GetJobAdPageList
  feishu  飞书招聘门户 —— Playwright 渲染 + 监听 search/job/posts 自然响应
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POOL = ROOT / "companies" / "radar_companies.json"
RADAR = ROOT / "sources" / "jobs_radar.json"
REPORT = ROOT / "sources" / "radar_report.md"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
CST = timezone(timedelta(hours=8))
SUSPECT_AFTER = 2          # 连续 2 次成功扫描未见 → 疑似下线
HISTORY_KEEP = 3           # 每岗位保留最近 3 条变更记录
HARD_PAT = re.compile(r"届|毕业|学历|本科|硕士|博士")
# V1.8 招聘性质：校招 / 实习 / 社招 / 未标明（岗位级证据优先于入口级推定）
CLASS_NAMES = ["校招", "实习", "社招", "未标明"]
INTERN_PAT = re.compile(r"实习|intern(ship)?|见习|暑期|日常实习", re.I)
CAMPUS_PAT = re.compile(r"校招|校园招聘|应届|20\d{2}\s*届|顶才|探索者|管培", re.I)
SOCIAL_PAT = re.compile(r"社招|社会招聘|experienced|资深工程师", re.I)

# 四层岗位族关键词（V1.7）：很多公司不用新词，传统岗位名也要命中
JOB_FAMILIES = [
    ("AI推理部署", ["模型部署", "推理优化", "推理引擎", "推理框架", "inference", "tensorrt",
                    "onnx", "边缘计算", "异构计算", "ai runtime", "模型压缩", "量化", "编译优化",
                    "算子", "kernel", "图优化", "高性能计算"]),
    ("机器人软件/ROS2", ["机器人软件", "ros", "机器人中间件", "运动控制", "导航", "运动规划",
                        "规划控制", "系统集成", "机器人系统", "机器人算法", "具身", "功能安全"]),
    ("C++ SDK/系统软件", ["c++", "sdk", "平台软件", "基础软件", "车载软件", "基础组件",
                          "系统软件", "中间件", "平台开发", "训练平台", "数据闭环", "基础架构",
                          "分布式", "存储", "数据库", "后端", "服务端", "infra", "agent",
                          "信息安全", "安全工程师"]),
    ("VLM/VLA/视觉算法", ["视觉算法", "感知算法", "vlm", "vla", "多模态", "世界模型",
                          "端到端", "强化学习", "模仿学习", "图像算法", "具身智能", "大模型",
                          "算法工程师"]),
    ("嵌入式/控制", ["嵌入式", "固件", "bsp", "驱动", "单片机", "mcu", "autosar",
                    "电机驱动", "电机控制", "电源", "硬件工程师", "pcb", "电气"]),
]
# 轻排除：只排明确无关岗，不排算法岗（视觉/VLA 是第二优先级方向）
EXCLUDE_PAT = re.compile(
    r"销售|售前|实施顾问|产品经理|市场(?!营销算法)|行政|人事|hr|h r|财务|会计|法务|"
    r"商务|运营专员|客服|采购|行政专员|设计师|视觉设计|平面|品牌|文案|直播|电商运营")


# ---------------------------------------------------------------- 招聘硬性条件（V2.0）
# 只做保守规则：宁可抽不到（页面显示「未说明」），也不猜。抽不到 ≠ 符合。
NON_TECH_PAT = re.compile(
    r"物流|供应链|制造支持|工艺|生产计划|管培|培训生|采购|财务|会计|人力|招聘|行政|"
    r"法务|市场|营销|销售|品牌|运营|客服|商务|售后")
TECH_TITLE_PAT = re.compile(
    r"c\+\+|c/c\+\+|python|java|golang|linux|算法|嵌入式|驱动|固件|bsp|mcu|单片机|"
    r"推理|部署|模型|算子|编译|cuda|tensorrt|onnx|ros|slam|导航|感知|视觉|图像|"
    r"机器人|控制|电机|硬件|电子|fpga|dsp|通信|软件|开发|研发|测试|数据|平台|"
    r"系统|架构|sdk|引擎|ai|infra|工程师|科学家|研究员", re.I)


def tech_relevant(title: str, jd: str = "") -> bool:
    """岗位是否属于技术岗。职能/制造/供应链类即使 JD 里出现「系统」也不算。"""
    t = title or ""
    if NON_TECH_PAT.search(t) and not re.search(
            r"算法|开发|工程师|研发|软件|嵌入式|推理|模型|数据|测试", t):
        return False
    return bool(TECH_TITLE_PAT.search(t))


def extract_requirements(jd: str) -> dict:
    """从 JD 原文抽硬性条件。返回 None 表示「未说明」，页面不得当成符合。"""
    t = (jd or "").replace("／", "/")
    out = {"education": None, "grad_range": None, "student_status": None,
           "intern_duration": None, "weekly_days": None}
    if not t:
        return out
    for e in ("博士", "硕士", "本科", "大专"):
        i = t.find(e)
        if i >= 0:
            tail = t[i:i + 10]
            out["education"] = e + ("及以上" if "及以上" in tail else "")
            break
    ys = {int(y) for y in re.findall(r"(20\d{2})\s*届", t)}
    ys |= {int(y) for y in re.findall(r"(20\d{2})\s*年(?:毕业|应届)", t)}
    if ys:
        out["grad_range"] = [min(ys), max(ys)]
    if re.search(r"在校生|在读|全日制在读", t):
        out["student_status"] = "在校生"
    elif re.search(r"(?:应届|20\d{2}\s*届)\s*(?:毕业生|生)", t):
        out["student_status"] = "应届毕业生"
    if re.search(r"实习|intern", t, re.I):
        m = re.search(r"(?:至少|不少于|连续|实习期?)\s*(\d{1,2})\s*个月", t)
        if m:
            out["intern_duration"] = int(m.group(1))
    m = re.search(r"(?:每周|一周)\s*(?:到岗|出勤)?\s*(\d)\s*天", t)
    if m:
        out["weekly_days"] = int(m.group(1))
    return out


def annotate_job(j: dict) -> dict:
    """离线补 V2.0 字段：硬性条件 / 技术相关度 / 岗位族置信度（幂等，不联网）。"""
    j = dict(j)
    j["families"] = families_of(j.get("title") or "", j.get("jd") or "")
    j["req"] = extract_requirements(j.get("jd") or "")
    j["tech_relevant"] = tech_relevant(j.get("title") or "", j.get("jd") or "")
    fams = j.get("families") or []
    j["family_conf"] = "high" if fams and fams != ["其他"] else "low"
    return j


def annotate_stats(jobs: list) -> dict:
    n = len(jobs) or 1
    req = [j for j in jobs if (j.get("req") or {}).get("education") or (j.get("req") or {}).get("grad_range")]
    return {
        "jobs": len(jobs),
        "tech_relevant": sum(1 for j in jobs if j.get("tech_relevant")),
        "non_tech": sum(1 for j in jobs if j.get("tech_relevant") is False),
        "family_low": sum(1 for j in jobs if j.get("family_conf") == "low"),
        "req_known": len(req),
        "req_known_pct": round(len(req) / n * 100),
    }


def families_of(title: str, jd: str) -> list:
    text = ((title or "") + " " + (jd or "")[:400]).lower()
    fams = []
    for fam, kws in JOB_FAMILIES:
        if any(k.lower() in text for k in kws):
            fams.append(fam)
    return fams or ["其他"]


# ================================================================ 纯函数（可单测）

def norm_city(city: str) -> str:
    c = re.sub(r"\s+", "", city or "")
    return c if c and c != "待核实" else "-"


def extract_grad(text: str) -> int | None:
    m = re.search(r"(20\d{2})\s*届", text or "")
    return int(m.group(1)) if m else None


def make_key(company: str, source_id: str, city: str, batch: str) -> str:
    return f"{company}:{source_id}:{norm_city(city)}:{batch or '-'}"


def classify_job(job: dict, site: dict | None = None) -> dict:
    """招聘性质分类（V1.8）：返回浅拷贝，幂等，可反复对同一岗位重算。

    证据优先级（越靠前越可信）：
      1. 岗位标题含「实习/校招/社招/2027届」→ high，岗位自身明确标注
      2. 来源批次标签（label/batch）含同类词     → medium，批次级标注
      3. 入口为校园招聘（zhiye category=2 / URL 含 campus）→ low，仅入口推定
      4. 都没有                                  → 「未标明」，none
    实习岗另外修正：type 改为「实习」；若 grad_year 只是从入口批次推来的，置空并留痕，
    避免把「2027届校招入口里的实习生」误判为「只面向 2027 届」。
    """
    site = site or {}
    j = dict(job)
    title = j.get("title") or ""
    # 括号里的「portalId 运行时探测」是采集说明，不是官方批次，剔除后再匹配
    tag = re.sub(r"[（(][^）)]*[）)]", "", " ".join(
        x for x in [j.get("label"), j.get("batch"), site.get("label")] if x))
    link = " ".join([str((j.get("links") or [""])[0]),
                     str(site.get("url") or ""), str(site.get("base") or "")])
    ats = j.get("src") or site.get("ats_type") or ""

    def hit(pat, text):
        m = pat.search(text or "")
        return m.group(0) if m else ""

    ev = hit(INTERN_PAT, title)
    if ev:
        cls, basis, conf = "实习", "岗位标题明确", "high"
    elif (ev := hit(SOCIAL_PAT, title)):
        cls, basis, conf = "社招", "岗位标题明确", "high"
    elif (ev := hit(CAMPUS_PAT, title)):
        cls, basis, conf = "校招", "岗位标题明确", "high"
    elif (ev := hit(INTERN_PAT, tag)):
        cls, basis, conf = "实习", "来源批次标签", "medium"
    elif (ev := hit(SOCIAL_PAT, tag)):
        cls, basis, conf = "社招", "来源批次标签", "medium"
    elif (ev := hit(CAMPUS_PAT, tag)):
        cls, basis, conf = "校招", "来源批次标签", "medium"
    elif ((ats == "zhiye" and str(site.get("category", "2")) == "2")
          or "campus" in link.lower()
          or site.get("type_label") == "校招"):
        cls, basis, conf, ev = "校招", "校园招聘入口推定", "low", "校园招聘入口"
    else:
        cls, basis, conf, ev = "未标明", "来源未标注", "none", ""

    j.update({"job_class": cls, "class_basis": basis, "class_conf": conf,
              "class_evidence": ev[:24]})
    if cls == "实习":
        j["type"] = "实习"
        # 标题未写届别、却因批次标签被推成 2027 届 → 实习不限届别，清掉硬条件
        if not extract_grad(title) and j.get("grad_year"):
            j["grad_year_raw"] = j["grad_year"]
            j["grad_year"] = None
            j["grad_year_basis"] = "实习岗不限届别；原值来自入口批次推定"
    return j


def site_by_source(pool: list) -> dict:
    """source_id（公司·label）→ 公司池配置，供离线重分类复用入口信息。"""
    out = {}
    for c in pool:
        src = c.get("source") or {}
        sid = f"{c['company_name']}·{src.get('label', '')}"
        out[sid] = {"ats_type": c.get("ats_type"), **src}
    return out


def class_stats_of(jobs: list) -> dict:
    from collections import Counter
    return {
        "class_stats": {k: v for k, v in Counter(j.get("job_class") or "未标明" for j in jobs).items()},
        "class_basis_stats": dict(Counter(j.get("class_basis") or "来源未标注" for j in jobs)),
    }


def class_section(snap: dict) -> list[str]:
    """报告中的招聘性质分类小节（在线扫描与离线重分类共用）。"""
    cs = snap.get("class_stats") or {}
    bs = snap.get("class_basis_stats") or {}
    lines = ["\n## 招聘性质分类（校招 / 实习 / 社招 / 未标明）",
             "| 性质 | 岗位数 |", "| --- | --- |"]
    lines += [f"| {k} | {cs.get(k, 0)} |" for k in CLASS_NAMES if cs.get(k)]
    lines.append("\n判定依据分布（标题明确 > 批次标签 > 入口推定）：" +
                 " · ".join(f"{k} {v}" for k, v in bs.items()))
    lines.append("\n> 说明：「校园招聘入口推定」只说明该岗位挂在校园招聘入口下，"
                 "不等于官方明确写了校招批次；投递前请点开 JD 原文核实。实习岗不套用入口批次的届别限制。")
    return lines


def jd_hash(jd: str) -> str:
    return hashlib.md5((jd or "").encode()).hexdigest()[:12]


def classify_change(old: dict, new: dict) -> list[str]:
    """JD 变化语义分类：返回变更种类列表。"""
    kinds = []
    if (old.get("title") or "") != (new.get("title") or ""):
        kinds.append("岗位名称变化")
    if re.sub(r"\s", "", old.get("duty") or "") != re.sub(r"\s", "", new.get("duty") or ""):
        kinds.append("职责变化")
    if re.sub(r"\s", "", old.get("require") or "") != re.sub(r"\s", "", new.get("require") or ""):
        kinds.append("任职要求变化")
    if norm_city(old.get("city") or "") != norm_city(new.get("city") or ""):
        kinds.append("工作地点变化")
    if old.get("grad_year") != new.get("grad_year") and (old.get("grad_year") or new.get("grad_year")):
        kinds.append("⚠ 硬性条件变化（届别）")
    if old.get("batch") != new.get("batch") and (old.get("batch") or new.get("batch")):
        kinds.append("⚠ 硬性条件变化（招聘批次）")
    # JD 全文层面出现届别/学历词且整体 hash 变化 → 提示人工核对
    if not kinds and (old.get("jd") or "") != (new.get("jd") or ""):
        kinds.append("JD 内容变化（格式或细节）")
    return kinds


def reconcile(old_jobs: list, scans: dict, today: str) -> tuple[list, dict]:
    """合并上次快照与本次扫描结果（V1.6 状态机）。

    scans: {source_id: {"status": "success"|"failed", "jobs": [job], "error": str|None}}
    只有 status=success 的源参与 missing 判断；失败源岗位原样保留。
    返回 (merged_jobs, source_states)。
    """
    old_by_key = {j["key"]: j for j in old_jobs}
    new_flat: dict = {}
    src_ok: dict = {}
    for sid, sc in scans.items():
        src_ok[sid] = {"status": sc["status"], "error": sc.get("error"),
                       "jobs_found": len(sc.get("jobs") or []), "checked_at": today}
        if sc["status"] != "success":
            continue
        for j in sc["jobs"]:
            new_flat[j["key"]] = j
    merged = []
    # 1) 本次扫到的岗位：继承 first_seen / change_log，更新 last_seen
    for key, j in new_flat.items():
        o = old_by_key.get(key)
        if o:
            kinds = classify_change(o, j)
            log = list(o.get("change_log") or [])
            if kinds:
                log.insert(0, {"date": today, "kinds": kinds})
                log = log[:HISTORY_KEEP]
            merged.append({**j,
                           "first_seen": o.get("first_seen") or today,
                           "last_seen": today,
                           "status": "open",
                           "consecutive_missing": 0,
                           "jd_hash": jd_hash(j.get("jd")),
                           "prev_jd_hash": o.get("jd_hash"),
                           "change_log": log})
        else:
            merged.append({**j,
                           "first_seen": today, "last_seen": today,
                           "status": "open", "consecutive_missing": 0,
                           "jd_hash": jd_hash(j.get("jd")), "prev_jd_hash": None,
                           "change_log": []})
    # 2) 本次未扫到的旧岗位：源失败保留原状（失败≠下线）；成功源 missing+1，连续 2 次 → suspect
    for key, o in old_by_key.items():
        if key in new_flat:
            continue
        sc = scans.get(o.get("source_id") or "")
        if sc is None or sc["status"] != "success":
            merged.append({**o})                       # 失败源/未知源：不增 missing、不改状态
            continue
        miss = (o.get("consecutive_missing") or 0) + 1
        st = "suspect" if miss >= SUSPECT_AFTER else "open"
        merged.append({**o, "consecutive_missing": miss, "status": st,
                       "last_seen": o.get("last_seen")})
    return merged, src_ok


# ================================================================ 适配器

def zhiye_portal_id(base: str, portal_id: str, category: str, s, pages=None) -> str:
    """portal_id 留空时：从门户页 HTML 提取候选，逐个试到 Count>0。
    pages 可传入口 URL 列表（/campus、/intern/jobs…）；category 依次试给定值与 2/3/1。"""
    if portal_id:
        return portal_id
    pages = pages or [base + "/campus"]
    cands = []
    for pg_url in pages:
        try:
            h = s.get(pg_url, timeout=25).text
        except Exception:
            continue
        cands += re.findall(r'"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"', h)
    cands = list(dict.fromkeys(cands))[:8]
    for pid in cands:
        for cat in dict.fromkeys([category, "2", "3", "1"]):
            try:
                r = s.post(base + "/api/Jobad/GetJobAdPageList", json={
                    "Category": [cat], "PageIndex": 0, "PageSize": 1,
                    "KeyWords": "", "SpecialType": 0, "PortalId": pid,
                    "DisplayFields": []}, timeout=20)
                if r.status_code == 200 and r.json().get("Count", 0) > 0:
                    print(f"  [zhiye] 动态 portalId={pid[:8]}… category={cat} 命中 {r.json()['Count']} 岗")
                    return pid
            except Exception:
                continue
    raise RuntimeError("未能确定 portalId")


CITY_WORD = ("北京|上海|天津|重庆|深圳|广州|苏州|南京|无锡|常州|合肥|杭州|成都|西安|武汉|"
             "宁波|东莞|佛山|珠海|昆山|嘉兴|绍兴|厦门|长沙|郑州|济南|青岛|沈阳|大连|哈尔滨|"
             "昆明|贵阳|南宁|福州|温州|徐州|扬州|镇江|南通|芜湖")


def city_from_title(title: str) -> str:
    """zhiye 系门户把城市写在标题尾部（「XX工程师 - 上海(J19796)」「XX（成都）(J12640)」），
    LocNames 常为空数组，这里从标题兜底提取。注意只认城市词表，防止把「-27届校招」当城市。"""
    t = title or ""
    m = re.search(r"[-–—]\s*([^-\s()（）]{1,12})\s*[(（][A-Za-z0-9]{2,}[)）]\s*$", t)
    if m and re.fullmatch(rf"(?:{CITY_WORD})市?", m.group(1)):
        return m.group(1).strip()
    m = re.search(rf"[（(]((?:{CITY_WORD})市?)\s*[)）]", t)
    if m:
        return m.group(1)
    return ""


def scan_zhiye(site: dict) -> list:
    import requests
    base = site["base"].rstrip("/")
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Content-Type": "application/json",
                      "Origin": base, "Referer": base + "/campus"})
    pid = zhiye_portal_id(base, site.get("portal_id", ""), site.get("category", "2"), s,
                          pages=[site.get("url") or base + "/campus", base + "/campus"])
    out, page = [], 0
    while page < 5:                      # 上限 5 页 × 50，防失控
        r = s.post(base + "/api/Jobad/GetJobAdPageList", json={
            "Category": [site.get("category", "2")], "PageIndex": page,
            "PageSize": 50, "KeyWords": "", "SpecialType": 0,
            "PortalId": pid, "DisplayFields": []}, timeout=25)
        d = r.json()
        data = d.get("Data") or []
        for it in data:
            duty, require = it.get("Duty") or "", it.get("Require") or ""
            jd = "\n".join(x for x in (duty, require) if x)
            batch = site.get("label") or extract_grad(it.get("JobAdName", "")) and f"{extract_grad(it.get('JobAdName',''))}届" or ""
            city = "、".join(it.get("LocNames") or []) or city_from_title(it.get("JobAdName", "")) or "待核实"
            out.append({
                "key": make_key(site["name"], str(it["JobAdId"]),
                                city, batch),
                "company": site["name"],
                "title": (it.get("JobAdName") or "").strip(),
                "city": city,
                "type": site.get("type_label") or it.get("Category") or ("校招" if site.get("category") == "2" else "社招"),
                "batch": batch,
                "grad_year": extract_grad(it.get("JobAdName", "")) or extract_grad(batch),
                "duty": duty, "require": require,
                "jd": jd.strip(),
                "links": [base + "/campus"],
                "src": "zhiye", "label": site.get("label", "")})
        got = len(data)
        page += 1
        if got < 50 or page * 50 >= (d.get("Count") or 0):
            break
    print(f"  [zhiye] {site['name']}: {len(out)} 岗")
    return out


def scan_feishu(site: dict) -> list:
    """渲染门户页 → 监听 search/job/posts 自然响应 → 合并去重。"""
    from playwright.sync_api import sync_playwright
    jobs: dict = {}
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(channel="msedge")
        pg = browser.new_page(user_agent=UA)

        def on_resp(r):
            if "search/job/posts" in r.url and r.request.method == "POST":
                try:
                    dd = (r.json().get("data") or {})
                    for j in dd.get("job_post_list") or []:
                        jobs[j["id"]] = j
                except Exception:
                    pass
        pg.on("response", on_resp)
        # networkidle 在慢门户上易超时；部分门户首个请求 405 后重试（csrf 流程）：
        # domcontentloaded + 显式等到 200 的岗位响应（最长 45s，/s/ 分享短链会先 302）+ 兜底等待
        with pg.expect_response(
                lambda r: "search/job/posts" in r.url and r.status == 200,
                timeout=45000) as ri:
            pg.goto(site["url"], timeout=60000, wait_until="domcontentloaded")
            pg.wait_for_timeout(4000)
            try:                      # 营销落地页需点「职位」进入列表路由才发岗位 XHR
                pg.locator("text=职位").first.click(timeout=4000)
            except Exception:
                pass
            try:                      # /s/xxx 内推分享页需点「查看全部职位/校招内推」类入口
                pg.locator("text=/查看全部职位|校招内推|社招内推|全部职位|查看更多|校园招聘/").first.click(timeout=5000)
            except Exception:
                pass
        pg.wait_for_timeout(2500)
        for _ in range(8):               # 尝试「加载更多」类按钮
            btn = pg.locator("text=/加载更多|查看更多|更多岗位|load more/i").first
            if btn.count() == 0:
                break
            try:
                btn.scroll_into_view_if_needed(timeout=3000)
                btn.click(timeout=3000)
                pg.wait_for_timeout(1500)
            except Exception:
                break
        for _ in range(4):               # 滚动兜底
            pg.mouse.wheel(0, 3000)
            pg.wait_for_timeout(900)
        browser.close()
    batch = site.get("label") or ""
    out = []
    for jid, j in jobs.items():
        city = "、".join(c.get("name", "") for c in (j.get("city_list") or []) if c.get("name"))
        desc = (j.get("description") or "")[:1500]
        grad = extract_grad(j.get("title", "")) or extract_grad(batch)
        out.append({
            "key": make_key(site["name"], jid, city, batch),
            "company": site["name"],
            "title": (j.get("title") or "").strip(),
            "city": city or "待核实",
            "type": site.get("type_label", "校招"),
            "batch": batch,
            "grad_year": grad,
            "duty": desc, "require": "",
            "jd": desc,
            "links": [site["url"].split("?")[0]],
            "src": "feishu", "label": site.get("label", "")})
    print(f"  [feishu] {site['name']}({site.get('label','')}): {len(out)} 岗")
    return out


def scan_hotjob(site: dict) -> list:
    """大易招聘系统（wecruit.hotjob.cn）：公开分页接口，表单 POST，无需登录。

    site: {name, su, base?, url?, label?, type_label?, recruit_type?}
    实测（2026-11-10）：POST /wecruit/positionInfo/listPosition/{su}，
    body=recruitType=1&currentPage=1&pageSize=10&coordinateLat=&coordinateLng=
    返回 data.pageForm.pageData[{postId, postName, postTypeName, workPlaceStr, ...}]
    """
    import requests, time as _t
    su = site["su"]
    base = (site.get("base") or "https://wecruit.hotjob.cn").rstrip("/")
    referer = site.get("url") or f"{base}/{su}/mc/position/campus"
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "X-Requested-With": "XMLHttpRequest",
                      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "Referer": referer.split("?")[0]})
    api = f"{base}/wecruit/positionInfo/listPosition/{su}?iSaJAx=isAjax&request_locale=zh_CN"
    out, page = [], 1
    while page <= 20:                      # 上限 20 页 × 10，防失控
        r = s.post(api, data={"recruitType": site.get("recruit_type", 1),
                              "currentPage": page, "pageSize": 10,
                              "coordinateLat": "", "coordinateLng": ""}, timeout=25)
        pf = ((r.json().get("data") or {}).get("pageForm") or {})
        data = pf.get("pageData") or []
        if not data:
            break
        for it in data:
            title = (it.get("postName") or "").strip()
            pid = str(it.get("postId") or it.get("postCode") or title)
            city = (it.get("workPlaceStr") or "").strip() or "待核实"
            kind = (it.get("postTypeName") or "").strip()
            proj = (it.get("projectName") or "").strip()
            out.append({
                "key": make_key(site["name"], pid, city, site.get("label", "")),
                "company": site["name"], "title": title, "city": city,
                "type": site.get("type_label", "校招"),
                "batch": site.get("label", ""),
                "grad_year": extract_grad(title) or extract_grad(site.get("label", "")),
                "duty": "、".join(x for x in (kind, proj) if x), "require": "",
                "jd": "、".join(x for x in (kind, proj) if x),
                "links": [f"{base}/{su}/mc/position/detail/{pid}", referer.split("?")[0]],
                "src": "hotjob", "label": site.get("label", "")})
        if page >= (pf.get("totalPage") or 1):
            break
        page += 1
        _t.sleep(0.8)
    print(f"  [hotjob] {site['name']}({site.get('label', '')}): {len(out)} 岗")
    return out


def scan_moka(site: dict) -> list:
    """Moka 招聘门户（app.mokahr.com）：jobs 接口响应加密，改为渲染列表页后
    从 DOM 抓岗位卡（a[href*="#/job/"]），只读公开列表，不登录。

    site: {name, url, label?, type_label?}  url 为智能表核验过的校招入口
    实测（2026-11-10，大疆）：卡片文本形如「标题|类别|||广东·深圳市|职位简介：…」
    """
    from playwright.sync_api import sync_playwright
    base_url = site["url"].split("#")[0]
    # hash 里带过滤参数（如 #/jobs?commitment=实习）时保留原 hash，否则用默认职位列表
    hash_part = "#" + site["url"].split("#", 1)[1] if "#" in site["url"] else "#/jobs"
    out: dict = {}
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(channel="msedge")
        pg = browser.new_page(user_agent=UA)
        pg.goto(base_url + hash_part, timeout=60000, wait_until="domcontentloaded")
        pg.wait_for_timeout(5000)
        for _ in range(6):                 # 滚动触发懒加载
            pg.mouse.wheel(0, 4000)
            pg.wait_for_timeout(1200)
        cards = pg.evaluate(
            "() => [...document.querySelectorAll('a[href*=\"#/job/\"]')].map(a => ({"
            "href: a.getAttribute('href') || '', txt: (a.innerText || '').trim()}))")
        browser.close()
    city_pat = re.compile(r"北京|上海|深圳|广州|苏州|南京|杭州|成都|武汉|西安|合肥|常州|"
                          r"无锡|宁波|天津|重庆|东莞|佛山|珠海|香港|长沙|郑州|济南|厦门")
    for c in cards:
        href = (c.get("href") or "").strip()
        lines = [x.strip() for x in (c.get("txt") or "").split("\n") if x.strip()]
        if not href or not lines:
            continue
        # 首行可能是「热招」徽标，跳过它取真正的岗位名
        title = ""
        for x in lines:
            if len(x) >= 5 and not x.startswith(("职位简介", "投递", "收藏", "分享")):
                title = re.sub(r"^热招\s*", "", x)[:90]
                break
        if not title:
            continue
        link = href if href.startswith("http") else base_url + href
        m = re.search(r"#/job/([0-9a-zA-Z-]{8,})", href)
        jid = m.group(1) if m else link
        if jid in out:
            continue
        city = next((x for x in lines if x != title and city_pat.search(x)
                     and len(x) <= 24), "")
        city = re.sub(r"^[^·]*·", "", city).strip() or city_from_title(title)
        jd_i = next((i for i, x in enumerate(lines) if x.startswith("职位简介")), None)
        jd = (lines[jd_i].split("：", 1)[-1] if jd_i is not None
              and "：" in lines[jd_i] else " ".join(lines[1:4]))[:400]
        out[jid] = {
            "key": make_key(site["name"], jid, city, site.get("label", "")),
            "company": site["name"], "title": title, "city": city or "待核实",
            "type": site.get("type_label", "校招"),
            "batch": site.get("label", ""),
            "grad_year": extract_grad(title) or extract_grad(site.get("label", "")),
            "duty": jd, "require": "", "jd": jd,
            "links": [link, base_url], "src": "moka", "label": site.get("label", "")}
    print(f"  [moka] {site['name']}({site.get('label', '')}): {len(out)} 岗")
    return list(out.values())


ADAPTERS = {"zhiye": scan_zhiye, "feishu": scan_feishu,
            "hotjob": scan_hotjob, "moka": scan_moka}


# ---------------------------------------------------------------- main
def scan_all() -> int:
    pool = json.loads(POOL.read_text(encoding="utf-8")).get("companies", [])
    today = datetime.now(CST).strftime("%Y-%m-%d %H:%M")
    scans: dict = {}
    skipped = 0
    for comp in pool:
        if not comp.get("enabled"):
            continue
        # 主入口 + extra_sources（同公司多个招聘入口：校招/实习/专项计划分开扫）
        srcs = ([comp["source"]] if comp.get("source") else []) + \
               [x.get("source") for x in comp.get("extra_sources", []) if x.get("source")]
        for src in srcs:
            site = {"name": comp["company_name"], "tier": comp.get("tier"),
                    "ats_type": comp.get("ats_type"), **src}
            site.setdefault("label", "")
            ats = site.get("ats_type") or comp.get("ats_type")
            if not ats or ats not in ADAPTERS:
                continue
            sid = f"{site['name']}·{site.get('label', '')}"
            try:
                jobs = None
                for attempt in (1, 2):          # 渲染类源偶发超时（csrf 流程/慢页面），重试一次
                    try:
                        jobs = ADAPTERS[ats](site)
                        break
                    except Exception as e:
                        if attempt == 1:
                            print(f"  [retry] {site['name']}: {type(e).__name__}，重试一次")
                            import time as _t2
                            _t2.sleep(3)
                        else:
                            raise
                kept = []
                for j in jobs:
                    if EXCLUDE_PAT.search(j.get("title") or ""):
                        skipped += 1
                        continue
                    j["source_id"] = sid
                    j["families"] = families_of(j.get("title"), j.get("jd"))
                    kept.append(annotate_job(classify_job(j, site)))   # V1.8 分类 + V2.0 条件/相关度
                scans[sid] = {"status": "success", "jobs": kept, "error": None}
            except Exception as e:
                scans[sid] = {"status": "failed", "jobs": [], "error": f"{type(e).__name__} {str(e)[:100]}"}
                print(f"  [FAIL] {site['name']}: {e}")

    old = json.loads(RADAR.read_text(encoding="utf-8")) if RADAR.exists() else {"jobs": []}
    merged, src_states = reconcile(old.get("jobs", []), scans, today)
    # 旧快照里保留下来的岗位（失败源/未扫到）也要有分类字段；classify_job 幂等
    sites = site_by_source(pool)
    merged = [classify_job(j, sites.get(j.get("source_id") or "")) for j in merged]
    merged.sort(key=lambda j: (j["company"], j.get("batch") or "", j["title"]))

    by_key = {j["key"]: j for j in merged}
    old_by_key = {j["key"]: j for j in old.get("jobs", [])}
    added = [k for k in by_key if k not in old_by_key]
    removed = [k for k in old_by_key if k not in by_key and old_by_key[k].get("status") != "suspect"]
    changed = [k for k in by_key if k not in added and old_by_key.get(k, {}).get("jd_hash") and
               by_key[k].get("prev_jd_hash") != by_key[k].get("jd_hash")]
    suspects = [k for k in by_key if by_key[k].get("status") == "suspect"]

    # 公司覆盖率（评审 §四.2）：池总量 / 已配置源 / 本次成功 / ATS 分布
    enabled = [c for c in pool if c.get("enabled") and c.get("source")]
    from collections import Counter
    ats_dist = Counter(c["ats_type"] for c in pool if c.get("source"))
    pool_stats = {
        "pool_total": len(pool),
        "enabled": len(enabled),
        "scanned_ok": sum(1 for v in src_states.values() if v["status"] == "success"),
        "ats_dist": dict(ats_dist),
        "skipped_jobs": skipped,
    }
    fam_stat = Counter()
    for j in merged:
        if j.get("status") == "open":
            for f in (j.get("families") or ["其他"]):
                fam_stat[f] += 1
    snap = {"updated": datetime.now(CST).isoformat(timespec="seconds"),
            "sources": [{"source_id": k, **v} for k, v in src_states.items()],
            "pool_stats": pool_stats,
            "family_stats": dict(fam_stat),
            **class_stats_of(merged),
            "jobs": merged}
    RADAR.parent.mkdir(parents=True, exist_ok=True)
    RADAR.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")

    n_ok = sum(1 for v in src_states.values() if v["status"] == "success")
    lines = [
        f"# 岗位雷达报告 · {today}",
        "",
        f"- 监控源 {len(src_states)} 个（成功 {n_ok} / 失败 {len(src_states) - n_ok}）· 快照岗位 **{len(merged)}**",
        f"- 新增 **{len(added)}** · 下线 **{len(removed)}** · JD 变更 **{len(changed)}** · 疑似下线 **{len(suspects)}**",
        f"- 说明：采集失败 ≠ 岗位下线；连续 {SUSPECT_AFTER} 次成功扫描未见才标记疑似下线（suspect），需人工核实",
    ]
    lines.append("\n## 岗位族覆盖（open 岗位按族统计）")
    lines.append("| 岗位族 | 官方在招 |")
    lines.append("| --- | --- |")
    for fam, _ in JOB_FAMILIES:
        lines.append(f"| {fam} | {fam_stat.get(fam, 0)} |")
    lines.append(f"| 其他 | {fam_stat.get('其他', 0)} |")
    lines.append(f"\n公司池 {pool_stats['pool_total']} 家：启用 {pool_stats['enabled']} · 本次成功 {pool_stats['scanned_ok']} · ATS 分布 {pool_stats['ats_dist']} · 排除无关岗 {skipped}")
    lines += class_section(snap)
    if added:
        lines.append("\n## 新增岗位")
        lines += [f"- **{by_key[k]['company']} · {by_key[k]['title']}**（{by_key[k]['city']}｜{by_key[k].get('label') or by_key[k]['type']}）" for k in added]
    if changed:
        lines.append("\n## JD 变更（语义分类）")
        for k in changed:
            j = by_key[k]
            kinds = (j.get("change_log") or [{}])[0].get("kinds", ["内容变化"])
            lines.append(f"- **{j['company']} · {j['title']}**：{'、'.join(kinds)}")
    if removed:
        lines.append("\n## 下线岗位")
        lines += [f"- {old_by_key[k]['company']} · {old_by_key[k]['title']}" for k in removed]
    if suspects:
        lines.append("\n## 疑似下线（连续未见，需人工核实）")
        lines += [f"- {by_key[k]['company']} · {by_key[k]['title']}（连续 {by_key[k]['consecutive_missing']} 次未出现）" for k in suspects]
    fails = [(k, v) for k, v in src_states.items() if v["status"] != "success"]
    if fails:
        lines.append("\n## 失败源（不参与下线判断）")
        lines += [f"- {k}：{v['error'] or '未知错误'}" for k, v in fails]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"快照 {len(merged)} 岗 → {RADAR.name}；新增 {len(added)} / 下线 {len(removed)} / 变更 {len(changed)} / 疑似 {len(suspects)}；源成功 {n_ok}/{len(src_states)}")
    return 0


def reclassify() -> int:
    """V1.8：离线重算全部岗位的招聘性质，不联网、不改动岗位内容与状态机。"""
    if not RADAR.exists():
        print("快照不存在，请先 --scan")
        return 1
    pool = json.loads(POOL.read_text(encoding="utf-8")).get("companies", [])
    sites = site_by_source(pool)
    snap = json.loads(RADAR.read_text(encoding="utf-8"))
    snap["jobs"] = [classify_job(j, sites.get(j.get("source_id") or ""))
                    for j in snap.get("jobs", [])]
    snap.update(class_stats_of(snap["jobs"]))
    RADAR.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")
    section = "\n".join(class_section(snap)) + "\n"
    old = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    head = old.split("\n## 招聘性质分类")[0].rstrip() + "\n"
    REPORT.write_text(head + section, encoding="utf-8")
    print("招聘性质分类：" + " · ".join(
        f"{k} {v}" for k, v in snap["class_stats"].items()))
    print("判定依据：" + " · ".join(
        f"{k} {v}" for k, v in snap["class_basis_stats"].items()))
    interns = [j for j in snap["jobs"] if j["job_class"] == "实习"]
    print(f"实习岗 {len(interns)} 个：" + "；".join(
        f"{j['company']}·{j['title']}" for j in interns[:8]))
    return 0


def annotate_snapshot() -> int:
    """读快照 → 逐岗补 V2.0 字段 → 写回 + 统计。不联网、幂等。"""
    d = json.loads(RADAR.read_text(encoding="utf-8"))
    jobs = [annotate_job(j) for j in d.get("jobs", [])]
    d["jobs"] = jobs
    d["tech_stats"] = annotate_stats(jobs)
    RADAR.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    st = d["tech_stats"]
    print(f"已补标 {st['jobs']} 岗：技术岗 {st['tech_relevant']} / 非技术 {st['non_tech']}，"
          f"岗位族低置信 {st['family_low']}，硬性条件可抽取 {st['req_known']}"
          f"（{st['req_known_pct']}%）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true", help="扫描全部监控源")
    ap.add_argument("--reclassify", action="store_true",
                    help="离线重算招聘性质分类（校招/实习/社招），不联网")
    ap.add_argument("--annotate", action="store_true",
                    help="离线补 V2.0 字段（硬性条件/技术相关度/岗位族置信度），不联网")
    args = ap.parse_args()
    if args.scan:
        return scan_all()
    if args.reclassify:
        return reclassify()
    if args.annotate:
        return annotate_snapshot()
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
