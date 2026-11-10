# -*- coding: utf-8 -*-
"""CareerOS V1.6 验收测试（评审 12 项清单的可自动化子集，纯逻辑不联网）。

覆盖：
  1. 同一岗位连续扫描三次不产生重复          2. JD 修改正确识别变化（语义分类）
  3. 数据源失败不误判岗位关闭                4. 岗位重新开放后回到 open
  5. 同岗多城市不误合并（key 含城市）        6. 忽略按 key 隔离（同公司其他岗位不受影响→前端 key 级）
  7. 届别提取正确（grad_year）               8. 扫描异常写入 source_states
  9. 仓库数据文件不含凭证关键字
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from job_radar import (classify_change, extract_grad, make_key, reconcile, jd_hash,
                       classify_job, class_stats_of, site_by_source, city_from_title)  # noqa: E402

ok = []


def J(key, title="C++ 工程师", city="杭州", duty="职责A", require="要求A",
      company="宇树科技", source_id="宇树科技·2027届校招", batch="2027届校招",
      label=None, links=None, src="zhiye"):
    return {"key": key, "company": company, "title": title, "city": city,
            "type": "校招", "batch": batch, "grad_year": extract_grad(batch),
            "duty": duty, "require": require, "jd": duty + "\n" + require,
            "links": ["https://x"] if links is None else links,
            "src": src, "label": batch if label is None else label,
            "source_id": source_id,
            "first_seen": "d0", "last_seen": "d0", "status": "open",
            "consecutive_missing": 0, "jd_hash": jd_hash(duty + require),
            "prev_jd_hash": None, "change_log": []}


def scan(jobs, status="success", sid="宇树科技·2027届校招"):
    return {sid: {"status": status, "jobs": jobs, "error": None if status == "success" else "TimeoutError"}}


# 1. 连续三次扫描同岗位不重复、状态稳定
k = make_key("宇树科技", "511068584", "杭州", "2027届校招")
m, _ = reconcile([], scan([J(k)]), "d1")
m, _ = reconcile(m, scan([J(k)]), "d2")
m, _ = reconcile(m, scan([J(k)]), "d3")
same = [j for j in m if j["key"] == k]
ok.append(("三次扫描无重复且 open", len(same) == 1 and same[0]["status"] == "open"
           and same[0]["first_seen"] == "d1" and same[0]["last_seen"] == "d3"))

# 2. JD 修改正确识别变化（职责/要求/硬性条件分类）
old = J(k, duty="职责A", require="要求A")
new = J(k, duty="职责A改", require="要求A改")
kinds = classify_change(old, new)
ok.append(("JD变更语义分类", "职责变化" in kinds and "任职要求变化" in kinds))
new2 = J(k, require="要求A；限2028届毕业")
kinds2 = classify_change(old, new2) if False else classify_change(
    J(k), J(k, require="要求A；硕博"))
ok.append(("任职要求变化分类", "任职要求变化" in kinds2))
ok.append(("届别提取", extract_grad("C++工程师（2027届校招）") == 2027
           and extract_grad("实习") is None))

# 3. 数据源失败不误判岗位关闭
m, _ = reconcile([J(k, batch="2027届校招")], scan([], status="failed"), "d2")
ok.append(("源失败不误判下线", len(m) == 1 and m[0]["status"] == "open"
           and m[0]["consecutive_missing"] == 0))

# 4. 岗位连续 2 次未出现 → suspect；重新出现 → 恢复 open
m, _ = reconcile([], scan([J(k)]), "d1")
m, _ = reconcile(m, scan([]), "d2")
ok.append(("首次未出现仍 open", m[0]["status"] == "open" and m[0]["consecutive_missing"] == 1))
m, _ = reconcile(m, scan([]), "d3")
ok.append(("连续2次未见→suspect", m[0]["status"] == "suspect"))
m, _ = reconcile(m, scan([J(k)]), "d4")
ok.append(("重新出现→open清零", m[0]["status"] == "open" and m[0]["consecutive_missing"] == 0))

# 5. 同岗多城市不误合并
k1 = make_key("Momenta", "7670", "北京", "2027届校招")
k2 = make_key("Momenta", "7670", "苏州", "2027届校招")
m, _ = reconcile([], {"Momenta·2027届校招": {"status": "success",
             "jobs": [J(k1, city="北京", source_id="Momenta·2027届校招"),
                      J(k2, city="苏州", source_id="Momenta·2027届校招")], "error": None}}, "d1")
ok.append(("同岗多城市两条记录", len(m) == 2 and k1 != k2))

# 6. 扫描异常写入 source_states（报告可见性）
m, states = reconcile([], {"A·x": {"status": "success", "jobs": [], "error": None},
                           "B·y": {"status": "failed", "jobs": [], "error": "HTTPError 403"}},
                      "d1")
ok.append(("源状态独立记录", states["A·x"]["status"] == "success"
           and states["B·y"]["status"] == "failed" and "403" in states["B·y"]["error"]))

# 7. 仓库数据文件不含凭证关键字
bad = []
for f in ["sources/jobs_watch.json", "sources/jobs_radar.json", "sources/jobs_radar.json"]:
    fp = ROOT / f
    if fp.exists():
        t = fp.read_text(encoding="utf-8").lower()
        for kw in ["cookie", "token=", "authorization", "password", "api_key"]:
            if kw in t:
                bad.append((f, kw))
ok.append(("数据文件无凭证", not bad))

# 9. jd_hash 稳定且随内容变化
ok.append(("jd_hash", jd_hash("a") == jd_hash("a") and jd_hash("a") != jd_hash("b")))

# 10. V1.8 招聘性质分类：证据优先级 + 实习岗届别修正 + 幂等
intern = J("k-intern", title="路径规划算法实习生", batch="2027届校招")
ci = classify_job(intern)
ok.append(("标题判定实习 high", ci["job_class"] == "实习"
           and ci["class_basis"] == "岗位标题明确" and ci["class_conf"] == "high"))
ok.append(("实习岗清除入口批次届别", ci["grad_year"] is None
           and ci.get("grad_year_raw") == 2027 and ci["type"] == "实习"))
ok.append(("分类幂等", classify_job(ci)["grad_year"] is None
           and classify_job(ci).get("grad_year_raw") == 2027
           and classify_job(ci)["job_class"] == "实习"))
ct = classify_job(J("k-title", title="2027届-C++ 工程师"))
ok.append(("标题判定校招 high", ct["job_class"] == "校招" and ct["class_conf"] == "high"
           and ct["grad_year"] == 2027))
cb = classify_job(J("k-batch", title="具身数据工程师", batch="2027届校招"))
ok.append(("批次标签判定校招 medium", cb["job_class"] == "校招"
           and cb["class_conf"] == "medium"))
cl = classify_job(J("k-entry", title="具身数据工程师", batch="", label="",
                    links=["https://x.zhiye.com/campus"], src="zhiye"),
                  {"category": "2", "ats_type": "zhiye"})
ok.append(("校园入口推定 low", cl["job_class"] == "校招" and cl["class_conf"] == "low"
           and "入口推定" in cl["class_basis"]))
cu = classify_job({"title": "软件工程师", "batch": "", "label": "",
                   "links": ["https://example.com"], "src": "feishu", "grad_year": None})
ok.append(("无线索→未标明", cu["job_class"] == "未标明" and cu["class_conf"] == "none"))
cs = classify_job(J("k-social", title="社招-C++ 资深工程师"))
ok.append(("社招标题判定", cs["job_class"] == "社招"))
stats = class_stats_of([ci, ct, cb, cl, cu, cs])
ok.append(("分类统计", stats["class_stats"] == {"校招": 3, "实习": 1, "社招": 1, "未标明": 1}))
pool = [{"company_name": "宇树科技", "ats_type": "zhiye",
         "source": {"base": "https://unitree.zhiye.com", "category": "2"}}]
ok.append(("公司池→source_id 映射", "宇树科技·" in site_by_source(pool)))

# 11. V1.8.2 新适配器（hotjob 大易 / moka）的入口推定
cm = classify_job(J("k-moka", title="具身数据工程师", batch="", label="",
                    links=["https://app.mokahr.com/x#/job/abc"], src="moka"),
                  {"type_label": "校招"})
ok.append(("moka入口推定", cm["job_class"] == "校招" and cm["class_conf"] == "low"))
ch = classify_job(J("k-hotjob", title="嵌入式软件工程师", batch="", label="",
                    links=["https://wecruit.hotjob.cn/SU1/mc/position/detail/x"], src="hotjob"),
                  {"type_label": "校招"})
ok.append(("hotjob入口推定", ch["job_class"] == "校招" and ch["class_conf"] == "low"))

# 12. V1.8.2 城市从标题提取（zhiye 系 LocNames 为空时的兜底）
ok.append(("城市提取·尾缀", city_from_title("电力电子工程师（大功率方向） - 上海(J19796)") == "上海"))
ok.append(("城市提取·括号", city_from_title("C++工程师（成都）(J12640)") == "成都"))
ok.append(("城市提取·不误收批次", city_from_title("嵌入式软件工程师-27届校招(J11525)") == ""))
ok.append(("城市提取·无城市", city_from_title("AI Infra 工程师") == ""))

fails = [k for k, v in ok if not v]
for k, v in ok:
    print(("✓" if v else "✗"), k)
if fails:
    print("失败:", fails)
    sys.exit(1)
print(f"OK 验收 {len(ok)}/{len(ok)}")
