#!/usr/bin/env python3
"""ATS 识别：输入公司招聘官网 URL，识别背后的招聘系统，输出公司池配置片段建议。

用法：
  python tools/detect_ats.py --url "https://xxx.zhiye.com/campus" --company 某公司

识别规则（先域名后指纹，低频只读一次）：
  *.zhiye.com            → zhiye（北森智业云，适配器已有）
  *.jobs.feishu.cn       → feishu（适配器已有）
  app.mokahr.com/*       → moka（适配器待写，先记录）
  *.hotjob.cn            → 大易/Hotjob（待适配）
  talent.baidu.com 等    → 自建（unknown，人工看）
"""
import argparse
import json
import re
import sys
from pathlib import Path

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

DOMAIN_RULES = [
    (r"\.zhiye\.com", "zhiye", "北森智业云（适配器已有：GetJobAdPageList）"),
    (r"\.jobs\.feishu\.cn", "feishu", "飞书招聘（适配器已有：渲染+响应监听）"),
    (r"mokahr\.com", "moka", "Moka（适配器待写，已记录）"),
    (r"\.hotjob\.cn", "hotjob", "大易/Hotjob（待适配）"),
    (r"talent\.didi", "didi-internal", "自建（待适配）"),
    (r"campus\. pony\.ai|careers\.dji\.com", "self-built", "自建站（人工核验接口）"),
]

FINGERPRINTS = [
    (r"北森|beisen|zhiye", "zhiye"),
    (r"飞书|feishu", "feishu"),
    (r"moka|mokahr", "moka"),
]


def detect(url: str) -> dict:
    out = {"url": url, "ats_type": "unknown", "how": "no-match", "advice": "人工打开页面，找 XHR 接口（Playwright 监听最快）", "source": None}
    for pat, ats, note in DOMAIN_RULES:
        if re.search(pat, url, re.I):
            out["ats_type"] = ats
            out["how"] = "domain"
            out["advice"] = note
            break
    if out["ats_type"] == "unknown":
        try:
            import requests
            r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
            body = r.text
            for pat, ats in FINGERPRINTS:
                if re.search(pat, body, re.I):
                    out["ats_type"] = ats
                    out["how"] = "fingerprint"
                    out["advice"] = "页面指纹命中"
                    break
        except Exception as e:
            out["advice"] = f"页面抓取失败：{type(e).__name__} {str(e)[:80]}"
    # 配置片段建议
    if out["ats_type"] == "zhiye":
        m = re.search(r"(https://[a-z0-9-]+\.zhiye\.com)", url)
        out["source"] = {"base": m.group(1), "portal_id": "", "category": "2"}
    elif out["ats_type"] == "feishu":
        out["source"] = {"url": url, "label": "待补批次", "type_label": "校招"}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--company", default="")
    args = ap.parse_args()
    d = detect(args.url)
    frag = {"company_name": args.company or "(公司名)",
            "category": "(类别)", "directions": [], "tier": "B",
            "career_url": args.url, "ats_type": d["ats_type"],
            "source": d["source"], "enabled": bool(d["source"]),
            "note": d["advice"]}
    print(json.dumps({"detect": d, "pool_fragment": frag}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
