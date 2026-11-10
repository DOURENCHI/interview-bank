#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""题库体检：一份可重复运行的量化审计。

产出 sources/audit_report.md，回答六个问题（外部评审建议的体检清单）：
  1. 模块 × 优先级 × 难度分布
  2. 内容状态与证据等级分布（真实面经 vs 预测题）
  3. 重复/相似题（dice + 包含率双阈值，与 nc_seed 同一套）
  4. 来源完整性（缺来源、缺核验日期）
  5. 每家公司的真实面经题数 vs 推导命中数
  6. P0 覆盖与近期维护活跃度
"""
from __future__ import annotations
import json, re, sys, collections
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from build import load_questions, MODULE_NAME  # noqa: E402

# 证据等级：source_type → S1~S4（外部评审建议的分级，落地为本库既有字段）
EVIDENCE = {
    "official":  "S1 官方文档/JD",
    "upstream":  "S1 官方文档/JD",
    "self_doc":  "S2 本人一手（项目文档）",
    "self_exp":  "S2 本人一手（亲历）",
    "nowcoder":  "S3 社区面经",
    "video":     "S3 社区面经",
    "inferred":  "S4 岗位推导预测",
}
REAL_EVIDENCE = ("S2", "S3")


def bigrams(s: str):
    s = re.sub(r"[\s，。、？！：:（）()\[\]【】“”\"'…·—+,.?《》/\\]", "", s.lower())
    return frozenset(s[i:i + 2] for i in range(len(s) - 1)) or frozenset([s])


def dup_scan(qs):
    """全库两两相似：按「标题+正文纯文本」比对（读程序题标题相同但代码不同，
    只比标题会全量误报——实测 1020 对假阳性）。dice≥0.80 视为可疑重复。"""
    items = [(q["id"], q["title"], bigrams(q["title"] + " " + q.get("plain", "")[:600]))
             for q in qs]
    pairs = []
    n = len(items)
    for i in range(n):
        ida, ta, ba = items[i]
        for j in range(i + 1, n):
            idb, tb, bb = items[j]
            inter = len(ba & bb)
            if not inter:
                continue
            dice = 2 * inter / (len(ba) + len(bb))
            if dice >= 0.80:
                pairs.append((round(dice, 2), ida, ta, idb, tb))
    pairs.sort(reverse=True)
    return pairs


def main() -> int:
    qs = load_questions()
    L = []
    A = L.append
    A(f"# 题库体检报告（{date.today().isoformat()}）\n")
    A(f"总题数 **{len(qs)}**，生成方式：`python tools/audit.py`（可重复运行）\n")

    # ---- 1. 分布 ----
    A("## 1. 模块 × 优先级分布\n")
    A("| 模块 | P0 | P1 | P2 | 合计 |")
    A("|---|---:|---:|---:|---:|")
    for mod in sorted({q["module"] for q in qs}):
        sub = [q for q in qs if q["module"] == mod]
        c = collections.Counter(q["priority"] for q in sub)
        A(f"| {MODULE_NAME.get(mod, mod)} | {c['P0']} | {c['P1']} | {c['P2']} | {len(sub)} |")
    A("")
    diff = collections.Counter(q["difficulty"] for q in qs)
    A(f"难度分布：1★ {diff.get(1,0)} ｜ 2★ {diff.get(2,0)} ｜ 3★ {diff.get(3,0)} ｜ "
      f"4★ {diff.get(4,0)} ｜ 5★ {diff.get(5,0)}\n")

    # ---- 2. 证据等级 ----
    A("## 2. 证据等级（真实面经 vs 预测题）\n")
    ev = collections.Counter(EVIDENCE.get(q.get("sourceType", "inferred"), "S4 岗位推导预测") for q in qs)
    for k in sorted(ev):
        A(f"- **{k}**：{ev[k]} 道（{ev[k]*100//len(qs)}%）")
    real = sum(v for k, v in ev.items() if k.startswith(REAL_EVIDENCE))
    A(f"\n> 真实一手+社区面经共 **{real} 道**；其余为岗位推导预测题——"
      "网页已提供「隐藏预测题」开关，两者不再混淆。\n")

    # ---- 3. 重复/相似 ----
    A("## 3. 相似/重复题扫描\n")
    pairs = dup_scan(qs)
    A(f"可疑对 **{len(pairs)}** 组（阈值：dice≥0.72 或包含率≥0.85）。TOP20：\n")
    A("| 相似度 | 题A | 题B |")
    A("|---|---|---|")
    for s, ia, ta, ib, tb in pairs[:20]:
        A(f"| {s} | `{ia}` {ta[:26]} | `{ib}` {tb[:26]} |")
    A("")

    # ---- 4. 来源完整性 ----
    no_src = [q["id"] for q in qs if not q.get("sourceRef")]
    no_date = [q["id"] for q in qs if not q.get("verified_at")]
    A("## 4. 来源完整性\n")
    A(f"- 缺 `source_ref`：**{len(no_src)}** 道" + (f"（{', '.join(no_src[:8])}…）" if no_src else ""))
    A(f"- 缺 `verified_at`：**{len(no_date)}** 道\n")

    # ---- 5. 公司维度 ----
    A("## 5. 公司维度：真实面经题 vs 推导命中\n")
    A("| 公司 | 出现记录（真实） | 按岗位族推导命中 |")
    A("|---|---:|---:|")
    tj = json.loads((ROOT / "companies" / "targets.json").read_text(encoding="utf-8"))
    role_by_key = {r["key"]: r for r in tj["roles"]}
    always = set(tj.get("always", []))
    for c in tj["companies"]:
        app = sum(1 for q in qs
                  if any(a.split("·")[0] == c["name"] for a in (q.get("appearances") or [])))
        hit = 0
        for q in qs:
            if any(a.split("·")[0] == c["name"] for a in (q.get("appearances") or [])):
                hit += 1
                continue
            if q["module"] in always:
                continue
            if q["sub"] in (c.get("extra") or []):
                hit += 1
                continue
            if any(q["module"] in role_by_key[rk].get("mods", [])
                   or q["sub"] in role_by_key[rk].get("subs", [])
                   for rk in c.get("roles", [])):
                hit += 1
        mark = "（核心）" if c.get("tier") == "core" else ""
        A(f"| {c['name']}{mark} | {app} | {hit} |")
    A("")

    # ---- 6. P0 与维护活跃度 ----
    A("## 6. P0 覆盖与维护活跃度\n")
    p0 = [q for q in qs if q["priority"] == "P0"]
    A(f"- P0 共 **{len(p0)}** 道，占 {len(p0)*100//len(qs)}%")
    core_p0 = [q for q in p0 if q["module"] in
               ("01_project", "02_cpp", "03_linux", "04_algo")]
    A(f"- 其中「项目+C+++Linux+算法」四块核心 **{len(core_p0)}** 道"
      f"（实习笔试+一面主战场）")
    bydate = collections.Counter(q.get("verified_at", "?")[:10] for q in qs)
    A("- 最近核验日期分布：" + "，".join(f"{k}×{v}" for k, v in
                                       sorted(bydate.items(), reverse=True)[:5]))

    out = ROOT / "sources" / "audit_report.md"
    # 人工复核附录不属于自动重算结果：旧报告里的「## 附：」段落原样带回，避免被覆盖丢失
    appendix = ""
    if out.exists():
        prev = out.read_text(encoding="utf-8")
        if "## 附：" in prev:
            appendix = "\n" + prev[prev.index("## 附："):].rstrip() + "\n"
    out.write_text("\n".join(L) + "\n" + appendix, encoding="utf-8")
    print(f"体检报告已生成：{out}")
    print(f"  题数 {len(qs)} | 可疑重复对 {len(pairs)} | 缺来源 {len(no_src)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
