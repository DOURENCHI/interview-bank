# -*- coding: utf-8 -*-
"""从 job_profiles.json 生成岗位种子 companies/jobs.json。

每个岗位模板展开成一个岗位卡：公司名取第一条 JD 证据「·」前段（学校就业网则顺延），
JD 原文 = 全部证据拼接，链接 = jd_sources，技能 = keywords。
人工在网页上添加的岗位存 localStorage（ib_jobs_v1），与此文件在构建产物中合并。
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHOOL_PAT = re.compile(r"就业网|招聘网|大学|学院|bysjy|niuqizp|归纳|待收集")


def company_of(evidence: str) -> str:
    seg = evidence.split("·")[0].strip()
    return seg


def usable_company(c: str) -> bool:
    return bool(c) and len(c) <= 20 and not SCHOOL_PAT.search(c)


def main() -> int:
    pj = ROOT / "companies" / "job_profiles.json"
    profiles = json.loads(pj.read_text(encoding="utf-8")).get("profiles", [])
    jobs = []
    for p in profiles:
        evs = p.get("jd_evidence") or []
        links = p.get("jd_sources") or []
        # 公司名：优先取第一条非学校渠道、非说明文字的证据
        company = ""
        for ev in evs:
            c = company_of(ev)
            if usable_company(c):
                company = c
                break
        ev_text = "；".join(evs)
        grad = None
        m = re.search(r"(20\d{2})\s*届", ev_text + " " + p["name"])
        if m:
            grad = int(m.group(1))
        jobs.append({
            "id": "job_" + p["id"],
            "company": p.get("company") or company or "待核实",
            "title": p["name"],
            "city": p.get("city") or "待核实",
            "type": "校招",
            "status": "待核实",
            "batch": f"{grad}届" if grad else "",
            "grad_year": grad,
            "jd": ev_text,
            "links": links,
            "skills": p.get("keywords", []),
            "prof": p["id"],
            "src": "job_profiles",
            "found": date.today().isoformat(),
        })
    out = ROOT / "companies" / "jobs.json"
    out.write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"生成 {out}（{len(jobs)} 个岗位）")
    for j in jobs:
        print(f"  {j['company']} · {j['title']} · 链接{len(j['links'])}条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
