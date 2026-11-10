#!/usr/bin/env python3
"""岗位雷达：低频增量监控目标公司官方招聘门户（CareerOS V1.5）。

用法：
  python tools/job_radar.py --scan      # 扫描全部监控源 → sources/jobs_radar.json + radar_report.md

合规边界（写在代码里）：
  * 每源每次只发少量请求（zhiye 1~2 个 POST；feishu 一次页面渲染，靠滚动/自然加载）
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
WATCH = ROOT / "sources" / "jobs_watch.json"
RADAR = ROOT / "sources" / "jobs_radar.json"
REPORT = ROOT / "sources" / "radar_report.md"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
CST = timezone(timedelta(hours=8))


def norm_job(company: str, key: str, title: str, city: str, jtype: str,
             jd: str, links: list, src: str, label: str = "") -> dict:
    return {
        "key": key,
        "company": company,
        "title": (title or "").strip(),
        "city": city or "待核实",
        "type": jtype or "校招",
        "jd": (jd or "").strip(),
        "links": links,
        "status": "招聘中",
        "src": src,
        "label": label,
        "found": datetime.now(CST).strftime("%Y-%m-%d"),
    }


# ---------------------------------------------------------------- zhiye
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
            jd = "\n".join(x for x in (it.get("Duty"), it.get("Require")) if x)
            out.append(norm_job(
                site["name"], f"{site['name']}:{it['JobAdId']}",
                it.get("JobAdName", ""), "、".join(it.get("LocNames") or []),
                it.get("Category") or ("校招" if site.get("category") == "2" else "社招"),
                jd, [base + "/campus"], "zhiye", site.get("label", "")))
        got = len(data)
        page += 1
        if got < 50 or page * 50 >= (d.get("Count") or 0):
            break
    print(f"  [zhiye] {site['name']}: {len(out)} 岗")
    return out


# ---------------------------------------------------------------- feishu
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
        pg.goto(site["url"], timeout=45000, wait_until="networkidle")
        pg.wait_for_timeout(2000)
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
    out = []
    for jid, j in jobs.items():
        city = "、".join(c.get("name", "") for c in (j.get("city_list") or []) if c.get("name"))
        out.append(norm_job(
            site["name"], f"{site['name']}:{jid}", j.get("title", ""), city,
            site.get("type_label", "校招"),
            (j.get("description") or "")[:1500],
            [site["url"].split("?")[0]], "feishu", site.get("label", "")))
    print(f"  [feishu] {site['name']}({site.get('label','')}): {len(out)} 岗")
    return out


ADAPTERS = {"zhiye": scan_zhiye, "feishu": scan_feishu}


# ---------------------------------------------------------------- main
def scan_all() -> int:
    watch = json.loads(WATCH.read_text(encoding="utf-8")).get("watch", [])
    all_jobs, failures = [], []
    for site in watch:
        try:
            all_jobs.extend(ADAPTERS[site["type"]](site))
        except Exception as e:
            failures.append(f"{site['name']}({site.get('label','')}): {type(e).__name__} {str(e)[:80]}")
            print(f"  [FAIL] {site['name']}: {e}")

    old = json.loads(RADAR.read_text(encoding="utf-8")) if RADAR.exists() else {"jobs": []}
    old_by_key = {j["key"]: j for j in old.get("jobs", [])}
    new_by_key = {j["key"]: j for j in all_jobs}
    added = [k for k in new_by_key if k not in old_by_key]
    removed = [k for k in old_by_key if k not in new_by_key]

    snap = {"updated": datetime.now(CST).isoformat(timespec="seconds"),
            "jobs": list(new_by_key.values())}
    RADAR.parent.mkdir(parents=True, exist_ok=True)
    RADAR.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")

    # 报告：新增/下线 + JD 变更（title 相同但 jd hash 变化）
    changed = []
    for k, j in new_by_key.items():
        o = old_by_key.get(k)
        if o and o.get("title") == j.get("title"):
            h_old = hashlib.md5((o.get("jd") or "").encode()).hexdigest()
            h_new = hashlib.md5((j.get("jd") or "").encode()).hexdigest()
            if h_old != h_new:
                changed.append(k)
    lines = [
        f"# 岗位雷达报告 · {datetime.now(CST).strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"- 监控源 {len(watch)} 个（失败 {len(failures)}）· 在招岗位 **{len(all_jobs)}**",
        f"- 新增 **{len(added)}** · 下线 **{len(removed)}** · JD 变更 **{len(changed)}**",
    ]
    if added:
        lines.append("\n## 新增岗位")
        for k in added:
            j = new_by_key[k]
            lines.append(f"- **{j['company']} · {j['title']}**（{j['city']}｜{j['label'] or j['type']}）")
    if changed:
        lines.append("\n## JD 变更（关注要求是否加码）")
        for k in changed:
            j = new_by_key[k]
            lines.append(f"- {j['company']} · {j['title']}")
    if removed:
        lines.append("\n## 下线岗位")
        for k in removed:
            j = old_by_key[k]
            lines.append(f"- {j['company']} · {j['title']}")
    if failures:
        lines.append("\n## 失败源")
        lines += [f"- {f}" for f in failures]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"快照 {len(all_jobs)} 岗 → {RADAR.name}；新增 {len(added)} / 下线 {len(removed)} / 变更 {len(changed)}")
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
