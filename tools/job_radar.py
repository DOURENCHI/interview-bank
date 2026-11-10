#!/usr/bin/env python3
"""岗位雷达：低频增量监控目标公司官方招聘门户（CareerOS V1.7：覆盖率升级）。

V1.7：公司池驱动——扫描对象来自 companies/radar_companies.json（enabled=true 且带 source），
不再硬编码；岗位按四层岗位族关键词自动打标（families），命中排除词的岗位直接跳过并计数；
快照附 pool_stats（公司覆盖率）与 families 统计。

用法：
  python tools/job_radar.py --scan      # 扫描全部监控源 → sources/jobs_radar.json + radar_report.md

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

# 四层岗位族关键词（V1.7）：很多公司不用新词，传统岗位名也要命中
JOB_FAMILIES = [
    ("AI推理部署", ["模型部署", "推理优化", "推理", "inference", "tensorrt", "onnx",
                    "边缘计算", "异构计算", "ai runtime", "部署工程师", "量化", "编译优化"]),
    ("机器人软件/ROS2", ["机器人软件", "ros", "机器人中间件", "运动控制", "导航",
                        "规划控制", "系统集成", "机器人系统", "机器人算法"]),
    ("C++ SDK/系统软件", ["c++", "sdk", "平台软件", "基础软件", "车载软件",
                          "基础组件", "系统软件", "中间件"]),
    ("VLM/VLA/视觉算法", ["视觉算法", "感知算法", "vlm", "vla", "多模态", "世界模型",
                          "端到端", "强化学习", "图像算法", "具身智能"]),
    ("嵌入式/控制", ["嵌入式", "固件", "bsp", "驱动", "单片机", "mcu",
                    "电机驱动", "硬件工程师"]),
]
# 轻排除：只排明确无关岗，不排算法岗（视觉/VLA 是第二优先级方向）
EXCLUDE_PAT = re.compile(
    r"销售|售前|实施顾问|产品经理|市场(?!营销算法)|行政|人事|hr|h r|财务|会计|法务|"
    r"商务|运营专员|客服|采购|行政专员|设计师|视觉设计|平面|品牌|文案|直播|电商运营")


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

def zhiye_portal_id(base: str, portal_id: str, category: str, s) -> str:
    """portal_id 留空时：从 /campus HTML 提取候选，逐个试到 Count>0。"""
    if portal_id:
        return portal_id
    h = s.get(base + "/campus", timeout=25).text
    cands = list(dict.fromkeys(re.findall(
        r'"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"', h)))
    for pid in cands:
        try:
            r = s.post(base + "/api/Jobad/GetJobAdPageList", json={
                "Category": [category], "PageIndex": 0, "PageSize": 1,
                "KeyWords": "", "SpecialType": 0, "PortalId": pid,
                "DisplayFields": []}, timeout=20)
            if r.status_code == 200 and r.json().get("Count", 0) > 0:
                print(f"  [zhiye] 动态 portalId={pid} 命中 {r.json()['Count']} 岗")
                return pid
        except Exception:
            continue
    raise RuntimeError("未能确定 portalId")


def scan_zhiye(site: dict) -> list:
    import requests
    base = site["base"].rstrip("/")
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Content-Type": "application/json",
                      "Origin": base, "Referer": base + "/campus"})
    pid = zhiye_portal_id(base, site.get("portal_id", ""), site.get("category", "2"), s)
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
            out.append({
                "key": make_key(site["name"], str(it["JobAdId"]),
                                "、".join(it.get("LocNames") or []), batch),
                "company": site["name"],
                "title": (it.get("JobAdName") or "").strip(),
                "city": "、".join(it.get("LocNames") or []) or "待核实",
                "type": it.get("Category") or ("校招" if site.get("category") == "2" else "社招"),
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
        # domcontentloaded + 显式等到 200 的岗位响应（最长 25s）+ 兜底等待
        with pg.expect_response(
                lambda r: "search/job/posts" in r.url and r.status == 200,
                timeout=25000) as ri:
            pg.goto(site["url"], timeout=60000, wait_until="domcontentloaded")
            pg.wait_for_timeout(3000)
            try:                      # 营销落地页需点「职位」进入列表路由才发岗位 XHR
                pg.locator("text=职位").first.click(timeout=4000)
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


ADAPTERS = {"zhiye": scan_zhiye, "feishu": scan_feishu}


# ---------------------------------------------------------------- main
def scan_all() -> int:
    pool = json.loads(POOL.read_text(encoding="utf-8")).get("companies", [])
    today = datetime.now(CST).strftime("%Y-%m-%d %H:%M")
    scans: dict = {}
    skipped = 0
    for comp in pool:
        if not comp.get("enabled") or not comp.get("source"):
            continue
        site = {"name": comp["company_name"], "tier": comp.get("tier"),
                **comp["source"]}
        site.setdefault("label", "")
        sid = f"{comp['company_name']}·{site.get('label', '')}"
        try:
            jobs = ADAPTERS[comp["ats_type"]](site)
            kept = []
            for j in jobs:
                if EXCLUDE_PAT.search(j.get("title") or ""):
                    skipped += 1
                    continue
                j["source_id"] = sid
                j["families"] = families_of(j.get("title"), j.get("jd"))
                kept.append(j)
            scans[sid] = {"status": "success", "jobs": kept, "error": None}
        except Exception as e:
            scans[sid] = {"status": "failed", "jobs": [], "error": f"{type(e).__name__} {str(e)[:100]}"}
            print(f"  [FAIL] {site['name']}: {e}")

    old = json.loads(RADAR.read_text(encoding="utf-8")) if RADAR.exists() else {"jobs": []}
    merged, src_states = reconcile(old.get("jobs", []), scans, today)
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true", help="扫描全部监控源")
    args = ap.parse_args()
    if args.scan:
        return scan_all()
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
