#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从本地教学/项目文档批量抽取面试题候选。

为什么要分档：文档的章节标题是教学叙事，不是面试问法。
  「2.3 验证装好了没」      → 操作步骤，不是题
  「它和话题有什么区别」     → "它"脱离上下文，不是题
  「为什么 end 指向后一个」  → 真·机制题
所以按信号强弱分 strong / weak / drop 三档，只有 strong 落成题卡，
weak 只进候选清单供人工挑。

用法:
    python tools/extract.py --scan     预览统计
    python tools/extract.py --write    写题卡 + 候选清单
"""
from __future__ import annotations

import argparse
import html as htmllib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # D:/工程/面试题库
ENG = ROOT.parent                                  # D:/工程
CONTENT = ROOT / "content"

# ---------------------------------------------------------------- 模块映射
# 顺序有关，先匹配到的先用
KEYMAP = [
    ("ROS2",      "06_ros2",       "P1"),
    ("YOLO",      "05_deploy",     "P0"),
    ("端侧AI",     "05_deploy",     "P0"),
    ("STM32",     "09_hardware",   "P1"),
    ("单片机",     "09_hardware",   "P1"),
    ("电子元器件",  "09_hardware",   "P1"),
    ("通信总线",   "09_hardware",   "P1"),
    ("PCB",       "09_hardware",   "P1"),
    ("FreeRTOS",  "09_hardware",   "P1"),
    ("Linux",     "03_linux",      "P0"),
    ("C++",       "02_cpp",        "P0"),
    ("Qt",        "02_cpp",        "P1"),
    ("Python",    "10_cv_pytorch", "P1"),
]
MODULE_NAME = {
    "01_project": "项目深挖", "02_cpp": "C++", "03_linux": "Linux",
    "04_algo": "算法机考", "05_deploy": "模型部署", "06_ros2": "ROS2",
    "07_imaging": "医学影像", "08_robot": "机器人学",
    "09_hardware": "硬件嵌入式", "10_cv_pytorch": "深度学习",
}
ID_BASE = {"01_project": 100, "02_cpp": 600, "03_linux": 1100, "04_algo": 1600,
           "05_deploy": 2100, "06_ros2": 2600, "07_imaging": 3100,
           "08_robot": 3600, "09_hardware": 4100, "10_cv_pytorch": 4600}

SKIP_DIRS = {"_figs", "_work", "_build", "__pycache__", "_archive", "deck"}

# ---------------------------------------------------------------- 分级规则

# 定死不是题的：教学组织 / 操作步骤 / 元信息
DROP_RE = re.compile(
    r"阅读顺序|阅读路径|阅读建议|环境准备|环境要求|前提条件|安装|配置|装好了|"
    r"命令清单|命令列表|目录长什么样|验证|运行一下|启动|编译|创建|新建|"
    r"写一个|动手|练习|小结|自测|附录|参考|速查|清单|索引|前言|导语|"
    r"关于|致谢|收尾|结语|目录|开始之前|这份讲义|这份手册|本讲义|本手册|"
    r"怎么读|怎么用|值得做|学习路线|课程|老师|视频|原话|回顾|总结|复盘|"
    r"下面|上面|上一节|下一节|本节|本章|第一站|第二站|第三站|第四站|第[一二三四五六七八九十]+步|"
    r"^Chapter|^第 *[0-9一二三四五六七八九十]+ *章|组 *·|第 *[0-9]+ *[~～-] *[0-9]+ *题|导学|"
    r"第[一二三四五六七八九十0-9]+ *(段|轮|部分|节)|分钟|[0-9]+ *秒|速记|口述稿|演练|模拟面|"
    r"翻车|别忘了|这张网|各解决|然后决定|一句话|先看|再看|全景|演进|随笔|感受"
)

# 概念型标题：不含疑问词，但本身就是面试必考点（Linux 教程标题多为这种）
# 不放行的话 Linux 模块会整块抽空
TECH_TERM = re.compile(
    r"inode|文件描述符|软链|硬链|权限|umask|进程|线程|僵尸|孤儿|信号|管道|重定向|"
    r"虚拟内存|分页|内存|中断|系统调用|内核|调度|挂载|磁盘|分区|启动流程|"
    r"fork|exec|systemd|锁|死锁|竞态|栈|堆|野指针|内存泄漏|智能指针|虚函数|多态|"
    r"模板|移动语义|右值|左值|引用|拷贝|构造|析构|RAII|STL|迭代器|容器|哈希"
)

# 指代词：脱离上下文就没意义
PRONOUN_RE = re.compile(r"它|它们|这件事|这个东西|这一步|这里|此处|该容器|此函数|这个类|那个")

# 强信号：一望即知是技术问题
STRONG_RE = re.compile(
    r"为什么|是什么|什么是|有什么区别|有什么差别|有何区别|如何|"
    r"原理|机制|本质|作用|优缺点|优点|缺点|区别|差别|对比|关系|"
    r"内存|指针|布局|结构|模型|算法|调度|生命周期|精度|性能|优化|"
    r"陷阱|报错|坑|原因|解决|实现"
)
Q_WORD = re.compile(r"为什么|是什么|什么是|如何|怎么|怎样|哪些|哪个|能否|是否")
CONTRAST = re.compile(r"区别|差别|不同|对比|比较|vs|VS")
TAIL_NOISE = [
    r"[（(](背下来|都要会认|重点|必看|注意|核心|别弄混|记住|划重点|易错|很实用|强烈推荐)[)）]",
    r"[（(]原视频[^)）]*[)）]",
]


def clean_title(raw: str) -> str:
    t = re.sub(r"<[^>]+>", "", raw)
    t = htmllib.unescape(t)
    t = re.sub(r"^\s*[0-9]+(\.[0-9]+)*\s*[、.．:：]?\s*", "", t)
    t = re.sub(r"^\s*[一二三四五六七八九十]+[、.．]\s*", "", t)
    for p in TAIL_NOISE:
        t = re.sub(p, "", t)
    return re.sub(r"\s+", " ", t).strip(" 　·—-_")


def grade(t: str) -> str:
    """返回 strong / weak / drop"""
    if not (6 <= len(t) <= 60):
        return "drop"
    if DROP_RE.search(t):
        return "drop"
    if PRONOUN_RE.search(t):
        return "weak"
    # 冒号标题：「损失函数：模型在最小化什么」留，「全流程六站：一张图看懂」丢
    m = re.match(r"(.{2,20}?)[：:](.{2,})$", t)
    if m:
        if len(m.group(1)) <= 2:          # 「O：优化的威力」这类断句已坏
            return "weak"
        tail = m.group(2)
        return "strong" if (Q_WORD.search(tail) or TECH_TERM.search(t)) else "weak"
    if STRONG_RE.search(t):
        return "strong"
    if TECH_TERM.search(t):
        return "strong"
    return "weak"


def to_question(t: str) -> str:
    """章节标题 → 面试官问法。只做保守改写，宁可留原样也不生成病句。"""
    if t.endswith(("？", "?")):
        return t
    if CONTRAST.search(t) and not Q_WORD.search(t):
        base = re.sub(r"[的之]?(根本|主要|核心|关键)?(差别|区别|不同)$", "", t)
        return f"{base}有什么区别？"
    return t + "？"


def extract_titles(path: Path):
    """取 h2/h3/h4。Linux 类文档的知识点在 h4（h2 只有 Chapter 编号）。"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    out, seen = [], set()
    for m in re.finditer(r"<h([234])\b[^>]*>(.*?)</h\1>", text, re.S | re.I):
        t = clean_title(m.group(2))
        if t and t not in seen:          # 文档内同标题去重（h3 常与 h2 重复）
            seen.add(t)
            out.append((int(m.group(1)), t))
    return out


# ---------------------------------------------------------------- 收集文档

def collect_sources():
    docs = []
    teach = ENG / "教学文档"
    if teach.is_dir():
        for f in sorted(teach.rglob("*.html")):
            if any(p in SKIP_DIRS for p in f.parts):
                continue
            if f.name == "index.html" or "考点实验台" in f.name:
                continue
            stem = f.stem + f.parent.name
            mod = pri = None
            for kw, m, p in KEYMAP:
                if kw in stem:
                    mod, pri = m, p
                    break
            if mod:
                docs.append({"file": f, "module": mod, "priority": pri,
                             "sub": re.sub(r"_从.*|_全套.*|讲义|教程", "", f.stem)[:14]})

    proj = ENG / "方向与规划" / "项目"
    if proj.is_dir():
        for f in sorted(proj.glob("*/*.html")):
            if "_bak" in f.name or any(p in SKIP_DIRS for p in f.parts):
                continue
            sub = "YOLO部署" if "YOLO" in f.name or "YOLO" in f.parent.name else f.parent.name
            docs.append({"file": f, "module": "01_project", "priority": "P0",
                         "sub": sub[:14]})
    return docs


def render_md(qid, title, module, sub, pri, src_rel) -> str:
    return f"""---
id: {qid}
title: {title}
module: {module}
sub: {sub}
priority: {pri}
difficulty: 2
roles: []
companies: []
qtype: principle
status: indexed
source_type: self_doc
source_ref: {src_rel}
verified_at: 2026-11-09
tags: []
auto: true
---

## 口述答案

> 待补充。200–320 字，口语，结构：结论 → 为什么 → 落到"我做过"。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

待补充。

## 来源

`{src_rel}`
"""


def existing_max(module: str) -> int:
    """该模块已有的最大编号，保证手工题卡不被覆盖。"""
    d = CONTENT / module
    if not d.is_dir():
        return 0
    nums = []
    for f in d.glob("Q-*.md"):
        m = re.match(r"Q-(\d+)", f.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) if nums else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--scan", action="store_true")
    args = ap.parse_args()

    docs = collect_sources()
    if not docs:
        print("没找到文档，检查路径:", ENG)
        return 1

    # 重跑前清掉上一轮自动生成的题卡，手工题卡（无 auto 标记）保留
    if args.write:
        removed = 0
        for f in CONTENT.rglob("Q-*.md"):
            try:
                if re.search(r"^auto: true$", f.read_text(encoding="utf-8"), re.M):
                    f.unlink()
                    removed += 1
            except OSError:
                pass
        if removed:
            print(f"清理旧自动题卡 {removed} 个")

    ctr = Counter({m: max(ID_BASE[m], existing_max(m)) for m in ID_BASE})
    strong_by_mod = defaultdict(list)
    weak_by_mod = defaultdict(list)
    stats = []
    n_drop = 0

    for d in docs:
        src_rel = d["file"].relative_to(ENG).as_posix()
        s = w = 0
        for _lvl, t in extract_titles(d["file"]):
            g = grade(t)
            if g == "drop":
                n_drop += 1
                continue
            if g == "weak":
                w += 1
                weak_by_mod[d["module"]].append((t, src_rel))
                continue
            ctr[d["module"]] += 1
            qid = f"Q-{ctr[d['module']]:04d}"
            title = to_question(t)
            s += 1
            strong_by_mod[d["module"]].append((qid, title, src_rel))
            if args.write:
                outdir = CONTENT / d["module"]
                outdir.mkdir(parents=True, exist_ok=True)
                (outdir / f"{qid}.md").write_text(
                    render_md(qid, title, d["module"], d["sub"], d["priority"], src_rel),
                    encoding="utf-8")
        stats.append({"file": src_rel, "module": d["module"], "strong": s, "weak": w})

    n_strong = sum(len(v) for v in strong_by_mod.values())
    n_weak = sum(len(v) for v in weak_by_mod.values())

    print(f"\n扫描 {len(docs)} 份文档")
    print(f"  落成题卡 strong : {n_strong}")
    print(f"  候选池   weak   : {n_weak}")
    print(f"  丢弃     drop   : {n_drop}\n")
    print(f"{'模块':<12}{'strong':>7}{'weak':>7}")
    print("-" * 26)
    for m in sorted(set(list(strong_by_mod) + list(weak_by_mod))):
        print(f"{MODULE_NAME[m]:<12}{len(strong_by_mod[m]):>7}{len(weak_by_mod[m]):>7}")
    print("-" * 26)
    print(f"{'合计':<12}{n_strong:>7}{n_weak:>7}")

    if args.scan:
        for m in sorted(strong_by_mod):
            print(f"\n### {MODULE_NAME[m]} — strong 前 10")
            for qid, title, _ in strong_by_mod[m][:10]:
                print(f"   {qid}  {title}")

    # 候选清单
    lines = ["# 候选题目池（weak 档）", "",
             "这些标题含指代词或信息不足，不能直接成题，但可能通过改写变成好题。",
             "确认后按 `docs/schema.md` 手工落成题卡。", ""]
    for m in sorted(weak_by_mod):
        lines.append(f"## {MODULE_NAME[m]}（{len(weak_by_mod[m])}）")
        lines.append("")
        lines.append("| 原标题 | 来源 |")
        lines.append("|---|---|")
        for t, src in weak_by_mod[m]:
            lines.append(f"| {t} | `{src}` |")
        lines.append("")
    (ROOT / "sources" / "candidates.md").write_text("\n".join(lines), encoding="utf-8")

    rep = ["# 抽取报告", "",
           f"- 文档数：{len(docs)}",
           f"- strong（已成题卡）：{n_strong}",
           f"- weak（进候选池）：{n_weak}",
           f"- drop（丢弃）：{n_drop}", "",
           "| 文档 | 模块 | strong | weak |", "|---|---|---|---|"]
    for s in stats:
        rep.append(f"| `{s['file']}` | {s['module']} | {s['strong']} | {s['weak']} |")
    (ROOT / "sources" / "extract_report.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
    print(f"\n→ sources/candidates.md    {n_weak} 条候选")
    print(f"→ sources/extract_report.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
