#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 content/**.md 编译成单文件题库网页 dist/bank.html。

零依赖：自己解析 frontmatter、自己渲染 Markdown，不需要 pyyaml / markdown。
产物是单个 HTML，双击即开，手机可用，可直接托管到 GitHub Pages。
"""
from __future__ import annotations

import html
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"

MODULE_NAME = {
    "01_project": "项目深挖", "02_cpp": "C++", "03_linux": "Linux",
    "04_algo": "算法机考", "05_deploy": "模型部署", "06_ros2": "ROS2",
    "07_imaging": "医学影像", "08_robot": "机器人学",
    "09_hardware": "硬件嵌入式", "10_cv_pytorch": "深度学习",
    "11_python": "Python", "12_backend": "后端基础",
    "13_hardware2": "硬件嵌入式·续",
}
MODULE_ORDER = list(MODULE_NAME)
PRI_ORDER = {"P0": 0, "P1": 1, "P2": 2}


# ------------------------------------------------------------------ 解析

def parse_fm(text: str) -> tuple[dict, str]:
    """极简 YAML frontmatter 解析，只支持本项目用到的 key: value / key: [a, b]"""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    head, body = text[3:end], text[end + 4:]
    meta: dict = {}
    for line in head.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        # 带引号的值不做行内注释剥离：标题里可能有 "#include"、"# 和 ## 的区别"
        if v[:1] in ('"', "'"):
            v = v[1:-1] if v[-1:] == v[0] else v[1:]
        else:
            # 去掉行内注释，否则 `key: []  # 说明` 会被当成字符串
            v = re.sub(r"\s+#.*$", "", v).strip()
        if v.startswith("[") and v.endswith("]"):
            items = [x.strip().strip('"\'') for x in v[1:-1].split(",")]
            meta[k] = [x for x in items if x]
        else:
            meta[k] = v.strip('"\'')
    return meta, body.strip()


# ------------------------------------------------------------------ Markdown

def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def join_lines(buf: list[str]) -> str:
    """中文换行不加空格，中英之间保留一个空格。"""
    if not buf:
        return ""
    s = buf[0]
    for x in buf[1:]:
        if not x:
            continue
        cjk_prev = bool(re.search(r"[\u4e00-\u9fff，。；：、）】]", s[-1:] if s else ""))
        cjk_next = bool(re.search(r"[\u4e00-\u9fff（【]", x[0]))
        s += x if (cjk_prev and cjk_next) else " " + x
    return s


def render_md(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        s = ln.strip()

        # 内联 SVG：原样输出，不能转义（题卡插图用手写 SVG，不用位图）
        if s.startswith("<svg"):
            buf = []
            while i < n:
                buf.append(lines[i])
                if "</svg>" in lines[i]:
                    break
                i += 1
            out.append("\n".join(buf))
            i += 1
            continue

        # 代码块
        if s.startswith("```"):
            j = i + 1
            buf = []
            while j < n and not lines[j].strip().startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            i = j + 1
            continue

        # 标题
        m = re.match(r"^(#{2,4})\s+(.*)$", s)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        # 表格
        if s.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1].strip()):
            rows = []
            j = i
            while j < n and lines[j].strip().startswith("|"):
                rows.append(lines[j].strip())
                j += 1
            head = [c.strip() for c in rows[0].strip("|").split("|")]
            body = rows[2:]
            t = ["<table><thead><tr>"]
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                cells = [c.strip() for c in r.strip("|").split("|")]
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            i = j
            continue

        # 引用块
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + inline(join_lines(buf)) + "</blockquote>")
            continue

        # 列表
        if re.match(r"^([-*]|\d+\.)\s+", s):
            ordered = bool(re.match(r"^\d+\.", s))
            tag = "ol" if ordered else "ul"
            items = []
            while i < n and re.match(r"^([-*]|\d+\.)\s+", lines[i].strip()):
                items.append(re.sub(r"^([-*]|\d+\.)\s+", "", lines[i].strip()))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue

        # 空行
        if not s:
            i += 1
            continue

        # 段落
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{2,4}\s|```|\||>|[-*]\s|\d+\.\s)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append("<p>" + inline(join_lines(buf)) + "</p>")
    return "\n".join(out)


# ------------------------------------------------------------------ 装载

def load_questions() -> list[dict]:
    qs = []
    for f in sorted(CONTENT.rglob("*.md")):
        meta, body = parse_fm(f.read_text(encoding="utf-8"))
        if not meta.get("id"):
            continue
        mod = meta.get("module") or f.parent.name
        qs.append({
            "id": meta["id"],
            "title": meta.get("title", "(无标题)"),
            "module": mod,
            "moduleName": MODULE_NAME.get(mod, mod),
            "sub": meta.get("sub", ""),
            "priority": meta.get("priority", "P1"),
            "difficulty": int(meta.get("difficulty") or 2),
            "status": meta.get("status", "indexed"),
            "qtype": meta.get("qtype", "principle"),
            "roles": meta.get("roles", []),
            "companies": meta.get("companies", []),
            "tags": meta.get("tags", []),
            "appearances": meta.get("appearances", []),
            "sourceRef": meta.get("source_ref", ""),
            "sourceType": meta.get("source_type", "inferred"),
            # 证据等级（外部评审建议的 S1~S4，由 source_type 派生）
            "evidence": {
                "official": "S1", "upstream": "S1",
                "self_doc": "S2", "self_exp": "S2",
                "nowcoder": "S3", "video": "S3",
            }.get(meta.get("source_type", "inferred"), "S4"),
            "html": render_md(body),
            # 搜索用纯文本
            "plain": re.sub(r"<[^>]+>", " ", body),
        })
    qs.sort(key=lambda q: (MODULE_ORDER.index(q["module"]) if q["module"] in MODULE_ORDER else 99,
                           PRI_ORDER.get(q["priority"], 9), q["id"]))
    return qs


# ------------------------------------------------------------------ 模板

PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CareerOS 求职功能台 · __COUNT__ 题</title>
<style>
:root{
  --bg:#faf3e2; --soft:#f3e9d2; --paper:#fffcf3; --line:#dbcba5;
  --tx:#2d2a21; --muted:#665c49; --blue:#1b5e8c; --green:#2e6b3e;
  --red:#a63a2e; --orange:#9a5a12; --purple:#6b4fa8; --yellow:#6f5520;
  --accent:#1b5e8c;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);
  font:16px/1.75 -apple-system,"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif;}
.wrap{max-width:1060px;margin:0 auto;padding:0 16px 80px}
header{padding:28px 0 12px;border-bottom:2px solid var(--line);margin-bottom:16px}
h1{margin:0 0 6px;font-size:24px;letter-spacing:.5px}
.meta{color:var(--muted);font-size:13px}
.bar{position:sticky;top:0;z-index:9;background:var(--bg);
  padding:10px 0;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px}
input[type=search],select{
  font:14px/1.6 inherit;color:var(--tx);background:var(--paper);
  border:1px solid var(--line);border-radius:8px;padding:7px 10px;outline:none}
input[type=search]{flex:1 1 240px;min-width:180px}
input[type=search]:focus,select:focus{border-color:var(--blue)}
label.chk{display:flex;align-items:center;gap:5px;font-size:13px;color:var(--muted);
  background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:7px 10px;cursor:pointer}
.q{background:var(--paper);border:1px solid var(--line);border-radius:10px;
  margin:10px 0;overflow:hidden}
.qh{display:flex;align-items:flex-start;gap:8px;padding:12px 14px;cursor:pointer;
  user-select:none;flex-wrap:wrap}
.qh:hover{background:#fdf8ea}
.pid{font:12px/1 ui-monospace,Consolas,monospace;color:var(--muted);
  background:var(--soft);padding:4px 6px;border-radius:5px;margin-top:4px}
.pri{font-size:11px;font-weight:700;padding:3px 7px;border-radius:5px;margin-top:5px;color:#fff}
.pri.P0{background:var(--red)} .pri.P1{background:var(--orange)} .pri.P2{background:#8a8378}
.qt{flex:1 1 320px;font-size:15.5px;font-weight:600;line-height:1.55;margin-top:2px}
.tag{font-size:11px;color:var(--muted);border:1px solid var(--line);
  border-radius:5px;padding:2px 6px;margin-top:5px;white-space:nowrap}
.tag.appear{color:var(--red);border-color:#d9a89f;background:#fdf1ee}
.body{display:none;padding:2px 16px 16px;border-top:1px dashed var(--line)}
.q.open .body{display:block}
.body h2{font-size:15px;color:var(--blue);margin:18px 0 6px;
  padding-left:9px;border-left:3px solid var(--blue)}
.body h3{font-size:14px;margin:14px 0 4px}
.body p{margin:6px 0}
.body ul,.body ol{margin:6px 0;padding-left:22px}
.body li{margin:3px 0}
.body blockquote{margin:8px 0;padding:8px 12px;background:var(--soft);
  border-left:3px solid var(--yellow);border-radius:0 6px 6px 0;color:#4a4334;font-size:14.5px}
.body code{background:var(--soft);border:1px solid var(--line);border-radius:4px;
  padding:1px 5px;font:13px/1.5 ui-monospace,Consolas,monospace}
.body pre{background:#f8f1de;border:1px solid var(--line);border-radius:8px;
  padding:12px;overflow:auto}
.body pre code{background:none;border:0;padding:0}
.body table{border-collapse:collapse;width:100%;margin:8px 0;font-size:14px}
.body th,.body td{border:1px solid var(--line);padding:6px 9px;text-align:left}
.body th{background:var(--soft)}
.body svg{width:100%;height:auto;display:block;margin:14px 0;
  border:1px solid var(--line);border-radius:8px;background:var(--paper)}
.todo{color:#a63a2e;font-style:italic}
.wrongmark{font-size:12px;color:var(--red);border:1px solid var(--red);
  border-radius:5px;padding:2px 7px;margin-top:4px;cursor:pointer;background:transparent}
.wrongmark.on{background:var(--red);color:#fff}
.empty{text-align:center;color:var(--muted);padding:60px 0}
#mockov{position:fixed;inset:0;background:rgba(45,42,33,.45);z-index:50;
  display:flex;align-items:center;justify-content:center}
.mpanel{width:min(720px,92vw);max-height:86vh;overflow:auto;background:var(--bg);
  border:1px solid var(--line);border-radius:12px;padding:20px 24px;
  box-shadow:0 12px 40px rgba(0,0,0,.25)}
.mhead{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.mrow{margin:10px 0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.mnote{font-size:12px;color:var(--muted);line-height:1.7;margin-top:10px}
/* —— 牛客宝典考点地图 —— */
.tutpanel{margin:12px 0 14px}
.tutpanel .rhead{flex-wrap:wrap}
.tuttabs{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:8px 0 12px}
.tuttabs .tchip{font:13px/1.6 inherit;border:1px solid var(--line);background:var(--soft);
  color:var(--tx);border-radius:999px;padding:5px 12px;cursor:pointer}
.tuttabs .tchip.on{background:linear-gradient(180deg,#fffdf7,#eaf1fb);border-color:var(--campus);
  color:var(--campus);font-weight:700;box-shadow:inset 0 -2px 0 var(--campus)}
.tlist{display:flex;flex-direction:column;gap:8px}
.tch{border:1px solid var(--line);border-left:4px solid var(--unknown-line);border-radius:10px;
  background:var(--paper);padding:9px 12px}
.tch.w3{border-left-color:var(--red)}
.tch.w2{border-left-color:var(--orange)}
.tch.w1{border-left-color:var(--unknown)}
.tch.na{background:var(--soft)}
.tch-top{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.tch-name{font-weight:700;font-size:15px}
.tch-no{font-size:11px;color:var(--muted)}
.tch-em{font-size:12px;color:var(--muted)}
.tch-w{margin-left:auto;color:var(--red);letter-spacing:1px;font-size:12px;white-space:nowrap}
.tch-mid{display:flex;align-items:center;gap:10px;margin-top:6px;flex-wrap:wrap;font-size:12px;color:var(--muted)}
.tch-mid b{color:var(--tx)}
.tch-mid .rbar2{width:90px}
.tch-act{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.tbadge{font-size:11px;border-radius:999px;padding:2px 8px;border:1px solid var(--line);
  color:var(--muted);background:var(--soft);white-space:nowrap}
.tbadge.gap{color:var(--red);border-color:#e0b4a8;background:#fdeeea}
.tbadge.zero{color:var(--orange);border-color:#e3c98a;background:var(--social-bg)}
.tbadge.mid{color:var(--blue);border-color:var(--campus-line);background:var(--campus-bg)}
.tbadge.ok{color:var(--green);border-color:var(--intern-line);background:var(--intern-bg)}
.tsec{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;padding-top:8px;border-top:1px dashed var(--line)}
.tsec .schip{font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:6px;
  padding:2px 7px;background:var(--soft)}
.tsec .schip b{color:var(--tx)}
.tsec .schip[data-tids]{cursor:pointer}
.tsec .schip[data-tids]:hover{border-color:var(--campus);color:var(--campus)}
.tsec .schip.zero{color:var(--red);border-color:#e0b4a8;background:#fdeeea}
.tutfoot{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:12px;padding-top:10px;
  border-top:1px solid var(--line)}
.tutbanner{display:flex;align-items:center;gap:8px;background:var(--campus-bg);
  border:1px solid var(--campus-line);color:var(--campus);border-radius:8px;padding:6px 10px;
  font-size:13px;margin-top:8px}
.tutbanner[hidden]{display:none}
.tutbanner button{border:0;background:transparent;color:inherit;font-size:17px;cursor:pointer;
  line-height:1;padding:0 2px}
/* —— 岗位适配度五维（V2.0） —— */
.dgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px;margin:4px 0 10px}
.dgrid .scard{cursor:pointer;transition:transform .12s,box-shadow .12s,border-color .12s}
.dgrid .scard:hover{transform:translateY(-1px);box-shadow:var(--shadow-h)}
.dgrid .scard.on{border-color:var(--campus);box-shadow:inset 0 -3px 0 var(--campus)}
.dgrid .scard small{display:block}
.dgrid .scard em{font-style:normal;font-size:11px;color:var(--muted);display:block;margin-top:2px}
.dtag.hi{background:var(--intern-bg);border-color:var(--intern-line);color:var(--green)}
.dtag.mid{background:var(--campus-bg);border-color:var(--campus-line);color:var(--campus)}
.dtag.lo{background:var(--soft);color:var(--muted)}
.jfilter{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 10px}
.jfilter .rnum{margin-left:auto}
.jdsnip{max-width:360px;font-size:12px;color:var(--muted);line-height:1.65}
.jdsnip span{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.jcard .rtable th{white-space:nowrap}
.jcard .rtable td:nth-child(5),.jcard .rtable td:nth-child(6),.jcard .rtable td:nth-child(7){white-space:nowrap}
.elc{display:inline-flex;gap:4px;font-size:11px;border:1px solid var(--line);border-radius:6px;
  padding:1px 6px;margin:2px 4px 2px 0;background:var(--soft);color:var(--muted)}
.elc b{color:var(--tx)}
.elc.ok{border-color:var(--intern-line);background:var(--intern-bg);color:var(--green)}
.elc.bad{border-color:#e0b4a8;background:#fdeeea;color:var(--red)}
.elc.warn{border-color:var(--social-line);background:var(--social-bg);color:var(--orange)}
.elc.unknown{border-style:dashed;color:var(--muted)}
.tag.warn{background:var(--social-bg);border-color:var(--social-line);color:var(--orange)}
.mqtitle{font-size:17px;font-weight:700;margin:14px 0;padding:12px 14px;
  background:var(--soft);border-left:4px solid var(--accent);border-radius:6px}
#m_follows{margin:12px 0;padding:10px 14px;background:var(--soft);border-radius:6px}
#m_follows .gl{font-size:11px;color:var(--muted)}
#m_follows li{margin:6px 0;font-size:13px;line-height:1.6}
.mhead b{font-size:15px}
.ev{font-size:10px;font-weight:700;border-radius:5px;padding:2px 5px;margin-top:5px;
  white-space:nowrap;border:1px solid transparent}
.evS1{color:#1a7f37;border-color:#1a7f37;background:#eaf5ec}
.evS2{color:#0550ae;border-color:#0550ae;background:#eaf1fb}
.evS3{color:#9a6700;border-color:#9a6700;background:#fdf6e0}
.evS4{color:#665c49;border-color:#c9bda0;background:#f3ecda}
.grade{display:flex;align-items:center;gap:6px;margin-top:14px;padding-top:10px;
  border-top:1px dashed var(--line)}
.grade .gl{font-size:11px;color:var(--muted)}
.gbtn{width:26px;height:22px;border:1px solid var(--line);background:var(--bg);
  border-radius:5px;cursor:pointer;font-size:11px;color:var(--muted)}
.gbtn:hover{border-color:var(--accent)}
.gbtn.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.gstat{font-size:11px;color:var(--muted)}
.mini{font-size:11px;padding:4px 8px;border:1px solid var(--line);background:var(--bg);
  border-radius:6px;cursor:pointer;color:var(--muted)}
.mini:hover{color:var(--accent);border-color:var(--accent)}
.selftest .body{border-left:3px solid var(--accent)}
.hint{font-size:12.5px;color:var(--muted);padding:8px 0 0}
.hint b{color:var(--blue)}
.hint .warn{color:var(--red)}
/* ---- 顶部学习数据 ---- */
.scards{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 2px}
.scard{flex:1 1 150px;background:var(--paper);border:1px solid var(--line);
  border-radius:10px;padding:10px 14px;cursor:pointer;transition:border-color .15s}
.scard:hover{border-color:var(--accent)}
.scard b{display:block;font-size:22px;line-height:1.3}
.scard small{font-size:12px;color:var(--muted)}
.scard.warn b{color:var(--red)}
.scard.good b{color:var(--green)}
/* ---- 快捷筛选 chips ---- */
.brow{display:flex;gap:8px;flex-wrap:wrap;flex:1 1 100%}
.chips{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.chip{font-size:13px;color:var(--muted);background:var(--paper);
  border:1px solid var(--line);border-radius:999px;padding:5px 14px;cursor:pointer}
.chip:hover{border-color:var(--accent);color:var(--accent)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
.chips .csep{width:1px;height:18px;background:var(--line);margin:0 2px}
/* ---- 详细筛选折叠与条件 pills ---- */
.moref{flex:1 1 100%}
.moref summary{display:inline-flex;align-items:center;gap:6px;font-size:13px;
  color:var(--muted);cursor:pointer;list-style:none;padding:4px 2px;user-select:none}
.moref summary::-webkit-details-marker{display:none}
.moref summary::before{content:'▸';transition:transform .15s}
.moref[open] summary::before{transform:rotate(90deg)}
.moref[open] summary{color:var(--accent)}
.moref summary .fc{font-size:11px;background:var(--accent);color:#fff;
  border-radius:999px;padding:1px 7px;font-weight:700}
.fgrid{display:flex;gap:8px;flex-wrap:wrap;padding:8px 0 4px}
.fpills{display:flex;gap:6px;flex-wrap:wrap}
.fpill{font-size:12px;color:var(--blue);background:#eaf1fb;border:1px solid #b9cfe8;
  border-radius:999px;padding:3px 10px;display:inline-flex;align-items:center;gap:5px}
.fpill b{font-weight:600}
.fpill i{font-style:normal;cursor:pointer;color:#5f7ea6;font-size:14px;line-height:1}
.fpill i:hover{color:var(--red)}
/* ---- 题卡掌握状态 / 收起态追问提示 ---- */
.qdot{display:inline-flex;align-items:center;gap:5px;font-size:11px;color:var(--muted);
  margin-top:6px;white-space:nowrap}
.qdot i{width:8px;height:8px;border-radius:50%;background:#c9bda0;display:inline-block}
.qdot.weak i{background:var(--red)} .qdot.due i{background:#c9930a}
.qdot.ok i{background:var(--green)}
.qf{font-size:12px;color:var(--muted);padding:0 14px 10px;display:flex;gap:6px;align-items:center}
.qf .fi{background:var(--soft);border-radius:5px;padding:2px 8px}
.qmeta{font-size:12px;color:var(--muted);margin-top:16px;padding-top:8px;
  border-top:1px dashed var(--line);display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.qmeta a{color:var(--blue);text-decoration:none}
.qmeta a:hover{text-decoration:underline}
/* ---- 模拟面试作答框 ---- */
#m_note{width:100%;min-height:88px;font:14px/1.7 inherit;color:var(--tx);
  background:var(--paper);border:1px solid var(--line);border-radius:8px;
  padding:10px 12px;outline:none;resize:vertical}
#m_note:focus{border-color:var(--accent)}
/* ---- 快捷键提示与焦点高亮 ---- */
.keys{font-size:12px;color:var(--muted);text-align:center;padding:26px 0 6px}
.keys kbd{background:var(--soft);border:1px solid var(--line);border-bottom-width:2px;
  border-radius:5px;padding:1px 6px;font:11px ui-monospace,Consolas,monospace}
.q.foc{border-color:var(--accent);box-shadow:0 0 0 2px #1b5e8c26}
/* ---- 四视图导航 ---- */
.tabs{display:flex;gap:6px;margin-top:16px;flex-wrap:wrap}
.tab{font-size:14px;padding:8px 20px;border:1px solid var(--line);background:var(--paper);
  border-radius:9px;cursor:pointer;color:var(--muted)}
.tab:hover{border-color:var(--accent);color:var(--accent)}
.tab.on{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600}
.view{display:none}
.view.on{display:block}
/* ---- 首页 / 训练视图面板 ---- */
.hdate{font-size:13px;color:var(--muted);margin:14px 0 8px}
.quick{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 14px}
.qcard{flex:1 1 200px;background:var(--paper);border:1px solid var(--line);border-radius:10px;
  padding:14px 16px;cursor:pointer;transition:border-color .15s}
.qcard:hover{border-color:var(--accent)}
.qcard b{display:block;font-size:15px;margin-bottom:3px}
.qcard small{font-size:12px;color:var(--muted);line-height:1.5;display:block}
.hgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0}
@media(max-width:900px){.hgrid{grid-template-columns:1fr}}
.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.panel h3{margin:0 0 8px;font-size:14px;color:var(--muted)}
.titem{display:flex;align-items:center;gap:10px;padding:10px 2px;
  border-bottom:1px dashed var(--line);cursor:pointer}
.titem:last-child{border-bottom:0}
.titem:hover b{color:var(--accent)}
.titem b{font-size:14px;flex:0 0 88px}
.tnote{font-size:12px;color:var(--muted);flex:1}
.tstat{font-size:11px;padding:2px 9px;border-radius:5px;white-space:nowrap}
.tstat.done{color:#1a7f37;background:#eaf5ec}
.tstat.doing{color:#9a5a12;background:#fdf3e4}
.tstat.todo{color:var(--muted);background:var(--soft)}
.prow{padding:9px 2px;border-bottom:1px dashed var(--line);cursor:pointer}
.prow:last-child{border-bottom:0}
.prow:hover b{color:var(--accent)}
.prow>b{display:block;font-size:14px;margin-bottom:4px}
.pbarw{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:8px;margin:3px 0}
.pbar{display:inline-block;width:120px;height:9px;background:var(--soft);
  border-radius:5px;overflow:hidden;vertical-align:middle}
.pbar i{display:block;height:100%;background:var(--accent)}
.pbar.mas i{background:var(--green)}
.hitem{display:flex;align-items:center;gap:9px;padding:8px 2px;
  border-bottom:1px dashed var(--line);font-size:13px}
.hitem:last-child{border-bottom:0}
.hitem .pid{margin-top:0}
.hitem b{flex:1;font-weight:400;color:var(--tx);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rscore.m4{color:#1a7f37;background:#eaf5ec}
.rscore.m3{color:#0550ae;background:#eaf1fb}
.rscore.m12{color:#a63a2e;background:#fdf1ee}
.hempty{font-size:12.5px;color:var(--muted);line-height:1.8}
.trgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.trcard{background:var(--paper);border:1px solid var(--line);border-radius:10px;
  padding:13px 15px;cursor:pointer}
.trcard:hover{border-color:var(--accent)}
.trcard b{display:block;font-size:14.5px;margin-bottom:3px}
.trcard small{font-size:12px;color:var(--muted)}
.trcard .pbar{width:100%;margin-top:8px}
/* 分析视图：rpanel 由浮层改为平铺容器 */
#view-rep .rpanel{width:auto;max-height:none;background:transparent;
  border:0;padding:0;box-shadow:none;overflow:visible}
/* ---- 岗位视图 ---- */
.jrow{display:flex;gap:8px;flex-wrap:wrap}
.jrow input,.jrow select{flex:1 1 140px;font:14px/1.6 inherit;color:var(--tx);
  background:var(--paper);border:1px solid var(--line);border-radius:8px;
  padding:7px 10px;outline:none}
.jrow input:focus{border-color:var(--blue)}
.jcard{margin:0}
#joblist{display:flex;flex-direction:column;gap:10px}
.jcard .qh{padding:13px 14px}
.jcard .rscore{font-size:14px;margin-top:3px}
.jbody{padding:4px 16px 14px;border-top:1px dashed var(--line)}
.jlink{color:var(--blue)!important;text-decoration:none;cursor:pointer}
.jlink:hover{border-color:var(--blue)}
.rgrid2{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.rcard2{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:11px 13px}
.rcard2 .rh{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.rcard2 .rt{font-size:14.5px;font-weight:600;margin:2px 0;line-height:1.5}
.rcard2 small{display:block;color:var(--muted);font-size:11.5px;margin-bottom:6px;line-height:1.6}
/* ---- V1.8 公司 & 岗位总览（全部公司 / 校招·实习分类） ---- */
.cstat{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 14px}
.cstat .scard{flex:1 1 140px}
.cbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px}
.cbar input[type=search]{flex:1 1 280px}
.chip.rst{color:var(--red);border-color:#d9a89f}
.chip.rst.act{background:var(--red);color:#fff;border-color:var(--red)}
#comp_more summary{cursor:pointer;user-select:none;color:var(--muted);font-size:13px;padding:4px 0}
#comp_more[open] summary{color:var(--accent)}
.ncfilter{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0 10px}
.ncfilter .chips{flex:1 1 100%}
.ncfilter select{font:13px/1.6 inherit;color:var(--tx);background:var(--paper);
  border:1px solid var(--line);border-radius:8px;padding:5px 8px}
.ncfilter select.ncsel{max-width:132px}
.nccard{background:var(--paper);border:1px solid var(--line);border-radius:8px;margin:6px 0;padding:8px 12px}
.nccard summary{cursor:pointer;display:flex;gap:8px;align-items:center;flex-wrap:wrap;list-style:none}
.nccard summary::-webkit-details-marker{display:none}
.nccard .nct{flex:1 1 100%;font-size:13.5px;font-weight:600;margin-top:3px}
.nccard[open] summary .nct{color:var(--accent)}
.ncb{padding:6px 0 2px 8px;border-top:1px dashed var(--line);margin-top:6px}
.nclist{margin:6px 0;padding-left:20px}
.nch{display:flex;gap:8px;align-items:flex-start;margin:4px 0;font-size:13px;line-height:1.6}
.nchq{flex:1}
.qref{font:11px ui-monospace,Consolas,monospace;color:#fff;background:var(--blue);
  border-radius:4px;padding:1px 6px;white-space:nowrap;text-decoration:none;margin-top:2px}
.qref:hover{background:#14486b}
.qref.near{background:#9a6700}
.qref.none{background:var(--soft);color:var(--muted)}
.ctable tbody tr{vertical-align:top}
.ncq{max-width:380px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cfilter .flab{font-size:12px;color:var(--muted);white-space:nowrap}
.cnote{font-size:12px;color:var(--muted);line-height:1.8;margin:6px 0 10px}
.ctable{font-size:12.5px}
.ctable th,.ctable td{padding:7px 9px;vertical-align:top}
.ctable th:last-child,.ctable td:last-child{min-width:118px}
.ctable tbody tr[data-coname]{cursor:pointer}
.ctable td small{display:block;color:var(--muted);font-size:11.5px;line-height:1.5}
.ctable tbody tr{cursor:default}
.ctable .jt{font-weight:600;font-size:13px;line-height:1.5}
.cbadge{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;
  border-radius:999px;white-space:nowrap}
.cbadge.campus{color:#1b5e8c;background:#eaf1fb;border:1px solid #b9cfe8}
.cbadge.intern{color:#2e6b3e;background:#eaf5ec;border:1px solid #b6d8bd}
.cbadge.social{color:#9a5a12;background:#fdf6e0;border:1px solid #e3c98a}
.cbadge.unknown{color:var(--muted);background:var(--soft);border:1px solid var(--line)}
.conf{font-size:10.5px;white-space:nowrap}
.conf.high{color:var(--green)} .conf.medium{color:var(--orange)}
.conf.low{color:var(--muted)} .conf.none{color:var(--red)}
.cjobrow.hs-saved,.cjobrow.hs-dismissed{opacity:.68}
.cjobrow.hs-dismissed .jt{text-decoration:line-through;text-decoration-color:#c9bda0}
.cempty{font-size:12.5px;color:var(--muted);padding:10px 2px}
/* ---- 学习分析（平铺视图） ---- */
.rpanel{width:min(900px,94vw);max-height:88vh;overflow:auto;background:var(--bg);
  border:1px solid var(--line);border-radius:12px;padding:22px 26px;
  box-shadow:0 12px 40px rgba(0,0,0,.25)}
.rhead{display:flex;align-items:center;gap:12px;margin-bottom:6px}
.rhead b{font-size:17px}
.rsec{font-size:13px;font-weight:700;color:var(--muted);margin:18px 0 6px;
  letter-spacing:.5px}
.rcards{display:flex;gap:10px;flex-wrap:wrap}
.rcard{flex:1 1 160px;background:var(--paper);border:1px solid var(--line);
  border-radius:10px;padding:12px 14px;cursor:pointer;transition:border-color .15s}
.rcard:hover{border-color:var(--accent)}
.rcard b{display:block;font-size:26px;line-height:1.25}
.rcard small{font-size:12px;color:var(--muted)}
.rcard.warn b{color:var(--red)}
.rcard.good b{color:var(--green)}
.rchart{display:flex;align-items:flex-end;gap:7px;height:96px;
  padding:8px 4px 0;background:var(--paper);border:1px solid var(--line);border-radius:10px}
.rbar{flex:1;display:flex;flex-direction:column;justify-content:flex-end;gap:3px;
  text-align:center;min-width:0}
.rbar i{display:block;background:var(--accent);border-radius:3px 3px 0 0;min-height:2px}
.rbar.zero i{background:var(--line)}
.rbar em{font-style:normal;font-size:11px;color:var(--muted)}
.rbar u{text-decoration:none;font-size:12px;color:var(--tx);font-weight:600}
.rtable{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--paper);
  border:1px solid var(--line);border-radius:10px;overflow:hidden}
.rtable th,.rtable td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left}
.rtable th{background:var(--soft);font-size:12px;color:var(--muted)}
.rtable tr:last-child td{border-bottom:0}
.rtable tbody tr{cursor:pointer}
.rtable tbody tr:hover{background:#fdf8ea}
.rbar2{position:relative;background:var(--soft);border-radius:4px;height:12px;
  width:110px;display:inline-block;vertical-align:middle;overflow:hidden}
.rbar2 i{position:absolute;inset:0;right:auto;background:var(--green);border-radius:4px}
.rnum{font:12px ui-monospace,Consolas,monospace;color:var(--muted)}
.rscore{font-weight:700;padding:1px 8px;border-radius:5px;font-size:12.5px}
.rscore.hi{color:#1a7f37;background:#eaf5ec}
.rscore.mid{color:#9a6700;background:#fdf6e0}
.rscore.lo{color:#a63a2e;background:#fdf1ee}
.radv{margin:8px 0 0;padding-left:22px;font-size:14px;line-height:1.9}
.radv li{margin:2px 0}
.rfoot{display:flex;gap:8px;margin-top:18px;flex-wrap:wrap}
@media(max-width:640px){
  h1{font-size:20px}.qt{flex:1 1 100%}.wrap{padding:0 12px 60px}
  .bar{gap:6px}input[type=search]{flex:1 1 100%}
  /* 考点地图：窄屏去掉进度条，操作按钮整行换行，避免挤成一条 */
  .tutpanel{padding:12px 12px 10px}
  .tch-mid .rbar2{display:none}
  .tch-act{margin-left:0;flex:1 1 100%;margin-top:5px}
  .tch-w{font-size:11px}
  .tuttabs .tchip{font-size:12px;padding:4px 10px}
}
/* ---- V1.9 视觉层次：类别色 / 卡片质感 / 过渡 ---- */
:root{
  --campus:#1b5e8c; --campus-bg:#eaf1fb; --campus-line:#b9cfe8;
  --intern:#2e6b3e; --intern-bg:#eaf5ec; --intern-line:#b6d8bd;
  --social:#9a5a12; --social-bg:#fdf6e0; --social-line:#e3c98a;
  --unknown:#6b6250; --unknown-bg:#f2ece0; --unknown-line:#d8cdb4;
  --shadow:0 1px 2px rgba(90,70,30,.05);
  --shadow-h:0 8px 22px rgba(90,70,30,.10);
}
.panel{box-shadow:var(--shadow)}
.panel h3{padding-left:9px;border-left:3px solid var(--accent)}
#ncbox>summary{padding-left:9px;border-left:3px solid var(--campus)}
#ncbox b{color:var(--campus)}
.scard{position:relative;overflow:hidden;box-shadow:var(--shadow);transition:transform .15s,box-shadow .15s}
.scard::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent)}
.scard:hover{transform:translateY(-2px);box-shadow:var(--shadow-h)}
.scard.sc-pool::before{background:var(--unknown)}
.scard.sc-job::before{background:var(--campus)}
.scard.sc-campus::before{background:var(--campus)}
.scard.sc-intern::before{background:var(--intern)}
.scard.sc-intern b{color:var(--intern)}
.scard.sc-campus b{color:var(--campus)}
.scard.sc-low::before{background:var(--social)}
.scard.sc-low b{color:var(--social)}
.scard.sc-nc::before{background:var(--purple)}
.scard.sc-nc b{color:var(--purple)}
.rtable th{background:linear-gradient(180deg,#f6eeda,#f1e6cd);letter-spacing:.3px}
.rtable tbody tr{transition:background .12s}
.rtable tbody tr:hover{background:#fbf4e2}
.cbadge.campus{color:#fff;background:var(--campus);border-color:var(--campus)}
.cbadge.intern{color:#fff;background:var(--intern);border-color:var(--intern)}
.cbadge.social{color:#fff;background:var(--social);border-color:var(--social)}
.cbadge.unknown{color:var(--unknown);background:var(--unknown-bg);border-color:var(--unknown-line)}
.jt{transition:color .12s}
.rtable tbody tr:hover .jt{color:var(--accent)}
.chip{transition:all .15s}
.chip:hover{transform:translateY(-1px);box-shadow:var(--shadow)}
.chip.on{background:linear-gradient(135deg,#1b5e8c,#2a7ab3);box-shadow:0 2px 8px rgba(27,94,140,.28)}
.chip.rst.act{background:linear-gradient(135deg,#a63a2e,#c0503f);box-shadow:0 2px 8px rgba(166,58,46,.28)}
.nccard{transition:box-shadow .15s,transform .15s;border-left:3px solid transparent}
.nccard:hover{box-shadow:var(--shadow-h);transform:translateY(-1px)}
.nccard[open]{border-left-color:var(--campus);background:#fffef8}
.nccard summary b{color:var(--campus)}
.qref{transition:background .12s,transform .12s}
.qref:hover{transform:translateY(-1px);background:#123f5e}
.qcard{box-shadow:var(--shadow);transition:transform .15s,box-shadow .15s,border-color .15s}
.qcard:hover{transform:translateY(-2px);box-shadow:var(--shadow-h)}
.prow:hover{background:#fbf4e2;border-radius:6px}
.tabs .tab{transition:all .15s}
.tab.on{background:linear-gradient(135deg,#1b5e8c,#2a7ab3);box-shadow:0 3px 10px rgba(27,94,140,.22)}
#h_nc{border-left:3px solid var(--purple)}
#h_nc .hitem b{font-weight:600}
#h_nc .hitem:hover{background:#fbf4e2;border-radius:6px}
.hitem a.tag{margin-top:0}
.ncfilter select.ncsel{color:var(--campus);border-color:var(--campus-line);background:var(--campus-bg)}
a.chip{text-decoration:none;display:inline-flex;align-items:center;gap:4px}
a.chip:hover{border-color:var(--accent);color:var(--accent)}
/* ── 题库导航：按考点刷题 / 企业题库 ── */
.navwrap{background:var(--paper);border:1px solid var(--line);border-radius:12px;
  padding:12px 14px;margin:8px 0 12px}
.navtabs{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.ntab{font:13px/1.6 inherit;border:1px solid var(--line);background:var(--soft);color:var(--tx);
  border-radius:999px;padding:5px 14px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.ntab:hover{border-color:var(--accent)}
.ntab.on{background:var(--accent);color:#fffcf3;border-color:var(--accent)}
.ntn{font-size:11px;opacity:.75}
.navpane{margin-top:10px}
.navwrap.compact .navpane{display:none}
.hint2{font-size:12px;color:var(--muted);margin:0 0 8px;line-height:1.6}
.topicgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(156px,1fr));gap:8px;
  padding:2px 0}
.tcard{display:flex;flex-direction:column;gap:3px;text-align:left;background:var(--soft);
  border:1px solid var(--line);border-radius:9px;padding:9px 11px;cursor:pointer;transition:.12s}
.tcard:hover{border-color:var(--accent);background:#fffdf6;transform:translateY(-1px)}
.tcard.on{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent);background:#fffdf6}
.tcard .tn{font-size:13px;font-weight:600;color:#26231b;line-height:1.35}
.tcard .tm{font-size:11px;color:var(--muted)}
.tcard .tc{font-size:11.5px;color:var(--accent);font-variant-numeric:tabular-nums}
.corgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(236px,1fr));gap:8px;
  padding:2px 0}
.ccard{display:flex;flex-direction:column;gap:5px;text-align:left;background:var(--soft);
  border:1px solid var(--line);border-radius:9px;padding:10px 12px;cursor:pointer;transition:.12s}
.ccard:hover{border-color:var(--accent);background:#fffdf6;transform:translateY(-1px)}
.ccard.on{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent);background:#fffdf6}
.ccard .cn{font-size:13.5px;font-weight:600;color:#26231b}
.ccard .cm{font-size:11.5px;color:var(--muted)}
.ccard .cm b{color:var(--accent);font-weight:600}
.dbar2{display:flex;height:6px;border-radius:3px;overflow:hidden;background:var(--soft)}
.dbar2 i{display:block;height:100%}
.dbar2 .d1{background:#2e6b3e}.dbar2 .d2{background:#b58a2b}.dbar2 .d3{background:#a63a2e}
.ccard .cd{font-size:11px;color:var(--muted);font-variant-numeric:tabular-nums}
.navfoot{display:flex;align-items:center;gap:10px;margin-top:10px;flex-wrap:wrap;
  border-top:1px dashed var(--line);padding-top:10px}
.navfoot .hint2{margin:0}
.navfoot .clr{font-size:12px;color:var(--accent);cursor:pointer;text-decoration:underline}
.modrow{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.mchip{font:12.5px/1.6 inherit;border:1px solid var(--line);background:var(--paper);
  color:var(--tx);border-radius:999px;padding:4px 11px;cursor:pointer;white-space:nowrap}
.mchip:hover{border-color:var(--accent)}
.mchip.on{background:var(--accent);border-color:var(--accent);color:#fffcf3}
.mchip b{font-weight:600}
.modrow .mchip:first-child{margin-right:2px}
.navmore{margin-top:8px}
.navmore button{font:12.5px/1.6 inherit;border:1px dashed var(--line);background:transparent;
  color:var(--accent);border-radius:8px;padding:5px 12px;cursor:pointer}
.navmore button:hover{border-color:var(--accent);background:#fffdf6}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>CareerOS · 求职功能台</h1>
  <div class="meta" id="stat"></div>
  <nav class="tabs">
    <button class="tab" data-v="home">🏠 首页</button>
    <button class="tab" data-v="bank">📚 题库</button>
    <button class="tab" data-v="train">🎯 训练</button>
    <button class="tab" data-v="jobs">💼 岗位</button>
    <button class="tab" data-v="comp">🏢 公司</button>
    <button class="tab" data-v="rep">📈 分析</button>
  </nav>
</header>

<section id="view-home" class="view">
  <div class="hdate" id="h_date"></div>
  <div class="scards" id="scards"></div>
  <div class="hempty" id="h_radar" style="margin:8px 2px"></div>
  <div class="panel" id="h_nc" style="margin:10px 0"></div>
  <div class="quick" id="h_quick"></div>
  <div class="hgrid">
    <div class="panel"><h3>今日训练任务</h3><div id="h_tasks"></div></div>
    <div class="panel"><h3>岗位训练进度（按真实校招 JD 模板）</h3><div id="h_profs"></div></div>
  </div>
  <div class="panel"><h3>最近训练记录</h3><div id="h_hist"></div></div>
</section>

<section id="view-bank" class="view">
<div class="bar">
  <div class="brow">
    <input type="search" id="q" placeholder="搜题目 / 正文 / 公司 / 岗位，如 Momenta、推理部署">
    <button id="mock" class="mini" title="按当前筛选/岗位模板抽题，逐题作答，高频追问揭示">🎤 模拟面试</button>
    <button id="rep" class="mini" title="自测覆盖、掌握度、复习节奏、错题本健康度">📊 学习报告</button>
    <button id="rep_tut" class="mini" title="按牛客面试宝典的章节目录刷题（分析视图顶部）">📚 考点地图</button>
  </div>
  <div class="tutbanner" id="tutbanner" hidden></div>
  <div class="chips" id="chips">
    <button class="chip on" data-c="all" title="清除快捷筛选（详细筛选保留）">全部</button>
    <button class="chip" data-c="p0">P0 必答</button>
    <button class="chip" data-c="due" title="间隔复习到期，该过一遍了">今日复习</button>
    <button class="chip" data-c="weak" title="自评≤2 的薄弱题">薄弱</button>
    <button class="chip" data-c="wrong">错题</button>
    <button class="chip" data-c="real" title="只看真实面经与一手题，隐藏 S4 预测题">真实面经</button>
  </div>
  <details class="moref" id="moref">
    <summary>更多筛选 <span class="fc" id="fcount" style="display:none">0</span></summary>
    <div class="fgrid">
      <select id="co"><option value="">全部公司</option>__COOPTS__</select>
      <select id="prof" title="岗位模板：按真实 JD 归纳的模块权重过滤题目，并可作为模拟面试题源"><option value="">岗位模板…</option>__PROFOPTS__</select>
      <select id="mod"><option value="">全部模块</option>__MODOPTS__</select>
      <select id="sub"><option value="">全部子方向</option></select>
      <select id="dif" title="难度"><option value="">全部难度</option>
        <option value="1">★ 简单</option><option value="2">★★ 中等</option><option value="3">★★★ 困难</option></select>
      <label class="chk" title="搜索不再自动展开答案，先自己答"><input type="checkbox" id="selftest_v"> 自测模式</label>
      <button id="exp" class="mini" title="导出错题与自评记录（JSON）">备份↓</button>
      <button id="impb" class="mini" title="从 JSON 恢复复习数据">恢复↑</button>
      <input type="file" id="imp" accept=".json" hidden>
      <!-- 已合并/隐藏的旧筛选（保留元素与选项避免逻辑回归）：岗位族 rl 与岗位模板 prof 重复；优先级 pri 与 P0 chip 重复；状态 st 全库已答；复习状态 rev 与上方 chips 重复 -->
      <span hidden>
        <select id="rl"><option value="">全部岗位</option>__RLOPTS__</select>
        <select id="pri"><option value="">全部优先级</option>
          <option value="P0">P0 必答</option><option value="P1">P1 进阶</option><option value="P2">P2 长期</option></select>
        <select id="st"><option value="">全部状态</option>
          <option value="answered">已答</option><option value="draft">草稿</option>
          <option value="indexed">待补充</option></select>
        <select id="rev"><option value="">全部复习状态</option>
          <option value="due">今日该复习</option><option value="weak">薄弱（自评≤2）</option>
          <option value="never">从未自测</option></select>
      </span>
    </div>
  </details>
  <div class="fpills" id="fpills"></div>
  <label hidden><input type="checkbox" id="wrong"></label>
  <label hidden><input type="checkbox" id="hidepred"></label>
  <label hidden><input type="checkbox" id="selftest"></label>
</div>
<div class="navwrap" id="banknav">
  <div class="navtabs">
    <button class="ntab on" data-nt="topic">📚 按考点刷题<span class="ntn" id="nt_topic"></span></button>
    <button class="ntab" data-nt="corp">🏢 企业题库<span class="ntn" id="nt_corp"></span></button>
    <button class="ntab" data-nt="list">📋 直接看列表</button>
  </div>
  <div class="navpane" id="nav_topic">
    <div class="modrow" id="modrow"></div>
    <div class="hint2">点考点直接筛题；数字是题量，后面是难度分布。</div>
    <div class="topicgrid" id="topicgrid"></div>
    <div class="navmore" id="more_topic"></div>
  </div>
  <div class="navpane" id="nav_corp" hidden>
    <div class="hint2">按公司聚合成题库；点卡片只看这家公司真实问过的题。</div>
    <div class="corgrid" id="corpgrid"></div>
    <div class="navmore" id="more_corp"></div>
  </div>
  <div class="navfoot">
    <button id="drill10" class="mini">▶ 开始 10 题练习</button>
    <span class="hint2" id="drillhint"></span>
  </div>
</div>
<div class="hint" id="hint"></div>

<div id="list"></div>
<div class="empty" id="empty" style="display:none">没有匹配的题目</div>
<div class="keys">快捷键：<kbd>/</kbd> 搜索 · <kbd>J</kbd>/<kbd>K</kbd> 上下题 · <kbd>空格</kbd> 展开收起 · <kbd>1</kbd>–<kbd>4</kbd> 自评 · <kbd>W</kbd> 标错 · <kbd>Esc</kbd> 关闭弹层</div>
</section>

<section id="view-train" class="view">
  <div class="hgrid">
    <div class="panel">
      <h3>🎤 模拟面试</h3>
      <div class="hempty">按当前筛选或岗位模板加权抽题，逐题作答 → 揭示高频追问 → 自评计入复习计划，结束生成掌握总结。可选不限时练习模式。</div>
      <div class="mrow"><button id="tr_mock" style="padding:8px 22px">配置并开始</button></div>
    </div>
    <div class="panel">
      <h3>🩹 复习中心</h3>
      <div class="hempty">间隔复习按自评分安排：1~2 分次日/三日重来，3 分一周，4 分三周。自评不会的题自动进错题本。</div>
      <div class="mrow">
        <button class="mini" id="tr_due">📋 今日该复习</button>
        <button class="mini" id="tr_weak">🩹 薄弱题清单</button>
        <button class="mini" id="tr_wrong">❌ 错题本</button>
      </div>
    </div>
  </div>
  <div class="panel">
    <h3>📚 项目连环问（顺序过题 · 不限时 · 面试官就是这个问法）</h3>
    <div class="trgrid" id="tr_projects"></div>
  </div>
</section>

<section id="view-jobs" class="view">
  <div class="panel" style="margin-bottom:14px">
    <h3>💼 岗位收藏 · 点卡片看「JD → 题库」技能匹配分析
      <button class="mini" data-goall="1" style="margin-left:8px">🏢 查看全部公司 / 全部岗位 →</button></h3>
    <details id="jobform">
      <summary>➕ 添加岗位（人工登记，存本机浏览器，随备份导出）</summary>
      <div style="display:flex;flex-direction:column;gap:8px;padding:8px 0">
        <div class="jrow">
          <input id="j_co" placeholder="公司 *">
          <input id="j_ti" placeholder="岗位名称 *">
          <input id="j_city" placeholder="城市">
          <select id="j_ty"><option>校招</option><option>实习</option><option>社招</option></select>
          <input id="j_url" placeholder="JD 链接（官网/招聘页）">
        </div>
        <textarea id="j_jd" placeholder="粘贴 JD 原文，用于技能匹配分析（命中 C++/Linux/部署/ROS2/感知等技能表，对照你的题库自评数据给出缺口判断）" style="min-height:110px;font:14px/1.7 inherit;color:var(--tx);background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:10px 12px;outline:none;resize:vertical"></textarea>
        <div class="mrow"><button id="j_save" style="padding:7px 18px">保存岗位</button>
          <span class="rnum">自动采集后续接入（官方招聘页低频增量监控），先人工登记最高优先级的</span></div>
      </div>
    </details>
  </div>
  <details id="radarbox" class="panel" style="margin-bottom:14px">
    <summary>🛰 岗位雷达 <span class="rnum" id="radar_meta"></span> — 自动监控官方招聘门户（每日低频增量），收藏后进入下方列表</summary>
    <div class="rgrid2" id="radarlist" style="margin-top:10px"></div>
  </details>
  <div class="panel" id="decidebox" style="margin-bottom:14px">
    <div class="rhead"><b>🎯 投递决策</b><span class="rnum" id="decide_meta"></span></div>
    <div class="mnote">资格先出局 → 再看相关度 → 最后看证据，不做「匹配度 75%」这种加权。
      四类卡片只统计<b>已收藏岗位</b>（想去投的才值得决策）；点卡片筛下方列表。下面是五大岗位族的市场供给与我的准备对比。</div>
    <div class="dgrid" id="decide_cards"></div>
    <div id="decide_fams"></div>
  </div>
  <div class="jfilter" id="jobfilter">
    <span class="flab">范围</span>
    <button class="chip on" data-jf="scope" data-v="tech">只看技术岗</button>
    <button class="chip" data-jf="scope" data-v="all">含非技术岗</button>
    <span class="csep"></span>
    <span class="flab">适配</span>
    <button class="chip on" data-jf="rel" data-v="all">全部</button>
    <button class="chip" data-jf="rel" data-v="high">高相关</button>
    <button class="chip" data-jf="rel" data-v="gap">有缺口 / 资格不符</button>
    <span class="rnum" id="job_meta"></span>
  </div>
  <div class="trgrid" id="joblist"></div>
</section>

<section id="view-comp" class="view">
  <div class="panel">
    <h3>🏢 全部公司 & 全部岗位 · 招聘性质分类（校招 / 实习 / 社招 / 未标明）</h3>
    <div class="cnote" id="comp_note"></div>
    <details class="panel" id="ncbox" open style="margin:12px 0 14px">
      <summary style="cursor:pointer;font-weight:700">📰 真实面经（牛客，每周自动同步）<span class="rnum" id="nc_meta"></span></summary>
      <div class="cnote">面经帖来自牛客公开版块，只保留「公司 × 岗位 × 轮次 × 题目原文摘录 × 原帖链接」，不含发帖人信息。
        题目右侧 <b>Q-xxxx</b> 是题库里的同考点题号，点它直接跳到题库复习；「近似」是同考点不同措辞，「未入库」可点原帖看正文。</div>
      <div class="ncfilter">
        <div class="chips" id="nc_chips">
          <span class="flab">公司</span>
          <span id="nc_co_chips" style="display:contents"></span>
          <select id="nc_co_all" title="全部面经公司（含未显示的）"><option value="all">更多公司…</option></select>
        </div>
        <select id="nc_round"><option value="all">全部轮次</option></select>
        <select id="nc_role"><option value="all">全部方向</option></select>
        <label class="chk"><input type="checkbox" id="nc_onlyref"> 只看有题号</label>
      </div>
      <div id="nc_exp"></div>
      <div class="rsec">📄 公司真题卷（牛客企业真题，仅登记元数据；题干有平台版权限制，点链接去牛客在线作答）</div>
      <div id="nc_papers"></div>
      <div class="rsec">🎯 牛客专项题库（选择题，站内练习；题干与答案需登录且有版权限制，这里只做导航）</div>
      <div class="chips" id="nc_topics" style="gap:6px"></div>
    </details>
    <div class="cstat" id="comp_stat"></div>
    <div class="cbar">
      <input type="search" id="comp_q" placeholder="搜公司 / 岗位 / 城市 / 批次 / 岗位族（同时过滤面经与真题卷）">
      <button class="chip rst" id="comp_reset" title="清空全部筛选条件">↩ 重置</button>
    </div>
    <div class="chips" id="comp_chips_main">
      <span class="flab">性质</span>
      <button class="chip on" data-k="cls" data-v="all">全部</button>
      <button class="chip" data-k="cls" data-v="校招">校招 <b>0</b></button>
      <button class="chip" data-k="cls" data-v="实习">实习 <b>0</b></button>
      <button class="chip" data-k="cls" data-v="社招">社招 <b>0</b></button>
      <button class="chip" data-k="cls" data-v="未标明">未标明 <b>0</b></button>
      <span class="csep"></span>
      <span class="flab">公司</span>
      <button class="chip on" data-k="src" data-v="all">全部公司</button>
      <button class="chip" data-k="src" data-v="pool">雷达池</button>
      <button class="chip" data-k="src" data-v="enabled">已接入</button>
      <button class="chip" data-k="src" data-v="unset">未接入</button>
      <button class="chip" data-k="src" data-v="targets">仅目标池</button>
    </div>
    <details class="moref" id="comp_more">
      <summary>⚙ 更多筛选（岗位状态 / 城市）<span class="fc" id="comp_more_n" hidden>0</span></summary>
      <div class="chips" id="comp_chips_more" style="padding:8px 0 2px">
        <span class="flab">岗位状态</span>
        <button class="chip on" data-k="st" data-v="all">全部</button>
        <button class="chip" data-k="st" data-v="open">在招</button>
        <button class="chip" data-k="st" data-v="suspect">疑似下线</button>
        <button class="chip" data-k="st" data-v="todo">待处理</button>
        <button class="chip" data-k="st" data-v="saved">已收藏</button>
        <button class="chip" data-k="st" data-v="dismissed">已忽略</button>
        <span class="csep"></span>
        <span class="flab">城市</span>
        <button class="chip on" data-k="city" data-v="all">全部</button>
        <span id="city_chips" style="display:contents"></span>
      </div>
    </details>
    <div class="rsec">全部公司（公司池 + 目标公司池，同名合并；只看「公司来源 / 搜索」两类筛选）</div>
    <div id="comp_table"></div>
    <div class="rsec">全部岗位（含已收藏 / 已忽略；按性质、岗位状态与搜索筛选）</div>
    <div id="comp_jobs"></div>
  </div>
</section>

<section id="view-rep" class="view">
  <div class="panel tutpanel" id="tutbox">
    <div class="rhead"><b>📚 牛客面试宝典 · 考点地图</b>
      <span class="rnum" id="tut_meta"></span></div>
    <div class="mnote" id="tut_lead"></div>
    <div class="tuttabs" id="tut_tabs"></div>
    <div id="tut_body"></div>
    <div class="tutfoot">
      <span class="flab">刷题入口</span>
      <span id="tut_practice" style="display:contents"></span>
      <span class="mnote" style="flex:1 1 100%;margin:4px 0 0">
        宝典目录与「学习说明」抓自牛客公开页（未登录可读）；<b>权重 ★</b> 是按原文强调程度的人工标注
        （原文：必考且占比最大的是 C++ 基础与算法；决定 sp offer / 名企的是项目与算法），不是官方分值。
        题干与参考答案在牛客站内需登录且有版权限制，这里只做目录对齐与进度统计，不转载内容。
      </span>
    </div>
  </div>
  <div class="rpanel">
    <div class="rhead"><b>📈 学习分析</b>
      <span id="r_gen" class="rnum"></span></div>
    <div class="mnote">全部数据来自本机浏览器（自评记录 + 错题本），换设备请先用题库页「备份↓」导出。点数字卡或模块行可跳到对应筛选。</div>
    <div class="rsec">总览</div>
    <div class="rcards" id="r_cards"></div>
    <div class="rsec">近 8 周自测节奏（每周自评次数）</div>
    <div class="rchart" id="r_weeks"></div>
    <div class="rsec">模块掌握度（按平均分升序，最弱的排最前）</div>
    <table class="rtable"><thead><tr>
      <th>模块</th><th>已自测 / 总数</th><th>覆盖</th><th>平均分</th><th>薄弱</th><th>到期</th>
    </tr></thead><tbody id="r_mods"></tbody></table>
    <div class="rsec">下一步建议</div>
    <ul class="radv" id="r_adv"></ul>
    <div class="rfoot">
      <button class="mini" id="r_due">📋 今日该复习</button>
      <button class="mini" id="r_weak">🩹 薄弱题清单</button>
      <button class="mini" id="r_clean" title="把已自评 ≥3 且未到期的题移出错题本">🧹 清理错题本</button>
    </div>
  </div>

  <div class="panel" id="loopbox" style="margin-top:14px">
    <div class="rhead"><b>🔁 训练闭环</b><span class="rnum" id="loop_meta"></span></div>
    <div class="mnote">不看「做了多少题」，看「有没有变强」：7 天均值变化 / P0 掌握率 / 连续两次低分 /
      跨 7 天复测通过率 / 卡点模块。复测指同一题间隔 ≥7 天再自评，第一次 4 分不代表长期掌握。</div>
    <div id="loop_body"></div>
    <div class="mrow" style="margin-top:8px">
      <button class="mini" id="loop_drill">🎯 生成今日训练（12 题）</button>
      <span class="rnum">顺序：到期 P0 → 未自测 P0 → 连续两次低分 → 薄弱 → 其他到期</span>
    </div>
  </div>

  <div class="panel" id="projbox" style="margin-top:14px">
    <div class="rhead"><b>🧩 项目证据链</b><span class="rnum" id="proj_meta"></span></div>
    <div class="mnote">每项技能都要能回答「凭什么说我会」：代码 → 指标 → 测试 → 面试表达。
      仓库/测试为空的项目按「证据不完整」处理，<b>不计入岗位卡的工程证据</b>。数据源：<code>companies/projects.json</code>。</div>
    <div id="proj_body"></div>
  </div>

  <div class="panel" id="healthbox" style="margin-top:14px">
    <div class="rhead"><b>🩺 系统健康</b><span class="rnum" id="health_meta"></span></div>
    <div class="mnote">数据质量比数量重要：红色 = 必须处理，黄色 = 需要人工看一眼。构建期指标在 <code>build.py</code> 里算，本地数据在浏览器里现算。</div>
    <div id="health_body"></div>
  </div>
</section>
</div>

<div id="mockov" style="display:none">
  <div class="mpanel">
    <div class="mhead"><b>🎤 模拟面试</b>
      <span id="m_conf"></span>
      <button class="mini" id="m_close">退出</button></div>
    <div id="m_setup">
      <div class="mrow">题源：<b id="m_src"></b></div>
      <div class="mrow">题数：
        <select id="m_n"><option>5</option><option selected>10</option><option>15</option></select>
        ／ 每题限时：
        <select id="m_sec"><option value="180">3 分钟</option><option value="300" selected>5 分钟</option><option value="480">8 分钟</option><option value="0">不限时（练习）</option></select>
        ／ <label class="chk"><input type="checkbox" id="m_follow" checked> 作答后揭示高频追问</label>
      </div>
      <div class="mrow"><button id="m_start" style="padding:8px 20px">开始面试</button></div>
      <div class="mnote">作答方式：对着每道题**先口述完整回答**（自测纪律），再看「高频追问」自检有没有被问倒；每题自评 1~4 分——1 不知道答案 / 2 知道答案但讲不清 / 3 能独立解释 / 4 能应对追问与实现，评分会计入间隔复习。抽题按当前筛选与岗位模板权重进行。</div>
    </div>
    <div id="m_run" style="display:none">
      <div class="mrow"><span id="m_pos"></span> ｜ 剩余 <b id="m_clock"></b>
        <button class="mini" id="m_skip">跳过本题</button></div>
      <div class="mqtitle" id="m_title"></div>
      <textarea id="m_note" placeholder="作答要点草稿：口述前敲几个关键词提醒自己（仅本场保留，切题不丢）"></textarea>
      <div id="m_follows" style="display:none"><div class="gl">高频追问（自检）</div><ol id="m_flist"></ol></div>
      <div class="mrow"><button class="mini" id="m_reveal">揭示追问</button>
        <span class="gl">自评：</span>
        <button class="gbtn" data-v="1">1 不会</button>
        <button class="gbtn" data-v="2">2 想不起</button>
        <button class="gbtn" data-v="3">3 掌握</button>
        <button class="gbtn" data-v="4">4 牢固</button>
        <button id="m_next" style="margin-left:auto">下一题 →</button></div>
    </div>
    <div id="m_end" style="display:none"></div>
  </div>
</div>

<script>
const DATA = __DATA__;
const TARGETS = __TARGETS__;
const PROFILES = __PROFILES__;
const JOBS_SEED = __JOBS__;
const RADAR = __RADAR__;
const POOL = __POOL__;          // companies/radar_companies.json：全量公司池（含未接入源）
const NC = __NC__;              // 牛客面经索引 + 公司真题卷元数据（每周增量同步）
const TUT = __TUT__;            // 牛客面试宝典目录 + 每章命中题号（构建期统计，点进去结果一致）
const PROJD = __PROJ__;         // companies/projects.json：项目证据档案（技能栈 + 证据三态）；PROJ 是项目题池，勿混
const HEALTH = __HEALTH__;      // 构建期数据质量指标（系统健康面板）
const PROF_BY_ID = {}; PROFILES.forEach(p => PROF_BY_ID[p.id] = p);
const WRONG_KEY = 'ib_wrong_v1';
const REV_KEY = 'ib_review_v1';
// 间隔复习：自评分 1~4 → 下次复习间隔天数（SM-2 简化版）
const REV_DAYS = {1: 1, 2: 3, 3: 7, 4: 21};
const OPEN_ALL = location.hash === '#all';   // 调试用：全部展开
const SCHEMA_VERSION = 2;                     // 本地数据/备份格式版本，导入时校验与迁移

// 统一封装浏览器存储：读失败降级为空，写失败必须让用户知道（不能假装已保存）
// 外链白名单：只允许 http/https，挡住 javascript:/data: 这类注入
function safeUrl(u){
  if (!u) return '';
  try {
    const x = new URL(u, location.href);
    return (x.protocol === 'http:' || x.protocol === 'https:') ? x.href : '';
  } catch (e) { return ''; }
}
function lsGet(k, dflt){
  try { const v = localStorage.getItem(k); return v == null ? dflt : JSON.parse(v); }
  catch (e) { console.warn('localStorage 读取失败', k, e); return dflt; }
}
function lsSet(k, v){
  try { localStorage.setItem(k, typeof v === 'string' ? v : JSON.stringify(v)); return true; }
  catch (e) {
    alert('本地存储写入失败：' + (e && e.message ? e.message : e) +
      '\n常见原因：隐私/无痕模式、存储空间已满、浏览器禁用了站点数据。\n本次修改没有保存，请先「备份↓」再换浏览器。');
    return false;
  }
}
let wrong = new Set(lsGet(WRONG_KEY, []));
let review = lsGet(REV_KEY, {});
let SELFTEST = false;
let LASTHIT = [];            // 最近一次渲染命中的题，供模拟面试抽题
let tutFilter = null;        // 宝典章节筛选：{ids:Set, label}（点「练这一章」写入）
let corpFilter = '';         // 企业题库筛选：公司名；不走 TARGETS 下拉，覆盖面经里出现的全部公司
let tutTab = ((TUT.tutorials || [])[0] || {}).id;
function revState(q){
  const r = review[q.id];
  if (!r) return 'never';
  const due = (Date.now() - r.ts) >= REV_DAYS[r.g] * 864e5;
  if (r.g <= 2) return 'weak';
  return due ? 'due' : 'ok';
}

const ROLE_BY_KEY = {};
TARGETS.roles.forEach(r => ROLE_BY_KEY[r.key] = r);
const ALWAYS = new Set(TARGETS.always || []);

// 岗位口径：命中模块或子方向即算对口；算法机考与项目深挖所有岗位都要
function roleHit(q, r){
  if (!r) return false;
  if (ALWAYS.has(q.module)) return true;
  return (r.mods || []).includes(q.module) || (r.subs || []).includes(q.sub);
}
// 公司口径：主投岗位族 + 该公司额外列出的子方向 + 出现记录真实命中
// appearances 格式 "公司·岗位"——出现过该公司面试题的题卡，选该公司时必中
function coHit(q, c){
  if (!c) return false;
  if ((q.appearances || []).some(a => a.split("·")[0] === c.name)) return true;
  if ((c.extra || []).includes(q.sub)) return true;
  return (c.roles || []).some(k => roleHit(q, ROLE_BY_KEY[k]));
}

const $ = id => document.getElementById(id);
const list = $('list');

function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}

function gradeBar(q){
  const r = review[q.id];
  const cls = v => r && r.g === v ? 'on' : '';
  const when = r ? `上次自评 ${r.g} · ${new Date(r.ts).toLocaleDateString()}` : '未自测';
  return `<div class="grade" data-q="${q.id}"><span class="gl">自评</span>
    ${[1,2,3,4].map(v=>`<button class="gbtn ${cls(v)}" data-g="${q.id}" data-v="${v}"
      title="${{1:'不知道答案',2:'知道答案但讲不清',3:'能独立解释',4:'能应对追问与实现'}[v]}">${v}</button>`).join('')}
    <span class="gstat">${when}</span></div>`;
}
const ST_NAME = {official: '官方文档', upstream: '上游项目', self_doc: '本人项目文档',
  self_exp: '本人实测', nowcoder: '牛客面经', video: '视频面经', inferred: '岗位推导'};

function card(q){
  const isW = wrong.has(q.id);
  const st = q.status === 'indexed' ? '<span class="tag">待补充</span>' : '';
  const ev = `<span class="ev ev${q.evidence}" title="证据等级：${{S1:'官方文档/JD',S2:'本人一手',S3:'社区面经',S4:'岗位推导预测'}[q.evidence]}">${q.evidence}</span>`;
  // 掌握状态点：自测模式下隐藏，避免提前泄露难度感
  const rs = revState(q);
  const dmap = {never: ['', '待学习'], weak: ['weak', '薄弱'],
                due: ['due', '今日复习'], ok: ['ok', '已掌握']};
  const dot = SELFTEST ? '' :
    `<span class="qdot ${dmap[rs][0]}" title="掌握状态来自你的自评记录"><i></i>${dmap[rs][1]}</span>`;
  // 收起态就能看到追问数量与第一条，不必展开全文
  const fs = followOf(q);
  const fq = (!SELFTEST && fs.length)
    ? `<div class="qf"><span class="fi">追问 ${fs.length} 条</span>` +
      `<span title="${esc(fs[0])}">${esc(fs[0].slice(0, 46))}${fs[0].length > 46 ? '…' : ''}</span></div>`
    : '';
  const aps = q.appearances || [];
  const qmeta = (q.sourceRef || aps.length)
    ? `<div class="qmeta">` +
      (q.sourceRef
        ? `<span>来源：<a href="${esc(q.sourceRef)}" target="_blank" rel="noopener">` +
          `${esc(q.sourceRef.length > 64 ? q.sourceRef.slice(0, 64) + '…' : q.sourceRef)}</a>` +
          `<span>（${ST_NAME[q.sourceType] || q.sourceType}）</span></span>`
        : '') +
      (aps.length
        ? `<span>真实出现：${aps.map(a => `<span class="tag appear">${esc(a)}</span>`).join(' ')}</span>`
        : '') +
      `</div>`
    : '';
  const df = q.difficulty || 2;
  const stars = '★'.repeat(df) + '☆'.repeat(Math.max(0, 3 - df));
  return `<article class="q" data-id="${q.id}">
    <div class="qh">
      <span class="pid">${q.id}</span>
      <span class="pri ${q.priority}">${q.priority}</span>
      <div class="qt">${esc(q.title)}</div>
      <span class="tag">${esc(q.sub || q.moduleName)}</span>
      <span class="tag" title="难度">${stars}</span>
      ${ev}${st}${dot}
      <button class="wrongmark ${isW?'on':''}" data-w="${q.id}">${isW?'已标错':'标错'}</button>
    </div>
    ${fq}
    <div class="body">${q.html}${qmeta}${gradeBar(q)}</div>
  </article>`;
}

function refreshSubs(){
  const mod = $('mod').value;
  const cur = $('sub').value;
  const set = [...new Set(DATA.filter(q => !mod || q.module === mod)
                                .map(q => q.sub).filter(Boolean))].sort();
  $('sub').innerHTML = '<option value="">全部子方向</option>' +
    set.map(s => `<option value="${esc(s)}">${esc(s)}</option>`).join('');
  if (set.includes(cur)) $('sub').value = cur;
}

// ── 题库导航：按考点 / 企业题库（对应截图里的分类卡片）──
function corpOf(q){
  const s = new Set();
  (q.appearances || []).forEach(a => { const n = String(a).split('·')[0].trim(); if (n) s.add(n); });
  (q.companies || []).forEach(n => { const t = String(n).split('·')[0].trim(); if (t) s.add(t); });
  return [...s];
}

let NAV_ALL = null;
let NAV_MORE_T = false, NAV_MORE_C = false;
let NAV_MOD = '';
const NAV_TOPIC_LIMIT = 18, NAV_CORP_LIMIT = 8;

function bankNavData(){
  const TM = new Map(), CM = new Map();
  const all = { name: '', label: '通用题库（全部）', n: 0, d: [0, 0, 0], subs: new Set() };
  DATA.forEach(q => {
    const d = Math.min(2, Math.max(0, (q.difficulty || 2) - 1));
    all.n++; all.d[d]++; all.subs.add(q.module + '|' + (q.sub || '未分类'));
    const k = q.module + '|' + (q.sub || '未分类');
    let t = TM.get(k);
    if (!t) { t = { module: q.module, moduleName: q.moduleName, sub: q.sub || '未分类', n: 0, d: [0, 0, 0] }; TM.set(k, t); }
    t.n++; t.d[d]++;
    corpOf(q).forEach(c => {
      let o = CM.get(c);
      if (!o) { o = { name: c, n: 0, d: [0, 0, 0], subs: new Set() }; CM.set(c, o); }
      o.n++; o.d[d]++; o.subs.add(q.sub || '未分类');
    });
  });
  return {
    topics: [...TM.values()].sort((a, b) => b.n - a.n || a.sub.localeCompare(b.sub)),
    corps: [...CM.values()].sort((a, b) => b.n - a.n || a.name.localeCompare(b.name)),
    all
  };
}

function renderBankNav(){
  const { topics, corps, all } = bankNavData();
  NAV_ALL = all;
  const modCnt = new Map();
  topics.forEach(t => modCnt.set(t.module, (modCnt.get(t.module) || 0) + t.n));
  const mods = [...modCnt.entries()].sort((a, b) => b[1] - a[1]);
  $('modrow').innerHTML =
    `<button class="mchip${NAV_MOD ? '' : ' on'}" data-m="">全部 <b>${topics.reduce((s, t) => s + t.n, 0)}</b></button>`
    + mods.map(([m, n]) => {
        const nm = (topics.find(t => t.module === m) || {}).moduleName || m;
        return `<button class="mchip${NAV_MOD === m ? ' on' : ''}" data-m="${esc(m)}">${esc(nm)} <b>${n}</b></button>`;
      }).join('');
  const tFiltered = NAV_MOD ? topics.filter(t => t.module === NAV_MOD) : topics;
  const tShow = NAV_MORE_T ? tFiltered : tFiltered.slice(0, NAV_TOPIC_LIMIT);
  $('topicgrid').innerHTML = tShow.map(t =>
    `<button class="tcard" data-mod="${esc(t.module)}" data-sub="${esc(t.sub)}">`
    + `<span class="tn">${esc(t.sub)}</span><span class="tm">${esc(t.moduleName)}</span>`
    + `<span class="tc">${t.n} 题 · 易 ${t.d[0]} 中 ${t.d[1]} 难 ${t.d[2]}</span></button>`).join('');
  $('more_topic').innerHTML = tFiltered.length > NAV_TOPIC_LIMIT
    ? `<button data-more="t">${NAV_MORE_T ? '收起' : `展开全部 ${tFiltered.length} 个考点`}</button>` : '';
  const cAll = [all, ...corps];
  const cShow = NAV_MORE_C ? cAll : cAll.slice(0, NAV_CORP_LIMIT);
  $('corpgrid').innerHTML = cShow.map(o => {
    const tot = o.n || 1;
    const p = o.d.map(x => (x / tot * 100).toFixed(1));
    return `<button class="ccard" data-co="${esc(o.name)}">`
      + `<span class="cn">${o.name ? esc(o.name) : o.label}</span>`
      + `<span class="cm"><b>${o.n}</b> 题 · ${o.subs.size} 个考点</span>`
      + `<span class="dbar2"><i class="d1" style="width:${p[0]}%"></i>`
      + `<i class="d2" style="width:${p[1]}%"></i><i class="d3" style="width:${p[2]}%"></i></span>`
      + `<span class="cd">易 ${o.d[0]} · 中 ${o.d[1]} · 难 ${o.d[2]}</span></button>`;
  }).join('');
  $('more_corp').innerHTML = cAll.length > NAV_CORP_LIMIT
    ? `<button data-more="c">${NAV_MORE_C ? '收起' : `展开全部 ${cAll.length} 个题库`}</button>` : '';
  $('nt_topic').textContent = topics.length + ' 个';
  $('nt_corp').textContent = corps.length + ' 家';
  syncNavSel();
}

function syncNavSel(){
  const mod = $('mod').value, sub = $('sub').value;
  document.querySelectorAll('#topicgrid .tcard').forEach(el =>
    el.classList.toggle('on', el.dataset.mod === mod && el.dataset.sub === sub));
  document.querySelectorAll('#corpgrid .ccard').forEach(el =>
    el.classList.toggle('on', (el.dataset.co || '') === corpFilter));
  const hint = $('drillhint');
  if (!hint) return;
  const co = corpFilter ? `企业「${corpFilter}」` : '';
  const tp = (!corpFilter && sub) ? `考点「${sub}」` : '';
  hint.innerHTML = (co || tp)
    ? `当前范围：${co || tp} · ${LASTHIT.length} 题　<a class="clr" id="navclr">清除</a>`
    : `当前范围：全部 ${DATA.length} 题`;
  const c = navclrEl();
  if (c) c.addEventListener('click', () => { corpFilter = ''; render(); });
}
function navclrEl(){ return document.getElementById('navclr'); }

document.querySelectorAll('.ntab').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.ntab').forEach(x => x.classList.toggle('on', x === b));
  const t = b.dataset.nt;
  $('nav_topic').hidden = t !== 'topic';
  $('nav_corp').hidden = t !== 'corp';
  $('banknav').classList.toggle('compact', t === 'list');
}));

$('topicgrid').addEventListener('click', e => {
  const b = e.target.closest('.tcard'); if (!b) return;
  corpFilter = ''; $('co').value = '';
  $('mod').value = b.dataset.mod; refreshSubs(); $('sub').value = b.dataset.sub;
  render();
  $('list').scrollIntoView({ behavior: 'smooth', block: 'start' });
});

$('corpgrid').addEventListener('click', e => {
  const b = e.target.closest('.ccard'); if (!b) return;
  corpFilter = b.dataset.co || '';
  $('co').value = ''; $('mod').value = ''; refreshSubs(); $('sub').value = ''; $('dif').value = '';
  render();
  $('list').scrollIntoView({ behavior: 'smooth', block: 'start' });
});

$('modrow').addEventListener('click', e => {
  const b = e.target.closest('.mchip'); if (!b) return;
  NAV_MOD = b.dataset.m || ''; NAV_MORE_T = false; renderBankNav();
});
$('more_topic').addEventListener('click', () => { NAV_MORE_T = !NAV_MORE_T; renderBankNav(); });
$('more_corp').addEventListener('click', () => { NAV_MORE_C = !NAV_MORE_C; renderBankNav(); });

$('drill10').addEventListener('click', () => {
  if (!LASTHIT.length) { alert('当前范围没有题，先选一个考点或企业'); return; }
  $('m_n').value = '10';
  openMock();
  $('m_start').click();
});

function render(){
  const kw = $('q').value.trim().toLowerCase();
  const mod = $('mod').value, pri = $('pri').value, st = $('st').value;
  const sub = $('sub').value, dif = $('dif').value;
  const onlyW = $('wrong').checked;
  const coDef = TARGETS.companies.find(c => c.name === $('co').value);
  const rlDef = ROLE_BY_KEY[$('rl').value];
  SELFTEST = $('selftest').checked;

  // 关键词命中公司名/岗位名时，按那套口径过滤（这样直接搜 "Momenta" 也能用）
  let kwCo = null, kwRl = null, kwPlain = false;
  if (kw) {
    kwCo = TARGETS.companies.find(c =>
      c.name.toLowerCase().includes(kw) ||
      (c.aliases || []).some(a => a.toLowerCase().includes(kw)));
    kwRl = TARGETS.roles.find(r =>
      r.name.toLowerCase().includes(kw) ||
      (r.aliases || []).some(a => a.toLowerCase().includes(kw)));
  }

  const hit = DATA.filter(q => {
    if (mod && q.module !== mod) return false;
    if (corpFilter && !corpOf(q).includes(corpFilter)) return false;
    if (sub && q.sub !== sub) return false;
    if (pri && q.priority !== pri) return false;
    if (dif && q.difficulty !== +dif) return false;
    if (st && q.status !== st) return false;
    if (onlyW && !wrong.has(q.id)) return false;
    if (tutFilter && !tutFilter.ids.has(q.id)) return false;
    if ($('hidepred').checked && q.evidence === 'S4') return false;
    const rv = $('rev').value;
    if (rv && revState(q) !== rv) return false;
    const prof = PROF_BY_ID[$('prof').value];
    if (prof && (prof.weights[q.module] || 0) <= 0) return false;
    if (coDef && !coHit(q, coDef)) return false;
    if (rlDef && !roleHit(q, rlDef)) return false;
    if (!kw) return true;
    const hay = (q.title + ' ' + q.id + ' ' + q.tags.join(' ') +
                 ' ' + (q.sub || '') + ' ' + (q.appearances || []).join(' ') +
                 ' ' + q.plain).toLowerCase();
    if (hay.includes(kw)) return true;
    if (kwCo && coHit(q, kwCo)) return true;
    if (kwRl && roleHit(q, kwRl)) return true;
    return false;
  });

  list.innerHTML = hit.map(card).join('');
  LASTHIT = hit; fcur = -1;
  $('empty').style.display = hit.length ? 'none' : 'block';
  // 搜索/筛选时自动展开，省一次点击；自测模式下不展开，先自己答
  if (!SELFTEST && (kw || mod || pri || st || sub || dif || onlyW || coDef || rlDef || corpFilter || OPEN_ALL)) {
    list.querySelectorAll('.q').forEach(el => el.classList.add('open'));
  }
  if (SELFTEST) list.classList.add('selftest'); else list.classList.remove('selftest');
  const dueCnt = DATA.filter(q => revState(q) === 'due').length;
  $('stat').textContent = `共 ${DATA.length} 题 ｜ 当前 ${hit.length} 题 ｜ `
    + `已答 ${DATA.filter(q=>q.status==='answered'||q.status==='verified').length} ｜ 草稿 ${DATA.filter(q=>q.status==='draft').length} ｜ 错题 ${wrong.size} ｜ `
    + `有出现记录 ${DATA.filter(q=>(q.appearances||[]).length).length} ｜ `
    + `已自测 ${Object.keys(review).length} ｜ 今日该复习 ${dueCnt}`;
  syncChips(); syncPills(); renderScards(); syncNavSel();

  // 宝典章节筛选提示条（从「分析 → 考点地图」跳进来时显示）
  const tb = $('tutbanner');
  if (tutFilter) {
    tb.hidden = false;
    const kindTxt = tutFilter.kind === 'today' ? '🎯 今日训练' : '📚 宝典章节';
    tb.innerHTML = `${kindTxt}：<b>${esc(tutFilter.label || '')}</b> · ${tutFilter.ids.size} 题`
      + ` <button id="tutclear" title="取消章节筛选，回到全部题目">×</button>`;
  } else {
    tb.hidden = true;
  }

  // 口径说明：让人知道"为什么这些题被算进来"
  const tips = [];
  const tCo = coDef || kwCo, tRl = rlDef || kwRl;
  if (tCo) tips.push(`公司 <b>${esc(tCo.name)}</b>（主投 ${esc(tCo.main || '—')}）`);
  if (tRl) tips.push(`岗位族 <b>${esc(tRl.name)}</b>：${esc(tRl.focus || '')}`);
  if (tips.length) {
    const uni = (TARGETS.universal || [])
      .map(m => DATA.filter(q => q.module === m).length).reduce((a, b) => a + b, 0);
    tips.push(`另有 <b>${uni}</b> 道算法机考为所有人的门槛项，不参与上面的口径`);
    tips.push('口径按 JD 推导，<span class="warn">不是该公司真实考题</span>');
  }
  $('hint').innerHTML = tips.join('　·　');
}

// 自评 1~4 写入复习计划；不会/想不起自动进错题本（卡片按钮与快捷键共用）
// 每次自评同时追加训练历史（首页「最近训练记录」与「今日任务」的完成度来源）
const HIST_KEY = 'ib_hist_v1';
let hist = lsGet(HIST_KEY, []);
function pushHist(qid, v){
  hist.push({ i: qid, g: v, t: Date.now(), m: MOCK.live ? 1 : 0 });
  if (hist.length > 600) hist = hist.slice(-500);
  lsSet(HIST_KEY, hist);
}
function setGrade(qid, v){
  review[qid] = { g: v, ts: Date.now() };
  localStorage.setItem(REV_KEY, JSON.stringify(review));
  pushHist(qid, v);
  if (v <= 2 && !wrong.has(qid)) {
    wrong.add(qid);
    localStorage.setItem(WRONG_KEY, JSON.stringify([...wrong]));
  }
}

list.addEventListener('click', e => {
  const wb = e.target.closest('[data-w]');
  if (wb) {
    const id = wb.dataset.w;
    wrong.has(id) ? wrong.delete(id) : wrong.add(id);
    localStorage.setItem(WRONG_KEY, JSON.stringify([...wrong]));
    wb.classList.toggle('on');
    wb.textContent = wrong.has(id) ? '已标错' : '标错';
    $('stat').textContent = $('stat').textContent.replace(/错题 \d+/, '错题 ' + wrong.size);
    return;
  }
  // 自评分按钮：1 不会 / 2 想不起来 / 3 基本掌握 / 4 可答追问 → 安排间隔复习
  const gbtn = e.target.closest('.gbtn');
  if (gbtn) {
    const qid = gbtn.dataset.g, v = +gbtn.dataset.v;
    setGrade(qid, v);
    const bar = gbtn.closest('.grade');
    bar.querySelectorAll('.gbtn').forEach(b =>
      b.classList.toggle('on', +b.dataset.v === v));
    const gs = bar.querySelector('.gstat');
    if (gs) gs.textContent = `上次自评 ${v} · ${new Date().toLocaleDateString()}`
      + (v <= 2 ? ' · 已标薄弱' : ` · ${REV_DAYS[v]} 天后复习`);
    render();
    return;
  }
  const head = e.target.closest('.qh');
  if (head) head.parentElement.classList.toggle('open');
});

// ---- 顶部学习数据卡：点击跳对应筛选 ----
function renderScards(){
  const tested = Object.keys(review).filter(id => QBY[id]);
  const dueN  = tested.filter(id => isDue(review[id])).length;
  const weakN = tested.filter(id => review[id].g <= 2).length;
  $('scards').innerHTML = `
    <div class="scard" data-s="none"><b>${DATA.length}</b><small>总题目 · 已自测 ${tested.length}</small></div>
    <div class="scard ${dueN ? 'warn' : ''}" data-s="due"><b>${dueN}</b><small>今日待复习</small></div>
    <div class="scard ${weakN ? 'warn' : ''}" data-s="weak"><b>${weakN}</b><small>薄弱题目</small></div>
    <div class="scard ${wrong.size ? 'warn' : ''}" data-s="wrong"><b>${wrong.size}</b><small>错题本</small></div>`;
}
$('scards').addEventListener('click', e => {
  const c = e.target.closest('.scard'); if (!c) return;
  const s = c.dataset.s;
  if (s === 'due' || s === 'weak') $('rev').value = s;
  else if (s === 'wrong') $('wrong').checked = true;
  else return;
  showView('bank'); window.scrollTo(0, 0); render();
});

// ---- 快捷筛选 chips：一级高频条件，与详细筛选控件双向同步 ----
function syncChips(){
  const on = {
    p0: $('pri').value === 'P0',
    due: $('rev').value === 'due', weak: $('rev').value === 'weak',
    wrong: $('wrong').checked, real: $('hidepred').checked,
    selftest: $('selftest').checked };
  $('selftest_v').checked = $('selftest').checked;
  document.querySelectorAll('#chips .chip').forEach(ch => {
    const c = ch.dataset.c;
    ch.classList.toggle('on', c === 'all' ? !Object.values(on).some(Boolean) : !!on[c]);
  });
}
$('chips').addEventListener('click', e => {
  const ch = e.target.closest('.chip'); if (!ch) return;
  const c = ch.dataset.c;
  if (c === 'all') {
    $('pri').value = ''; $('rev').value = '';
    $('wrong').checked = $('hidepred').checked = $('selftest').checked = false;
    tutFilter = null;
  } else if (c === 'p0') $('pri').value = $('pri').value === 'P0' ? '' : 'P0';
  else if (c === 'due' || c === 'weak') $('rev').value = $('rev').value === c ? '' : c;
  else if (c === 'wrong') $('wrong').checked = !$('wrong').checked;
  else if (c === 'real') $('hidepred').checked = !$('hidepred').checked;
  else if (c === 'selftest') $('selftest').checked = !$('selftest').checked;
  render();
});
// 更多筛选里的「自测模式」开关：与内部隐藏 checkbox 双向同步
$('selftest_v').addEventListener('change', e => {
  $('selftest').checked = e.target.checked;
  render();
});

// ---- 详细筛选的条件 pills：可单独移除，不必整体重置 ----
function syncPills(){
  const defs = [
    ['co', '公司', $('co').value],
    ['rl', '岗位', $('rl').value && (ROLE_BY_KEY[$('rl').value] || {}).name],
    ['prof', '模板', $('prof').value && (PROF_BY_ID[$('prof').value] || {}).name],
    ['mod', '模块', $('mod').value && MODNAME[$('mod').value]],
    ['sub', '子方向', $('sub').value],
    ['pri', '优先级', $('pri').value],
    ['dif', '难度', $('dif').value && '★'.repeat(+$('dif').value)],
    ['st', '状态', $('st').value], ['rev', '复习', $('rev').value],
  ];
  const pills = defs.filter(d => d[2]).map(([id, label, val]) =>
    `<span class="fpill"><b>${label}：${esc(val)}</b><i data-p="${id}" title="单独移除这个条件">×</i></span>`);
  $('fpills').innerHTML = pills.join('');
  $('fcount').textContent = pills.length;
  $('fcount').style.display = pills.length ? 'inline-block' : 'none';
}
$('fpills').addEventListener('click', e => {
  const i = e.target.closest('[data-p]'); if (!i) return;
  $(i.dataset.p).value = '';
  render();
});

// ---- 桌面快捷键：/ 搜索 · J/K 上下题 · 空格展开 · 1-4 自评 · W 标错 ----
let fcur = -1;
function moveFocus(d){
  if (!LASTHIT.length) return;
  fcur = Math.min(LASTHIT.length - 1, Math.max(0, fcur + d));
  const el = list.children[fcur];
  if (!el) return;
  list.querySelectorAll('.q.foc').forEach(x => x.classList.remove('foc'));
  el.classList.add('foc');
  el.scrollIntoView({ block: 'center' });
}
document.addEventListener('keydown', e => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const tag = e.target.tagName;
  if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') {
    if (e.key === 'Escape') e.target.blur();
    return;
  }
  if (e.key === 'Escape') {
    if ($('mockov').style.display === 'block') {
      clearInterval(MOCK.timer); MOCK.live = false; $('mockov').style.display = 'none';
    }
    return;
  }
  if ($('mockov').style.display === 'block') return;
  if (e.key === '/') { e.preventDefault(); $('q').focus(); $('q').select(); }
  else if (e.key === 'j' || e.key === 'J') moveFocus(fcur < 0 ? 0 : 1);
  else if (e.key === 'k' || e.key === 'K') moveFocus(-1);
  else if (e.key === 'Enter' || e.key === ' ') {
    const el = list.children[fcur];
    if (el) { e.preventDefault(); el.classList.toggle('open'); }
  }
  else if (['1', '2', '3', '4'].includes(e.key)) {
    const el = list.children[fcur];
    if (el) {
      setGrade(el.dataset.id, +e.key);
      const v = +e.key, bar = el.querySelector('.grade');
      if (bar) {
        bar.querySelectorAll('.gbtn').forEach(b => b.classList.toggle('on', +b.dataset.v === v));
        const gs = bar.querySelector('.gstat');
        if (gs) gs.textContent = `上次自评 ${v} · ${new Date().toLocaleDateString()}`
          + (v <= 2 ? ' · 已标薄弱' : ` · ${REV_DAYS[v]} 天后复习`);
      }
      render();
      const el2 = list.children[fcur];
      if (el2) el2.classList.add('foc');
    }
  }
  else if (e.key === 'w' || e.key === 'W') {
    const el = list.children[fcur];
    if (el) {
      const id = el.dataset.id;
      wrong.has(id) ? wrong.delete(id) : wrong.add(id);
      localStorage.setItem(WRONG_KEY, JSON.stringify([...wrong]));
      render();
      const el2 = list.children[fcur];
      if (el2) el2.classList.add('foc');
    }
  }
});

// 复习数据备份：导出/导入（schema_version=2；导入前校验 → 预览 → 默认合并）
function backupPayload(){
  const jobs = lsGet(LOCAL_JOBS_KEY, []);
  return {
    app: 'CareerOS', schema_version: SCHEMA_VERSION,
    exported_at: new Date().toISOString(),
    counts: {review: Object.keys(review).length, wrong: wrong.size,
             hist: hist.length, jobs: jobs.length, dismiss: [...loadDismiss()].length},
    data: {wrong: [...wrong], review, hist, jobs, dismiss: [...loadDismiss()]}
  };
}
$('exp').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(backupPayload(), null, 1)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `careeros-backup-v${SCHEMA_VERSION}-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
});

// 校验 + 归一化：返回 {errs, warns, review, wrong, hist, jobs, dismiss, ver}
function parseBackup(text){
  const out = {errs: [], warns: [], review: {}, wrong: [], hist: [], jobs: [], dismiss: [], ver: 0};
  let d;
  try { d = JSON.parse(text); } catch { out.errs.push('不是合法 JSON'); return out; }
  if (!d || typeof d !== 'object' || Array.isArray(d)) { out.errs.push('顶层不是对象'); return out; }
  out.ver = Number(d.schema_version || ((d.wrong || d.review) ? 1 : 0));
  if (!out.ver) { out.errs.push('缺少 schema_version，也不是 v1 备份（无 wrong/review）'); return out; }
  if (out.ver > SCHEMA_VERSION) {
    out.errs.push(`备份版本 v${out.ver} 高于当前页面 v${SCHEMA_VERSION}，请先更新页面再导入`);
    return out;
  }
  const data = (d.data && typeof d.data === 'object') ? d.data : d;   // v1 兼容
  const valid = new Set(DATA.map(q => q.id));
  if (data.review != null) {
    if (typeof data.review !== 'object' || Array.isArray(data.review)) out.errs.push('review 应为对象');
    else Object.entries(data.review).forEach(([id, v]) => {
      if (!v || typeof v !== 'object' || [1, 2, 3, 4].indexOf(v.g) < 0 || typeof v.ts !== 'number') {
        out.warns.push('跳过格式异常的自测记录'); return;
      }
      if (!valid.has(id)) { out.warns.push('跳过题库里不存在的题号'); return; }
      out.review[id] = {g: v.g, ts: v.ts};
    });
  }
  if (data.wrong != null) {
    if (!Array.isArray(data.wrong)) out.errs.push('wrong 应为数组');
    else out.wrong = data.wrong.filter(id => typeof id === 'string' && valid.has(id));
  }
  if (data.hist != null && Array.isArray(data.hist)) out.hist = data.hist.filter(x => x && typeof x === 'object');
  if (data.jobs != null) {
    if (!Array.isArray(data.jobs)) out.errs.push('jobs 应为数组');
    else out.jobs = data.jobs.filter(j => j && typeof j === 'object' && (j.company || j.title));
  }
  if (data.dismiss != null && Array.isArray(data.dismiss)) {
    out.dismiss = data.dismiss.filter(k => typeof k === 'string');
  }
  return out;
}

const jobKeyOf = j => j.id || j.key || ((j.company || '') + '|' + (j.title || ''));

function planImport(p){
  const revAdd = [], revUpd = [];
  Object.entries(p.review).forEach(([id, v]) => {
    if (!review[id]) revAdd.push(id);
    else if (v.ts > (review[id].ts || 0)) revUpd.push(id);
  });
  const wrongAdd = p.wrong.filter(id => !wrong.has(id));
  const curJobs = lsGet(LOCAL_JOBS_KEY, []);
  const curKeys = new Set(curJobs.map(jobKeyOf));
  const jobsAdd = p.jobs.filter(j => !curKeys.has(jobKeyOf(j)));
  const histKeys = new Set(hist.map(x => JSON.stringify(x)));
  const histAdd = p.hist.filter(x => !histKeys.has(JSON.stringify(x)));
  const dis = loadDismiss();
  const disAdd = p.dismiss.filter(k => !dis.has(k));
  return {revAdd, revUpd, wrongAdd, jobsAdd, histAdd, disAdd};
}

$('impb').addEventListener('click', () => $('imp').click());
$('imp').addEventListener('change', e => {
  const f = e.target.files[0];
  e.target.value = '';                       // 允许重复选同一个文件
  if (!f) return;
  const rd = new FileReader();
  rd.onload = () => {
    const p = parseBackup(rd.result);
    if (p.errs.length) { alert('导入失败：\n· ' + p.errs.join('\n· ')); return; }
    const plan = planImport(p);
    const warn = p.warns.length ? `\n\n已忽略 ${p.warns.length} 条（${[...new Set(p.warns)].join('、')}）` : '';
    const msg = `备份版本 v${p.ver}，共 ${Object.keys(p.review).length} 条自测、${p.wrong.length} 条错题、${p.jobs.length} 个岗位、${p.hist.length} 条训练记录。\n\n`
      + `将合并到本机（不覆盖较新的记录）：\n`
      + `· 自测：新增 ${plan.revAdd.length} 条，更新 ${plan.revUpd.length} 条\n`
      + `· 错题：新增 ${plan.wrongAdd.length} 条\n`
      + `· 岗位：新增 ${plan.jobsAdd.length} 个\n`
      + `· 训练记录：新增 ${plan.histAdd.length} 条\n`
      + `· 忽略清单：新增 ${plan.disAdd.length} 条`
      + warn + `\n\n确定导入？`;
    if (!confirm(msg)) return;
    // 合并：自测按 ts 取新，其余取并集
    const merged = Object.assign({}, review);
    Object.entries(p.review).forEach(([id, v]) => {
      if (!merged[id] || v.ts > (merged[id].ts || 0)) merged[id] = v;
    });
    review = merged;
    p.wrong.forEach(id => wrong.add(id));
    const histSeen = new Set(hist.map(x => JSON.stringify(x)));
    p.hist.forEach(x => { const k = JSON.stringify(x); if (!histSeen.has(k)) { histSeen.add(k); hist.push(x); } });
    const curJobs = lsGet(LOCAL_JOBS_KEY, []);
    const curKeys = new Set(curJobs.map(jobKeyOf));
    p.jobs.forEach(j => { if (!curKeys.has(jobKeyOf(j))) { curJobs.push(j); curKeys.add(jobKeyOf(j)); } });
    const dis = loadDismiss();
    p.dismiss.forEach(k => dis.add(k));

    const okAll = lsSet(REV_KEY, review) & lsSet(WRONG_KEY, [...wrong]) &
      lsSet(HIST_KEY, hist) & lsSet(LOCAL_JOBS_KEY, curJobs) & lsSet(DISMISS_KEY, [...dis]);
    render();
    alert(okAll ? `已导入：自测 ${Object.keys(review).length} 条（新增 ${plan.revAdd.length}）｜错题 ${wrong.size}｜岗位 ${curJobs.length}｜训练记录 ${hist.length}`
                : '部分数据写入失败，见上方提示；建议先导出备份再换浏览器');
  };
  rd.readAsText(f);
});

// 支持 ?co=Momenta&rl=C&q=关键字，链接可直接分享
const _p = new URLSearchParams(location.search);
[['co','co'],['rl','rl'],['mod','mod'],['q','q']].forEach(([k, id]) => {
  const v = _p.get(k);
  if (v) $(id).value = v;
});

['q','mod','pri','st','sub','co','rl','wrong','hidepred','selftest','rev','prof','dif'].forEach(id =>
  $(id).addEventListener('input', () => { if (id === 'co') corpFilter = ''; render(); }));
$('mod').addEventListener('input', () => { refreshSubs(); render(); });

// ---- 模拟面试：抽题 → 逐题计时 → 揭示追问 → 自评 → 总结 ----
const MODNAME = {}; DATA.forEach(q => MODNAME[q.module] = q.moduleName);
const MOCK = { list: [], i: 0, left: 0, timer: null, secs: 300, live: false, notes: {} };

$('prof').addEventListener('input', () => {
  // 岗位模板选中时，把权重写进提示行
  const p = PROF_BY_ID[$('prof').value];
  if (!p) return;
  const bars = Object.entries(p.weights).sort((a, b) => b[1] - a[1])
    .map(([m, w]) => `${MODNAME[m] || m} ${w}%`).join(' ｜ ');
  $('hint').innerHTML = `岗位模板 <b>${esc(p.name)}</b>（按真实校招 JD 归纳的配比）：${bars}`
    + `　·　<button class="mini" id="m_quick">🎤 直接开一场</button>`;
  $('m_quick').addEventListener('click', openMock);
});

function openMock(){
  const prof = PROF_BY_ID[$('prof').value];
  // 面试官不会问"这段代码输出什么"——读程序自测题默认排除，仅当池为空才兜底
  const real = LASTHIT.filter(q => q.qtype !== 'coding');
  const pool = real.length ? real
    : (LASTHIT.length ? LASTHIT : DATA.filter(q => q.status !== 'indexed'));
  $('m_ov_src') && 0;
  $('m_src').textContent = (prof ? `岗位模板「${prof.name}」` : '当前筛选结果') + `，池 ${pool.length} 题`;
  $('m_conf').textContent = '';
  $('m_setup').style.display = 'block';
  $('m_run').style.display = 'none';
  $('m_end').style.display = 'none';
  $('mockov').style.display = 'block';
  MOCK.pool = pool;
}
$('mock').addEventListener('click', openMock);
$('m_close').addEventListener('click', () => {
  clearInterval(MOCK.timer); MOCK.live = false; $('mockov').style.display = 'none';
});

// ---- 项目连环问：按项目顺序过全部题，不限时（面试官就是这么连环问的） ----
const PROJ = {};
DATA.forEach(q => { if (q.module === '01_project' && q.sub)
  (PROJ[q.sub] = PROJ[q.sub] || []).push(q); });

function openDrill(sub){
  const qs = (PROJ[sub] || []).slice().sort((a, b) => a.id < b.id ? -1 : 1);
  if (!qs.length) return;
  MOCK.list = qs; MOCK.i = 0; MOCK.graded = []; MOCK.notes = {};
  MOCK.secs = 0; MOCK.live = true; MOCK.drill = sub;
  $('m_src').textContent = `项目连环问 · ${sub} · 顺序 ${qs.length} 题 · 不限时`;
  $('m_conf').textContent = '';
  $('m_setup').style.display = 'none';
  $('m_run').style.display = 'block';
  $('m_end').style.display = 'none';
  $('mockov').style.display = 'block';
  showQ();
}

function shuffle(a){ for (let i = a.length - 1; i > 0; --i) {
  const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

function weightedPick(pool, prof, n){
  // 按模块权重加权抽题：P0 优先入池，权重大的模块概率高
  let bag = [];
  pool.forEach(q => {
    const w = prof ? (prof.weights[q.module] || 0) : (q.priority === 'P0' ? 3 : 1);
    const bonus = q.priority === 'P0' ? 2 : 1;
    for (let k = 0; k < Math.max(1, Math.round(w * bonus / 10)); ++k) bag.push(q);
  });
  if (!bag.length) bag = pool.slice();
  const seen = new Set(), out = [];
  for (const q of shuffle(bag)) {
    if (seen.has(q.id)) continue;
    seen.add(q.id); out.push(q);
    if (out.length >= n) break;
  }
  return out;
}

function followOf(q){
  // 从卡面 html 里抽「高频追问」节的列表项
  const i = q.html.indexOf('高频追问');
  if (i < 0) return [];
  const seg = q.html.slice(i, q.html.indexOf('<h2', i) > 0 ? q.html.indexOf('<h2', i) : undefined);
  return [...seg.matchAll(/<li>([\s\S]*?)<\/li>/g)].map(m =>
    m[1].replace(/<[^>]+>/g, '').trim()).filter(x => x && x !== '待补充').slice(0, 6);
}

$('m_start').addEventListener('click', () => {
  const prof = PROF_BY_ID[$('prof').value];
  const n = +$('m_n').value;
  MOCK.secs = +$('m_sec').value;
  MOCK.list = weightedPick(MOCK.pool, prof, n);
  if (!MOCK.list.length) { alert('题池为空：先调整筛选或选择岗位模板'); return; }
  MOCK.i = 0; MOCK.graded = []; MOCK.notes = {}; MOCK.live = true; MOCK.drill = null;
  $('m_setup').style.display = 'none';
  $('m_run').style.display = 'block';
  showQ();
});

function showQ(){
  const q = MOCK.list[MOCK.i];
  $('m_pos').textContent = `第 ${MOCK.i + 1} / ${MOCK.list.length} 题 ｜ ${q.id} ｜ ${MODNAME[q.module] || q.module}`;
  $('m_title').textContent = q.title;
  $('m_note').value = MOCK.notes[q.id] || '';
  $('m_follows').style.display = 'none';
  MOCK.left = MOCK.secs;
  clearInterval(MOCK.timer);
  if (MOCK.secs > 0) {
    $('m_clock').textContent = `${MOCK.secs / 60}:00`;
    MOCK.timer = setInterval(() => {
      MOCK.left--;
      const m = Math.floor(MOCK.left / 60), s = MOCK.left % 60;
      $('m_clock').textContent = `${m}:${String(s).padStart(2, '0')}`;
      if (MOCK.left <= 0) { clearInterval(MOCK.timer); $('m_clock').textContent = '时间到'; }
    }, 1000);
  } else {
    $('m_clock').textContent = '不限时';
  }
}
$('m_note').addEventListener('input', () => {
  const q = MOCK.list[MOCK.i];
  if (q) MOCK.notes[q.id] = $('m_note').value;
});

$('m_reveal').addEventListener('click', () => {
  const q = MOCK.list[MOCK.i];
  const fs = followOf(q);
  $('m_flist').innerHTML = fs.length
    ? fs.map(x => `<li>${esc(x)}</li>`).join('')
    : '<li>本题卡未配置高频追问，去题库页面看「讲深一层」自检</li>';
  $('m_follows').style.display = 'block';
});

function gradeMock(v){
  setGrade(MOCK.list[MOCK.i].id, v);
  MOCK.graded.push(v);
  nextQ();
}
document.querySelectorAll('#m_run .gbtn').forEach(b =>
  b.addEventListener('click', () => gradeMock(+b.dataset.v)));
$('m_skip').addEventListener('click', () => { MOCK.graded.push(1); nextQ(); });
$('m_next').addEventListener('click', () => nextQ());

function nextQ(){
  clearInterval(MOCK.timer);
  MOCK.i++;
  if (MOCK.i < MOCK.list.length) { showQ(); return; }
  MOCK.live = false;
  // 总结
  $('m_run').style.display = 'none';
  $('m_end').style.display = 'block';
  const c = [1, 2, 3, 4].map(v => MOCK.graded.filter(x => x === v).length);
  const weak = MOCK.graded.map((g, i) => g <= 2 ? MOCK.list[i] : null).filter(Boolean);
  $('m_end').innerHTML = `<b>本场结束</b>：${MOCK.list.length} 题 ｜ 不会 ${c[0]} · 想不起 ${c[1]} · 掌握 ${c[2]} · 牢固 ${c[3]}
    ${weak.length ? `<div class="mrow">薄弱题（已计入复习与错题本）：${weak.map(q => esc(q.id)).join('、')}</div>` : ''}
    <div class="mrow"><button class="mini" id="m_again">再来一场</button>
    <button class="mini" id="m_done">关闭</button></div>`;
  $('m_again').addEventListener('click', () =>
    MOCK.drill ? openDrill(MOCK.drill) : openMock());
  $('m_done').addEventListener('click', () => { $('mockov').style.display = 'none'; render(); });
}
// ---- 学习报告：自测覆盖 / 节奏 / 模块掌握度 / 错题本健康度 ----
function weekStart(ts){
  const d = new Date(ts); d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() - (d.getDay() + 6) % 7);   // 回到本周一 0 点
  return d.getTime();
}
const MODQ = {}; DATA.forEach(q => (MODQ[q.module] = MODQ[q.module] || []).push(q));
const QBY = {}; DATA.forEach(q => QBY[q.id] = q);
const isDue = r => r && r.g > 2 && (Date.now() - r.ts) >= REV_DAYS[r.g] * 864e5;

function renderRep(){
  const now = Date.now();
  const valid = new Set(DATA.map(q => q.id));
  const tested = Object.keys(review).filter(id => valid.has(id));
  const weakIds = tested.filter(id => review[id].g <= 2);
  const dueIds  = tested.filter(id => isDue(review[id]));
  const strongIds = tested.filter(id => review[id].g === 4);
  const cov = Math.round(tested.length / DATA.length * 100);
  $('r_gen').textContent = '生成于 ' + new Date(now).toLocaleString();

  // 总览卡：点卡跳对应筛选
  $('r_cards').innerHTML = `
    <div class="rcard ${cov >= 80 ? 'good' : ''}" data-act="none">
      <b>${tested.length}<small> / ${DATA.length}</small></b><small>已自测 · 覆盖 ${cov}%</small></div>
    <div class="rcard ${wrong.size ? 'warn' : ''}" data-act="wrong">
      <b>${wrong.size}</b><small>错题本</small></div>
    <div class="rcard ${dueIds.length ? 'warn' : ''}" data-act="due">
      <b>${dueIds.length}</b><small>今日该复习</small></div>
    <div class="rcard ${weakIds.length ? 'warn' : ''}" data-act="weak">
      <b>${weakIds.length}</b><small>薄弱（自评≤2）</small></div>
    <div class="rcard ${strongIds.length ? 'good' : ''}" data-act="none">
      <b>${strongIds.length}</b><small>牢固掌握（自评4）</small></div>`;

  // 近 8 周节奏：review 每题只存最新一次自评，按 ts 归周
  const ws0 = weekStart(now);
  const wk = [];
  for (let i = 7; i >= 0; --i) {
    const s = ws0 - i * 7 * 864e5;
    const c = tested.filter(id => { const t = review[id].ts; return t >= s && t < s + 7 * 864e5; }).length;
    wk.push([`${new Date(s).getMonth() + 1}/${new Date(s).getDate()}`, c]);
  }
  const mx = Math.max(1, ...wk.map(x => x[1]));
  $('r_weeks').innerHTML = wk.map(([l, c]) =>
    `<div class="rbar ${c ? '' : 'zero'}"><u>${c || ''}</u>` +
    `<i style="height:${Math.round(c / mx * 56)}px"></i><em>${l}</em></div>`).join('');

  // 模块掌握度：平均分升序，最弱排最前；从未自测的模块垫底
  const rows = Object.keys(MODQ).map(m => {
    const qs = MODQ[m];
    const done = qs.filter(q => review[q.id]);
    const avg = done.length ? done.reduce((a, q) => a + review[q.id].g, 0) / done.length : null;
    return { m, name: MODNAME[m] || m, total: qs.length, tested: done.length, avg,
      weak: done.filter(q => review[q.id].g <= 2).length,
      due: done.filter(q => isDue(review[q.id])).length };
  }).sort((a, b) => (a.avg == null ? 9 : a.avg) - (b.avg == null ? 9 : b.avg));
  $('r_mods').innerHTML = rows.map(r => {
    const pct = Math.round(r.tested / r.total * 100);
    const cls = r.avg == null ? '' : (r.avg >= 3.3 ? 'hi' : r.avg >= 2.5 ? 'mid' : 'lo');
    return `<tr data-mod="${esc(r.m)}">
      <td>${esc(r.name)}</td>
      <td class="rnum">${r.tested} / ${r.total}</td>
      <td><span class="rbar2"><i style="width:${pct}%"></i></span> <span class="rnum">${pct}%</span></td>
      <td><span class="rscore ${cls}">${r.avg == null ? '未测' : r.avg.toFixed(1)}</span></td>
      <td>${r.weak || '—'}</td><td>${r.due || '—'}</td></tr>`;
  }).join('');

  // 行动建议
  const adv = [];
  const pri0 = ids => ids.filter(id => QBY[id] && QBY[id].priority === 'P0').length;
  if (dueIds.length)
    adv.push(`今天有 <b>${dueIds.length}</b> 题到期复习（P0 ${pri0(dueIds)} 道），点下方「今日该复习」开始，约 ${Math.max(5, dueIds.length * 2)} 分钟`);
  if (weakIds.length)
    adv.push(`薄弱题 <b>${weakIds.length}</b> 道（P0 ${pri0(weakIds)}）：重口述一遍再自评 3 分以上，才能移出薄弱区`);
  const worst = rows.find(r => r.avg != null);
  if (worst && worst.avg < 3)
    adv.push(`最弱模块是 <b>${esc(worst.name)}</b>（平均 ${worst.avg.toFixed(1)}、薄弱 ${worst.weak} 道），面试前优先补它的 P0/P1`);
  if (cov < 60)
    adv.push(`还有 <b>${DATA.length - tested.length}</b> 道从未自测（覆盖 ${cov}%）：每天开一场 10 题模拟面试，一周可新增约 70 题覆盖`);
  const healed = [...wrong].filter(id => review[id] && review[id].g >= 3).length;
  if (healed >= 3)
    adv.push(`错题本里有 <b>${healed}</b> 道已自评 ≥3，点「清理错题本」移出，让它只装真不会的`);
  if (!adv.length)
    adv.push('状态良好：无到期、无薄弱。保持每天一场模拟面试的节奏即可。');
  $('r_adv').innerHTML = adv.map(x => `<li>${x}</li>`).join('');
}

// ---------------- 牛客宝典考点地图（sources/tutorial_map.json） ----------------
const EV_LABEL = {code: '代码', metric: '指标', test: '测试', doc: '文档'};

// 训练闭环：只看变化与复测，不看刷题量
function histById(){
  const m = {};
  hist.forEach(h => { (m[h.i] = m[h.i] || []).push(h); });
  Object.keys(m).forEach(k => m[k].sort((a, b) => a.t - b.t));
  return m;
}
function loopStats(){
  const now = Date.now(), D7 = 7 * 864e5;
  const avg = a => a.length ? a.reduce((x, h) => x + h.g, 0) / a.length : null;
  const recent = hist.filter(h => h.t >= now - D7);
  const prev = hist.filter(h => h.t >= now - 2 * D7 && h.t < now - D7);
  const a1 = avg(recent), a0 = avg(prev);
  const by = histById();
  const p0 = DATA.filter(q => q.priority === 'P0');
  const p0ok = p0.filter(q => review[q.id] && review[q.id].g >= 3).length;
  const twice = DATA.filter(q => {
    const hs = by[q.id] || [];
    if (hs.length < 2) return false;
    const [x, y] = hs.slice(-2);
    return x.g < 3 && y.g < 3;
  });
  let tests = 0, pass = 0;
  DATA.forEach(q => {
    const hs = by[q.id] || [];
    for (let i = 1; i < hs.length; i++) {
      if (hs[i].t - hs[i - 1].t >= D7) { tests++; if (hs[i].g >= 3) pass++; }
    }
  });
  const lowByMod = {};
  hist.filter(h => h.g <= 2).forEach(h => {
    const q = QBY[h.i]; if (q) lowByMod[q.module] = (lowByMod[q.module] || 0) + 1;
  });
  const hotMods = Object.entries(lowByMod).sort((a, b) => b[1] - a[1]).slice(0, 3);
  return {a0, a1, delta: (a1 != null && a0 != null) ? a1 - a0 : null,
    nRecent: recent.length, p0, p0ok, twice, tests, pass, hotMods};
}
function renderLoop(){
  const st = loopStats();
  const deltaTxt = st.delta == null ? '样本不足（需要两周记录）'
    : (st.delta >= 0.2 ? '↑ +' + st.delta.toFixed(2) : st.delta <= -0.2 ? '↓ ' + st.delta.toFixed(2) : '→ 持平');
  const dCls = st.delta == null ? 'mid' : st.delta >= 0.2 ? 'hi' : st.delta <= -0.2 ? 'lo' : 'mid';
  const rate = st.tests ? Math.round(st.pass / st.tests * 100) : null;
  const rows = [
    ['近 7 天均值', st.a1 == null ? '无记录' : st.a1.toFixed(2) + ' / 4',
      `前 7 天 ${st.a0 == null ? '—' : st.a0.toFixed(2)} · ${deltaTxt}`, dCls],
    ['P0 掌握率', st.p0ok + ' / ' + st.p0.length,
      Math.round(st.p0ok / Math.max(1, st.p0.length) * 100) + '%（自评 ≥3 算掌握）',
      st.p0ok / Math.max(1, st.p0.length) >= 0.6 ? 'hi' : 'mid'],
    ['连续两次低分', st.twice.length + ' 题',
      st.twice.length ? '同一题最近两次都 <3，属于「讲了还是不会」' : '没有反复卡住的题', st.twice.length ? 'lo' : 'hi'],
    ['跨 7 天复测', rate == null ? '还没有复测' : rate + '%',
      st.tests ? `${st.pass} / ${st.tests} 次复测仍 ≥3 分` : '隔 7 天再自评一次，才能验证长期掌握', rate == null ? 'mid' : rate >= 70 ? 'hi' : 'lo'],
  ];
  $('loop_meta').textContent = `近 7 天 ${st.nRecent} 次自评 · 历史 ${hist.length} 条`;
  $('loop_body').innerHTML = `<table class="rtable"><thead><tr>
      <th>指标</th><th>当前</th><th>说明</th></tr></thead><tbody>` +
    rows.map(r => `<tr><td><b>${r[0]}</b></td>
      <td><span class="rscore ${r[3]}">${esc(r[1])}</span></td>
      <td>${esc(r[2])}</td></tr>`).join('') +
    (st.hotMods.length ? `<tr><td><b>卡点模块</b></td><td>${st.hotMods.length} 个</td>
      <td>${st.hotMods.map(([m, n]) => esc(MODNAME[m] || m) + ' ' + n + ' 次低分').join('；')}</td></tr>` : '') +
    `</tbody></table>`;
}
function todayPlan(n){
  n = n || 12;
  const by = histById(), picked = [], seen = new Set();
  const add = q => { if (q && !seen.has(q.id) && picked.length < n) { seen.add(q.id); picked.push(q); } };
  const p0 = DATA.filter(q => q.priority === 'P0');
  p0.filter(q => revState(q) === 'due').forEach(add);
  p0.filter(q => !review[q.id]).forEach(add);
  DATA.filter(q => {
    const hs = by[q.id] || [];
    return hs.length >= 2 && hs[hs.length - 1].g < 3 && hs[hs.length - 2].g < 3;
  }).forEach(add);
  p0.filter(q => review[q.id] && review[q.id].g <= 2).forEach(add);
  DATA.filter(q => revState(q) === 'due').forEach(add);
  return picked.slice(0, n);
}
function renderProj(){
  const ps = PROJD.projects || [];
  if (!ps.length) { $('proj_meta').textContent = '未配置 companies/projects.json'; return; }
  const cnt = st => ps.filter(p => ((p.evidence || {}).code || {}).status === st).length;
  $('proj_meta').textContent = `${ps.length} 个项目 · 代码证据 完整 ${cnt('present')} / 部分 ${cnt('partial')} / 缺 ${cnt('missing')}`
    + ` · 仓库已登记 ${ps.filter(p => p.repo).length} 个`;
  $('proj_body').innerHTML = `<div class="tlist">` + ps.map(p => {
    const ev = p.evidence || {};
    const chips = Object.keys(EV_LABEL).map(k => {
      const v = ev[k] || {};
      const cls = v.status === 'present' ? 'ok' : v.status === 'partial' ? 'warn' : 'unknown';
      const txt = v.status === 'present' ? '有' : v.status === 'partial' ? '部分' : '缺';
      return `<span class="elc ${cls}" title="${esc(v.note || '')}">${EV_LABEL[k]} ${txt}</span>`;
    }).join('');
    return `<div class="tch w1">
      <div class="tch-top">
        <span class="tch-name">${esc(p.name)}</span>
        <span class="tag">${esc(p.tier || '')}</span>
        <span class="tch-em">${esc((p.stack || []).join(' / '))}</span>
        <span class="tch-w">${esc(p.repo ? '仓库已登记' : '仓库未登记')}</span>
      </div>
      <div class="tch-mid">
        ${chips}
        <span>项目深挖 <b>${p.interview_count || 0}</b> 题</span>
        <span class="tch-act">
          ${p.repo ? `<a class="mini" href="${esc(safeUrl(p.repo))}" target="_blank" rel="noopener">仓库 ↗</a>` : ''}
          <button class="mini" data-pdrill="${esc(p.sub || '')}">过题 ${p.interview_count || 0}</button>
        </span>
      </div>
      <div class="tsec">${(p.gaps || []).map(g => `<span class="schip zero">缺口 ${esc(g)}</span>`).join('') || '<span class="schip">无明显缺口</span>'}</div>
    </div>`;
  }).join('') + `</div>`;
}

function renderHealth(){
  const H = HEALTH;
  let bytes = 0, keys = 0;
  try {
    Object.keys(localStorage).forEach(k => {
      if (k.indexOf('ib_') === 0) { keys++; bytes += (localStorage.getItem(k) || '').length; }
    });
  } catch (e) { /* 隐私模式读不到就不显示体积 */ }
  const rows = (H.checks || []).slice();
  rows.push({name: '本地数据', status: bytes > 3.5e6 ? 'warn' : 'ok',
             detail: `${keys} 个键 · ${Math.round(bytes / 1024)} KB · 备份格式 v${SCHEMA_VERSION}`});
  rows.push({name: '你的自测', status: Object.keys(review).length ? 'ok' : 'warn',
             detail: `${Object.keys(review).length} 题已自测 · 错题 ${wrong.size} · 训练记录 ${hist.length} 条`});
  const bad = rows.filter(r => r.status === 'bad').length;
  const warn = rows.filter(r => r.status === 'warn').length;
  $('health_meta').textContent = `生成于 ${H.built_at} · ${bad ? bad + ' 项必须处理' : '无阻断项'} · ${warn} 项待观察`;
  $('health_body').innerHTML = `<table class="rtable"><thead><tr>
      <th>检查项</th><th>状态</th><th>明细</th></tr></thead><tbody>` +
    rows.map(r => `<tr><td>${esc(r.name)}</td>
      <td><span class="elc ${r.status}">${r.status === 'ok' ? '正常' : r.status === 'warn' ? '待观察' : '需处理'}</span></td>
      <td style="text-align:left">${esc(r.detail)}</td></tr>`).join('') + `</tbody></table>`;
}

function tutOf(id){ return (TUT.tutorials || []).find(t => t.id === id) || {}; }
function tutStat(ids){
  const arr = ids || [];
  const done = arr.filter(id => review[id]);
  const avg = done.length ? done.reduce((a, id) => a + review[id].g, 0) / done.length : null;
  return {n: arr.length, done: done.length, avg};
}
function tutBadge(s, tech){
  if (tech === false) return ['非技术章', 'na'];
  if (!s.n) return ['题库空', 'gap'];
  if (s.n < 5) return ['题库缺口', 'gap'];
  if (!s.done) return ['未自测', 'zero'];
  if (s.avg != null && s.avg < 2.5) return ['均分偏低', 'zero'];
  if (s.done / s.n >= 0.6) return ['已覆盖', 'ok'];
  return ['进行中', 'mid'];
}
// 加权准备度：Σ 权重×(0.4×自测覆盖 + 0.6×均分/4) ÷ Σ 权重，只算技术章
function tutScore(t){
  let w = 0, acc = 0;
  (t.chapters || []).forEach(ch => {
    if (!ch.weight) return;
    const s = tutStat(ch.ids);
    const cov = s.n ? Math.min(1, s.done / s.n) : 0;
    const avg = s.avg == null ? 0 : s.avg / 4;
    w += ch.weight;
    acc += ch.weight * (0.4 * cov + 0.6 * avg);
  });
  return w ? Math.round(acc / w * 100) : 0;
}
function tutDone(t){
  const s = new Set();
  (t.chapters || []).forEach(ch => (ch.ids || []).forEach(id => { if (review[id]) s.add(id); }));
  return s.size;
}
function renderTut(){
  const tabs = TUT.tutorials || [];
  if (!tabs.length) { $('tut_meta').textContent = '考点地图数据缺失（sources/tutorial_map.json）'; return; }
  const t = tutOf(tutTab) || tabs[0];
  $('tut_tabs').innerHTML = tabs.map(x =>
    `<button class="tchip ${x.id === t.id ? 'on' : ''}" data-tut="${x.id}">` +
    `${esc(x.short)} · ${x.articles} 篇 <b>${tutDone(x) ? tutScore(x) + '%' : '未开始'}</b></button>`).join('')
    + `<span class="mnote" style="margin:0">${esc(t.fit || '')}</span>`;

  // 各章有重叠（网络⊂操作系统、设计模式⊂C++基础），总量按题号去重
  const uni = new Set();
  (t.chapters || []).forEach(ch => (ch.ids || []).forEach(id => uni.add(id)));
  let done = 0;
  uni.forEach(id => { if (review[id]) done += 1; });
  const tot = uni.size;
  const score = tutScore(t);
  const gaps = (t.chapters || []).filter(ch => ch.weight && (ch.ids || []).length < 5).map(ch => ch.name);
  const noTest = (t.chapters || []).filter(ch => ch.weight && (ch.ids || []).length >= 5
    && !tutStat(ch.ids).done).map(ch => ch.name);

  $('tut_meta').textContent = `${t.title} · ${t.articles} 篇 · ${t.learners} 人学习`;
  $('tut_lead').innerHTML =
    (done
      ? `按这套目录加权，你的准备度是 <b>${score}%</b>（Σ 权重 ×（0.4×自测覆盖 + 0.6×均分/4）÷ Σ 权重，只算技术章）；`
      : `还没开始自测，所以准备度暂不算分（公式：Σ 权重 ×（0.4×自测覆盖 + 0.6×均分/4）÷ Σ 权重，只算技术章）；`)
    + `本书映射到题库 <b>${tot}</b> 题，已自测 <b>${done}</b> 题。<br>`
    + (gaps.length
        ? `⚠ <b>题库明显缺口</b>：${gaps.map(esc).join('、')}（题量 &lt; 5）—— 这几章别指望题库，直接读宝典 + 面经原文补。`
        : '✅ 题库对本书各章都有基础覆盖，重心转向自测与口述。')
    + (noTest.length
        ? `<br>🕳 <b>有题但一次没自测</b>：${noTest.map(esc).join('、')} —— 各抽 5 题口述一遍再自评，才知道真会不会。`
        : '');

  $('tut_body').innerHTML = `<div class="tlist">` + (t.chapters || []).map(ch => {
    const s = tutStat(ch.ids);
    const [bt, bc] = tutBadge(s, ch.tech);
    const pct = s.n ? Math.round(s.done / s.n * 100) : 0;
    const stars = ch.weight ? '★'.repeat(ch.weight) + '☆'.repeat(3 - ch.weight) : '—';
    const secs = (ch.sections || []).map(sec => {
      const has = sec.ids && sec.ids.length;
      const attr = has ? ` data-tids="${sec.ids.join(',')}" data-tname="${esc(ch.name + ' · ' + sec.n)}"`
                       : '';
      const cnt = sec.ids ? ` <b>${sec.ids.length}</b>` : '';
      const zc = (sec.ids && !sec.ids.length) ? ' zero' : '';
      return `<span class="schip${zc}"${attr} title="${has ? '点这一节筛出这 ' + sec.ids.length + ' 题'
        : (sec.ids === null ? '这一节暂无可映射题号' : '这一节题库没有对应题')}">${esc(sec.n)}${cnt}</span>`;
    }).join('');
    const act = (s.n ? `<button class="mini" data-tids="${ch.ids.join(',')}" `
      + `data-tname="${esc(ch.name)}">练这一章 ${s.n} 题</button>` : '')
      + (ch.name === '项目相关' ? '<button class="mini" data-drill="1">项目连环问</button>' : '');
    return `<div class="tch w${ch.weight || 0}${ch.tech === false ? ' na' : ''}">
      <div class="tch-top">
        <span class="tch-no">${esc(ch.no)}</span>
        <span class="tch-name">${esc(ch.name)}</span>
        <span class="tch-em">${esc(ch.emphasis || '')}</span>
        <span class="tch-w" title="按原文强调程度标注，非官方分值">${stars}</span>
      </div>
      ${ch.tech === false ? '' : `<div class="tch-mid">
        <span class="tbadge ${bc}">${bt}</span>
        <span>题库 <b>${s.n}</b> 题${ch.weak ? `（P0 ${ch.weak}）` : ''}</span>
        <span>已自测 <b>${s.done}</b></span>
        <span class="rbar2"><i style="width:${pct}%"></i></span>
        <span>均分 <b>${s.avg == null ? '未测' : s.avg.toFixed(1)}</b></span>
        <span class="tch-act">${act}<a class="mini" href="${esc(t.url)}" target="_blank"
          rel="noopener">读宝典 ↗</a></span>
      </div>`}
      <div class="tsec">${secs}</div>
    </div>`;
  }).join('') + `</div>`;

  $('tut_practice').innerHTML = (TUT.practice || []).map(p =>
    `<a class="chip" href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.label)} <b>${esc(p.n)}</b> ↗</a>`).join('');
}
function tutOpen(ids, label){
  if (!ids || !ids.length) return;
  tutFilter = {ids: new Set(ids), label: label || '宝典章节', kind: 'tut'};
  ['q', 'co', 'rl', 'prof', 'mod', 'sub', 'pri', 'st', 'rev', 'dif'].forEach(k => {
    const el = $(k); if (el) el.value = '';
  });
  if ($('wrong')) $('wrong').checked = false;
  if ($('hidepred')) $('hidepred').checked = false;
  document.querySelectorAll('#chips .chip').forEach(c =>
    c.classList.toggle('on', c.dataset.c === 'all'));
  showView('bank'); render(); window.scrollTo(0, 0);
}
$('loop_drill').addEventListener('click', () => {
  const list = todayPlan(12);
  if (!list.length) { alert('题库里没有需要补的题：要么已全部掌握，要么还没自测记录。'); return; }
  tutFilter = {ids: new Set(list.map(q => q.id)), label: `${list.length} 题`, kind: 'today'};
  showView('bank'); render(); window.scrollTo(0, 0);
});

document.addEventListener('click', e => {
  const b = e.target.closest('[data-pdrill]'); if (!b) return;
  showView('train');
  const h = [...document.querySelectorAll('#view-train h3')].find(x => x.innerText.includes('项目连环问'));
  if (h) h.scrollIntoView({block: 'start'});
});

$('tut_tabs').addEventListener('click', e => {
  const b = e.target.closest('[data-tut]'); if (!b) return;
  tutTab = +b.dataset.tut; renderTut();
});
$('tut_body').addEventListener('click', e => {
  if (e.target.closest('[data-drill]')) {
    showView('train');
    const h = [...document.querySelectorAll('#view-train h3')]
      .find(x => x.innerText.includes('项目连环问'));
    if (h) h.scrollIntoView({block: 'start'});
    return;
  }
  const el = e.target.closest('[data-tids]'); if (!el) return;
  tutOpen(el.dataset.tids.split(',').filter(Boolean), el.dataset.tname || '宝典章节');
});
$('tutbanner').addEventListener('click', e => {
  if (!e.target.closest('#tutclear')) return;
  tutFilter = null; render();
});
$('rep').addEventListener('click', () => showView('rep'));
$('rep_tut').addEventListener('click', () => {
  showView('rep'); renderTut();
  const el = $('tutbox'); if (el) el.scrollIntoView({block: 'start'});
});
$('r_cards').addEventListener('click', e => {
  const c = e.target.closest('.rcard'); if (!c) return;
  const act = c.dataset.act;
  if (act === 'wrong') $('wrong').checked = true;
  else if (act === 'due' || act === 'weak') $('rev').value = act;
  else return;
  showView('bank'); render();
});
$('r_mods').addEventListener('click', e => {
  const tr = e.target.closest('tr[data-mod]'); if (!tr) return;
  $('mod').value = tr.dataset.mod; refreshSubs();
  showView('bank'); render();
});
$('r_due').addEventListener('click', () => {
  $('rev').value = 'due'; showView('bank'); render();
});
$('r_weak').addEventListener('click', () => {
  $('rev').value = 'weak'; showView('bank'); render();
});
$('r_clean').addEventListener('click', () => {
  const healed = [...wrong].filter(id => review[id] && review[id].g >= 3);
  if (!healed.length) { alert('错题本没有「自评≥3」的题，无需清理'); return; }
  if (!confirm(`把 ${healed.length} 道已自评 ≥3 的题移出错题本？\n（只影响错题标记，复习计划保留）`)) return;
  healed.forEach(id => wrong.delete(id));
  localStorage.setItem(WRONG_KEY, JSON.stringify([...wrong]));
  renderRep();
});

// ---- 四视图导航：首页 / 题库 / 训练 / 分析 ----
document.querySelectorAll('.tab').forEach(t =>
  t.addEventListener('click', () => showView(t.dataset.v)));
function showView(v){
  document.querySelectorAll('.view').forEach(s =>
    s.classList.toggle('on', s.id === 'view-' + v));
  document.querySelectorAll('.tab').forEach(t =>
    t.classList.toggle('on', t.dataset.v === v));
  if (v === 'home') renderHome();
  if (v === 'train') renderTrain();
  if (v === 'jobs') { renderJobs(); renderRadar(); }
  if (v === 'comp') renderCompanies();
  if (v === 'rep') { renderRep(); renderTut(); renderLoop(); renderProj(); renderHealth(); }
  try { history.replaceState(null, '', '#' + v); } catch {}
}

// ---- 首页：数据卡 + 快速开始 + 今日任务 + 岗位进度 + 最近记录 ----
const ACT_LABEL = {due: '今日复习', weak: '薄弱补强', mock: '模拟面试', drill: '项目连环问'};
function runAct(act){
  if (act === 'due') { $('rev').value = 'due'; showView('bank'); render(); }
  else if (act === 'weak') { $('rev').value = 'weak'; showView('bank'); render(); }
  else if (act === 'mock') { showView('bank'); openMock(); }
  else if (act === 'drill') showView('train');
  else if (act === 'comp') { showView('comp'); window.scrollTo(0, 0); }
}
function renderHome(){
  const d = new Date();
  const wk = '日一二三四五六'[d.getDay()];
  $('h_date').textContent = `${d.getFullYear()}.${d.getMonth() + 1}.${d.getDate()} · 周${wk} · 数据都在本机浏览器，换设备先备份`;
  const srcs = RADAR.sources || [];
  const okN = srcs.filter(x => x.status === 'success').length;
  const all = RADAR.jobs || [];
  // 三段拆分：可关注（届别匹配/未标注/实习）· 技能参考（届别不符但方向相关）· 待核实（suspect/届别未知）
  let canGo = 0, refN = 0, suspectN = 0;
  all.forEach(j => {
    if (j.status === 'suspect') { suspectN++; return; }
    const gy = j.grad_year;
    if (gy && gy !== USER_GRAD && !(j.type || '').includes('实习')) refN++;
    else canGo++;
  });
  const ps = RADAR.pool_stats || {};
  const openN = all.filter(x => x.status === 'open').length;
  const targetN = all.filter(x => x.status === 'open' && (x.families || []).some(f => f !== '其他')).length;
  const csx = RADAR.class_stats || {}, bsx = RADAR.class_basis_stats || {};
  const clsLine = `招聘性质：<b>校招 ${csx['校招'] || 0}</b> · <b>实习 ${csx['实习'] || 0}</b> · 社招 ${csx['社招'] || 0} · 未标明 ${csx['未标明'] || 0} · 入口推定待核实 ${bsx['校园招聘入口推定'] || 0}<br>` +
    `<button class="mini" id="h_allco">🏢 查看全部 ${allCompanies().length} 家公司 / 全部 ${all.length} 岗（按校招 · 实习分类）→</button>`;
  $('h_radar').innerHTML = srcs.length
    ? `🛰 岗位雷达：<b>${srcs.length}</b> 个官方源（成功 ${okN}）· 最近实际扫描 <b>${esc((RADAR.updated || '—').replace('T', ' ').slice(0, 16))}</b> · 官方在招 <b>${openN}</b>（可关注 ${canGo} · 技能参考 ${refN} · 待核实 ${suspectN}）· 目标方向命中 <b>${targetN}</b> · 目标届别 <b>${USER_GRAD} 届</b><br>` +
      `公司池 <b>${ps.pool_total || '—'}</b> 家（启用 ${ps.enabled || 0} · 本次成功 ${ps.scanned_ok || 0} · ATS：${Object.entries(ps.ats_dist || {}).map(([k, v]) => k + ' ' + v).join('、') || '—'}）· 岗位族：${Object.entries(RADAR.family_stats || {}).sort((a, b) => b[1] - a[1]).slice(0, 4).map(([k, v]) => `${k} ${v}`).join(' · ')}<br>` +
      clsLine
    : '🛰 岗位雷达尚未运行（GitHub Actions 每日 09:30 自动扫描官方招聘门户）';
  // 首页：最近真实面经（3 条）+ 全部入口
  const exps = (NC.experiences || []).slice()
    .sort((a, b) => (b.collected_at || '').localeCompare(a.collected_at || ''));
  $('h_nc').innerHTML =
    `<div class="rsec" style="margin:0 0 6px">📰 真实面经（牛客同步 · 共 ${exps.length} 篇 / 有题号关联 ${exps.filter(x => (x.highlights || []).some(h => h.ref)).length} 篇）</div>` +
    exps.slice(0, 3).map(x => `<div class="hitem">
      <span class="pid">${esc(x.company)}</span>
      <b title="${esc(x.title)}">${esc(x.title)}</b>
      <span class="rnum">${x.n_questions || 0} 题</span>
      ${safeUrl(x.url) ? `<a class="tag jlink" href="${esc(safeUrl(x.url))}" target="_blank" rel="noopener">原帖 ↗</a>` : '—'}
    </div>`).join('') +
    `<div class="mrow" style="margin-top:8px"><button class="mini" id="h_nc_more">查看全部面经 / 按公司筛选 →</button></div>`;
  renderScards();
  $('h_quick').innerHTML = `
    <div class="qcard" data-a="due"><b>📋 今日复习</b><small>处理间隔复习到期的题目</small></div>
    <div class="qcard" data-a="drill"><b>🎯 岗位专项训练</b><small>按真实 JD 模板选题训练</small></div>
    <div class="qcard" data-a="mock"><b>🎤 模拟面试</b><small>连续答题、追问揭示、训练总结</small></div>
    <div class="qcard" data-a="tut"><b>📚 宝典考点地图</b><small>牛客 C++ / 算法两套宝典 × 题库覆盖与缺口</small></div>
    <div class="qcard" data-a="bank"><b>📚 全部题库</b><small>搜索与筛选全部 ${DATA.length} 题</small></div>`;
  // 今日任务：need 为今日目标量，done 从训练历史统计
  const t0 = new Date(); t0.setHours(0, 0, 0, 0);
  const today = hist.filter(h => h.t >= t0.getTime());
  const dueIds = DATA.filter(q => revState(q) === 'due').map(q => q.id);
  const weakIds = DATA.filter(q => revState(q) === 'weak').map(q => q.id);
  const dueSet = new Set(dueIds), weakSet = new Set(weakIds);
  const projIds = new Set(DATA.filter(q => q.module === '01_project').map(q => q.id));
  const mockIds = new Set(today.filter(h => h.m).map(h => h.i));
  const projToday = new Set(today.filter(h => projIds.has(h.i)).map(h => h.i));
  const tasks = [
    { act: 'due', need: dueIds.length, done: today.filter(h => dueSet.has(h.i)).length,
      note: dueIds.length ? `${dueIds.length} 道到期（P0 ${dueIds.filter(id => QBY[id].priority === 'P0').length}）` : '今日无到期，保持节奏' },
    { act: 'weak', need: Math.min(weakIds.length, 8), done: today.filter(h => weakSet.has(h.i)).length,
      note: weakIds.length ? `${weakIds.length} 道薄弱，先攻 8 道` : '没有薄弱题' },
    { act: 'mock', need: 8, done: mockIds.size, note: '一场 10 题 · 自评 8 题算完成' },
    { act: 'drill', need: 3, done: projToday.size, note: '项目题顺序过 3 道算打卡' },
  ];
  $('h_tasks').innerHTML = tasks.map(t => {
    const st = t.need === 0 ? 'done' : t.done >= t.need ? 'done' : t.done > 0 ? 'doing' : 'todo';
    const stTxt = st === 'done' ? '已完成' : st === 'doing' ? `进行中 ${t.done}/${t.need}` : t.need === 0 ? '无任务' : '待开始';
    return `<div class="titem" data-a="${t.act}">
      <b>${ACT_LABEL[t.act]}</b><span class="tnote">${t.note}</span>
      <span class="tstat ${st}">${stTxt}</span></div>`;
  }).join('');
  // 岗位训练进度：对口 = 模板有权重的模块 + 通用门槛（算法机考）
  $('h_profs').innerHTML = PROFILES.map(p => {
    const pool = DATA.filter(q => (p.weights[q.module] || 0) > 0 || ALWAYS.has(q.module));
    const done = pool.filter(q => review[q.id]);
    const cov = pool.length ? Math.round(done.length / pool.length * 100) : 0;
    const mas = done.length ? Math.round(done.filter(q => review[q.id].g >= 3).length / done.length * 100) : 0;
    return `<div class="prow" data-p="${esc(p.id)}">
      <b>${esc(p.name)}</b>
      <div class="pbarw"><span>覆盖</span><span class="pbar"><i style="width:${cov}%"></i></span><span class="rnum">${cov}% · 对口 ${pool.length} 题</span></div>
      <div class="pbarw"><span>掌握</span><span class="pbar mas"><i style="width:${mas}%"></i></span><span class="rnum">${mas}%（自评≥3）</span></div>
    </div>`;
  }).join('');
  // 最近训练记录：有 hist 用 hist，没有就用 review 最新时间兜底
  let items;
  if (hist.length) {
    items = hist.slice(-6).reverse().map(h => {
      const q = QBY[h.i]; if (!q) return '';
      const d2 = new Date(h.t);
      const sameDay = d2.toDateString() === new Date().toDateString();
      const when = sameDay ? `${String(d2.getHours()).padStart(2, '0')}:${String(d2.getMinutes()).padStart(2, '0')}`
        : `${d2.getMonth() + 1}/${d2.getDate()}`;
      const cls = h.g === 4 ? 'm4' : h.g === 3 ? 'm3' : 'm12';
      const tag = h.m ? ' · 模拟面试' : '';
      return `<div class="hitem"><span class="pid">${q.id}</span><b title="${esc(q.title)}">${esc(q.title)}</b>
        <span class="rscore ${cls}">自评 ${h.g}</span><span class="rnum">${when}${tag}</span></div>`;
    });
  } else {
    const recent = Object.keys(review).filter(id => QBY[id])
      .sort((a, b) => review[b].ts - review[a].ts).slice(0, 6);
    items = recent.length
      ? recent.map(id => {
          const q = QBY[id], r = review[id], d2 = new Date(r.ts);
          const cls = r.g === 4 ? 'm4' : r.g === 3 ? 'm3' : 'm12';
          return `<div class="hitem"><span class="pid">${q.id}</span><b title="${esc(q.title)}">${esc(q.title)}</b>
            <span class="rscore ${cls}">自评 ${r.g}</span><span class="rnum">${d2.getMonth() + 1}/${d2.getDate()}</span></div>`;
        })
      : ['<div class="hempty">还没有训练记录。去题库页给题目打自评分，或开一场模拟面试，这里会开始积累。</div>'];
    if (recent.length) items.push('<div class="hempty" style="margin-top:6px">（升级前只有每题最新一次自评；从现在起每次训练都会留痕）</div>');
  }
  $('h_hist').innerHTML = items.join('');
}
$('h_quick').addEventListener('click', e => {
  const c = e.target.closest('.qcard'); if (!c) return;
  const a = c.dataset.a;
  if (a === 'bank') { showView('bank'); window.scrollTo(0, 0); }
  else if (a === 'tut') {
    showView('rep'); renderTut();
    const el = $('tutbox'); if (el) el.scrollIntoView({block: 'start'});
  }
  else runAct(a);
});
$('h_tasks').addEventListener('click', e => {
  const c = e.target.closest('.titem'); if (!c) return;
  runAct(c.dataset.a);
});
$('h_profs').addEventListener('click', e => {
  const c = e.target.closest('.prow'); if (!c) return;
  $('prof').value = c.dataset.p;
  showView('bank'); window.scrollTo(0, 0); render();
});

// ---- 训练视图：入口 + 项目连环问列表 ----
function renderTrain(){
  const subs = Object.keys(PROJ).sort((a, b) => PROJ[b].length - PROJ[a].length);
  $('tr_projects').innerHTML = subs.map(s => {
    const qs = PROJ[s];
    const done = qs.filter(q => review[q.id]).length;
    const pct = Math.round(done / qs.length * 100);
    return `<div class="trcard" data-s="${esc(s)}">
      <b>${esc(s)}</b><small>${qs.length} 题 · 已自测 ${done}</small>
      <span class="pbar"><i style="width:${pct}%"></i></span>
    </div>`;
  }).join('');
}
$('tr_projects').addEventListener('click', e => {
  const c = e.target.closest('.trcard'); if (!c) return;
  openDrill(c.dataset.s);
});
$('tr_mock').addEventListener('click', () => { showView('bank'); openMock(); });
$('tr_due').addEventListener('click', () => runAct('due'));
$('tr_weak').addEventListener('click', () => runAct('weak'));
$('tr_wrong').addEventListener('click', () => {
  $('wrong').checked = true; showView('bank'); render();
});

// ---- 岗位视图：收藏 + JD 技能匹配分析（规则版，JD → 题库缺口联动） ----
const LOCAL_JOBS_KEY = 'ib_jobs_v1';
function loadJobs(){
  let local = [];
  try { local = JSON.parse(localStorage.getItem(LOCAL_JOBS_KEY) || '[]'); } catch {}
  return JOBS_SEED.concat(local);
}
// 技能规则表：JD 关键词 → 题库模块。匹配分析的核心映射，随题库方向扩展
const SKILLS = [
  {name: 'C++', tier: 'core', kws: ['c++', 'c/c++', 'stl', '多线程', '内存管理', '智能指针', '模板', 'cmake', '编译', '链接', 'abi', '跨平台'], mods: ['02_cpp']},
  {name: 'Linux', tier: 'core', kws: ['linux', 'shell', 'gdb', 'makefile', '系统编程', '进程', 'epoll'], mods: ['03_linux']},
  {name: '算法机考', tier: 'eng', kws: ['算法', '数据结构', '手撕', '机考', '编程题'], mods: ['04_algo']},
  {name: '模型部署', tier: 'core', kws: ['tensorrt', 'onnx', '推理', '部署', '量化', 'cuda', '边缘计算', '性能优化', 'fp16', 'int8'], mods: ['05_deploy']},
  {name: 'ROS2/中间件', tier: 'core', kws: ['ros2', 'ros', 'dds', '中间件', 'ethercat', 'can总线', '串口', '通信'], mods: ['06_ros2']},
  {name: '深度学习/感知', tier: 'domain', kws: ['pytorch', '目标检测', '分割', 'yolo', 'opencv', '感知', '融合', '深度学习', '视觉'], mods: ['10_cv_pytorch', '07_imaging']},
  {name: 'Python', tier: 'eng', kws: ['python'], mods: ['11_python']},
  {name: '硬件/嵌入式', tier: 'core', kws: ['单片机', 'uart', 'spi', 'i2c', '嵌入式', 'fpga', 'mcu', 'rtos', '原理图'], mods: ['09_hardware']},
  {name: '机器人学', tier: 'domain', kws: ['运动学', '动力学', 'slam', '轨迹规划', '标定', '机械臂'], mods: ['08_robot']},
  {name: '数据库/缓存', tier: 'eng', kws: ['mysql', '数据库', 'sql', 'redis', '缓存', '索引', '事务', 'mvcc', '消息队列', 'kafka', 'rabbitmq'], mods: ['12_backend']},
  {name: '工业通信/现场总线', tier: 'eng', kws: ['profinet', 'mrp', 'plc', 'modbus', 'canopen', '现场总线', '工业以太网', 'opc ua'], mods: ['06_ros2', '09_hardware']},
];
const TIER_LABEL = {core: '核心', eng: '工程', domain: '场景'};
const TARGET_FAMS = ['AI推理部署', '机器人软件/ROS2', 'C++ SDK/系统软件', 'VLM/VLA/视觉算法', '嵌入式/控制'];

// 取 JD 里第一处命中词的前后原文，作为「为什么判它命中」的证据
function jdSnippet(jd, kws){
  const t = jd || '';
  if (!t) return '';
  const low = t.toLowerCase();
  let best = -1, hit = '';
  kws.forEach(k => {
    const i = low.indexOf(k.toLowerCase());
    if (i >= 0 && (best < 0 || i < best)) { best = i; hit = k; }
  });
  if (best < 0) return '';
  const a = Math.max(0, best - 30), b = Math.min(t.length, best + hit.length + 42);
  return (a > 0 ? '…' : '') + t.slice(a, b).replace(/\s+/g, ' ').trim() + (b < t.length ? '…' : '');
}

// 只产出「命中事实」，不再算总分：无自评就是 null，不拿 50 分充数
function jobScore(job){
  const jd = job.jd || '';
  const text = (jd + ' ' + (job.skills || []).join(' ')).toLowerCase();
  const hits = [];
  SKILLS.forEach(s => {
    const kws = s.kws.filter(k => text.includes(k));
    if (!kws.length) return;
    const pool = [];
    s.mods.forEach(m => (MODQ[m] || []).forEach(q => pool.push(q)));
    const done = pool.filter(q => review[q.id]);
    const avg = done.length ? done.reduce((a, q) => a + review[q.id].g, 0) / done.length : null;
    hits.push({name: s.name, tier: s.tier, kws, mods: s.mods, snip: jdSnippet(jd, kws),
      pool: pool.length, done: done.length,
      cov: pool.length ? Math.round(done.length / pool.length * 100) : 0, avg});
  });
  return hits;
}

// 招聘资格：多字段独立判断；抽不到的字段一律「未说明」，不算符合
const USER_INFO = {grad: 2029, degree: '硕士'};
const USER_GRAD = USER_INFO.grad;          // 兼容旧引用

function eligibilityOf(job){
  const r = job.req || {};
  const gr = (r.grad_range && r.grad_range.length) ? r.grad_range
           : (job.grad_year ? [job.grad_year, job.grad_year] : null);
  const fields = [], bad = [], unknown = [];
  if (r.education){
    const needDoc = r.education.indexOf('博士') === 0;
    fields.push(['学历要求', r.education, needDoc ? 'bad' : 'ok']);
    if (needDoc) bad.push(`要求${r.education}（你是${USER_INFO.degree}）`);
  } else { fields.push(['学历要求', '未说明', 'unknown']); unknown.push('学历'); }
  if (gr){
    const ok = gr[0] <= USER_INFO.grad && USER_INFO.grad <= gr[1];
    const txt = gr[0] === gr[1] ? gr[0] + ' 届' : gr[0] + '–' + gr[1] + ' 届';
    fields.push(['毕业届别', txt, ok ? 'ok' : 'bad']);
    if (!ok) bad.push(`限 ${txt}（你是 ${USER_INFO.grad} 届）`);
  } else { fields.push(['毕业届别', '未说明', 'unknown']); unknown.push('届别'); }
  if (r.student_status){
    fields.push(['在校身份', r.student_status, r.student_status === '在校生' ? 'warn' : 'ok']);
    if (r.student_status === '在校生') unknown.push('在校/注册证明');
  } else { fields.push(['在校身份', '未说明', 'unknown']); unknown.push('在校身份'); }
  if (r.intern_duration){
    fields.push(['实习时长', '≥ ' + r.intern_duration + ' 个月', 'warn']);
    unknown.push('可投入时长');
  } else fields.push(['实习时长', '未说明', 'unknown']);
  if (r.weekly_days){
    fields.push(['每周到岗', r.weekly_days + ' 天', 'warn']);
    unknown.push('每周可到岗');
  } else fields.push(['每周到岗', '未说明', 'unknown']);

  if (bad.length) return {cls: 'lo', txt: '不符合', fields, bad, unknown};
  const keyUnknown = unknown.filter(x => x === '学历' || x === '届别');
  if (keyUnknown.length) return {cls: 'mid', txt: '资格未说明', fields, bad: [], unknown};
  if (unknown.length) return {cls: 'mid', txt: '待确认 ' + unknown.length + ' 项', fields, bad: [], unknown};
  return {cls: 'hi', txt: '条件齐备', fields, bad: [], unknown: []};
}

// 岗位适配度：相关度 / 知识覆盖 / 理论掌握 / 工程证据 / 招聘资格 —— 五个维度独立，不合成单一百分比
function jobMatch(job){
  const hits = jobScore(job);
  const core = hits.filter(h => h.tier === 'core').length;
  const eng = hits.filter(h => h.tier === 'eng').length;
  const fams = (job.families || []).filter(f => TARGET_FAMS.indexOf(f) >= 0);
  let relevance;
  if (core >= 2) relevance = {lvl: '高相关', cls: 'hi', why: `命中 ${core} 项核心技能` + (fams.length ? '，方向属 ' + fams.join('/') : '')};
  else if (core === 1 && (eng >= 1 || fams.length)) relevance = {lvl: '中相关', cls: 'mid', why: `1 项核心 + ${eng} 项工程技能`};
  else if (core === 1) relevance = {lvl: '弱相关', cls: 'mid', why: '仅 1 项核心技能，工程侧证据少'};
  else if (eng >= 2) relevance = {lvl: '弱相关', cls: 'mid', why: '只命中工程技能，未命中核心技术栈'};
  else relevance = {lvl: '不相关', cls: 'lo', why: '未命中核心技术栈'};

  const cover = hits.length ? Math.round(hits.filter(h => h.pool > 0).length / hits.length * 100) : 0;
  const tested = hits.filter(h => h.avg != null);
  const mastery = tested.length
    ? {pct: Math.round(tested.reduce((a, h) => a + h.avg, 0) / tested.length / 4 * 100),
       txt: (tested.reduce((a, h) => a + h.avg, 0) / tested.length).toFixed(1)}
    : {pct: null, txt: '数据不足'};

  const evRows = hits.map(h => {
    const ps = (PROJD.projects || []).filter(p => (p.stack || []).indexOf(h.name) >= 0);
    const codeOk = ps.some(p => ['present', 'partial'].indexOf(((p.evidence || {}).code || {}).status) >= 0);
    return {name: h.name, projects: ps.map(p => p.name), codeOk};
  });
  const evidence = {rows: evRows, covered: evRows.filter(r => r.codeOk).length, total: hits.length};

  hits.forEach((h, i) => {
    const ev = evRows[i];
    if (ev.codeOk) h.state = ['项目证据', 'done'];
    else if (ev.projects.length) h.state = ['项目提到·证据待补', 'doing'];
    else if (h.done > 0) h.state = ['仅自测·无项目', 'doing'];
    else if (h.pool > 0) h.state = ['仅题库储备', 'todo'];
    else h.state = ['尚无证据', 'todo'];
    h.projects = ev.projects;
  });

  const gaps = [];
  hits.forEach(h => {
    if (!h.pool && !h.projects.length) gaps.push(`${h.name}：题库与项目都没有`);
    else if (h.avg != null && h.avg < 2.5) gaps.push(`${h.name}：自测均分 ${h.avg.toFixed(1)}，需重练`);
    else if (!h.projects.length) gaps.push(`${h.name}：缺项目证据`);
  });
  return {hits, relevance, cover, mastery, evidence, eligibility: eligibilityOf(job), gaps};
}
function masteryCls(m){ return m.pct == null ? 'mid' : m.pct >= 80 ? 'hi' : m.pct >= 60 ? 'mid' : 'lo'; }
let jobFilter = {scope: 'tech', rel: 'all', decide: 'all'};
let radarLimit = 18;
const DECIDE_ORDER = ['apply', 'watch', 'ref', 'no'];
const DECIDE_META = {
  apply: ['优先投递', '高相关 + 有证据或掌握≥3', 'hi'],
  watch: ['持续关注', '相关，但资格或证据待补', 'mid'],
  ref: ['仅供学习', '弱相关 / 不在五大目标方向', 'lo'],
  no: ['不符合', '届别/学历硬性冲突', 'lo'],
};

// 决策规则：资格先出局 → 相关度 → 证据/掌握。顺序固定，避免「总分高但根本不能投」
function decideOf(job, m){
  if (m.eligibility.cls === 'lo')
    return {k: 'no', label: '不符合', cls: 'lo', why: m.eligibility.bad[0] || '硬性条件不符'};
  const fams = (job.families || []).filter(f => TARGET_FAMS.indexOf(f) >= 0);
  const strong = m.relevance.lvl === '高相关' &&
    (m.evidence.covered >= 1 || (m.mastery.pct != null && m.mastery.pct >= 60));
  if (strong && fams.length)
    return {k: 'apply', label: '优先投递', cls: 'hi',
      why: '高相关 + ' + (m.evidence.covered ? `有 ${m.evidence.covered} 项工程证据` : `掌握 ${m.mastery.txt}/4`)};
  if (m.relevance.lvl === '高相关' || (m.relevance.lvl === '中相关' && fams.length))
    return {k: 'watch', label: '持续关注', cls: 'mid',
      why: m.eligibility.cls === 'mid' ? '资格待确认，先核实 JD' : '相关，但证据或掌握不足'};
  return {k: 'ref', label: '仅供学习', cls: 'lo', why: '弱相关或不在五大目标方向'};
}

// 五大岗位族：市场供给（雷达）vs 我的准备（题库覆盖/自评），按自评数量缓存
let famCache = {key: -1, rows: []};
function famStats(){
  const key = Object.keys(review).length;
  if (famCache.key === key) return famCache.rows;
  const jobs = (RADAR.jobs || []).filter(j => j.tech_relevant !== false);
  const rows = TARGET_FAMS.map(f => {
    const js = jobs.filter(j => (j.families || []).indexOf(f) >= 0);
    const ms = js.map(j => jobMatch(j));
    const high = ms.filter(m => m.relevance.lvl === '高相关').length;
    const cov = ms.length ? Math.round(ms.reduce((a, m) => a + m.cover, 0) / ms.length) : 0;
    const tested = ms.filter(m => m.mastery.pct != null);
    const mastery = tested.length
      ? (tested.reduce((a, m) => a + m.mastery.pct, 0) / tested.length / 25).toFixed(1) : null;
    return {f, n: js.length, high, cov, mastery};
  });
  famCache = {key, rows};
  return rows;
}

function renderDecide(){
  const jobs = loadJobs();
  const cnt = {apply: 0, watch: 0, ref: 0, no: 0};
  jobs.forEach(j => { cnt[decideOf(j, jobMatch(j)).k] += 1; });
  $('decide_cards').innerHTML = DECIDE_ORDER.map(k =>
    `<div class="scard ${jobFilter.decide === k ? 'on' : ''}" data-decide="${k}" title="${DECIDE_META[k][1]}">
      <b>${cnt[k]}</b><small>${DECIDE_META[k][0]}</small><em>${DECIDE_META[k][1]}</em></div>`).join('');
  $('decide_meta').textContent = `已收藏 ${jobs.length} 岗 · 点卡片筛下方列表`;
  const rows = famStats();
  const total = rows.reduce((a, r) => a + r.n, 0) || 1;
  $('decide_fams').innerHTML = `<div class="rsec">五大岗位族 · 市场供给 vs 我的准备（雷达 ${(RADAR.jobs || []).filter(j => j.tech_relevant !== false).length} 个技术岗）</div>
    <table class="rtable"><thead><tr>
      <th>岗位族</th><th>在招</th><th>高相关</th><th>我的知识覆盖</th><th>我的掌握</th><th>判断</th>
    </tr></thead><tbody>` + rows.map(r => {
      const share = Math.round(r.n / total * 100);
      const advice = r.mastery == null ? '还没自测，覆盖再高也不算会'
        : (Number(r.mastery) < 2.5 ? '掌握偏低，优先补'
          : (r.high >= 30 ? '供给多且能对上，主投' : '能对上，但岗位偏少'));
      return `<tr><td><b>${esc(r.f)}</b></td>
        <td class="rnum">${r.n} <small>(${share}%)</small></td>
        <td class="rnum">${r.high}</td>
        <td><span class="rbar2"><i style="width:${r.cov}%"></i></span> <span class="rnum">${r.cov}%</span></td>
        <td>${r.mastery == null ? '<span class="muted">数据不足</span>' : r.mastery + '/4'}</td>
        <td>${advice}</td></tr>`;
    }).join('') + `</tbody></table>`;
}

function renderJobs(){
  renderDecide();
  const all = loadJobs();
  const scoped = all.filter(j => jobFilter.scope === 'all' || j.tech_relevant !== false);
  const jobs = scoped.filter(j => {
    if (jobFilter.decide !== 'all' && decideOf(j, jobMatch(j)).k !== jobFilter.decide) return false;
    if (jobFilter.rel === 'all') return true;
    const m = jobMatch(j);
    if (jobFilter.rel === 'high') return m.relevance.lvl === '高相关';
    if (jobFilter.rel === 'gap') return m.gaps.length > 0 || m.eligibility.cls === 'lo';
    return true;
  });
  const hidden = all.length - scoped.length;
  $('job_meta').textContent = `${jobs.length} / ${all.length} 岗` +
    (hidden ? `（已隐藏非技术岗 ${hidden}）` : '') +
    (jobFilter.rel !== 'all' ? ` ｜ 筛选：${jobFilter.rel === 'high' ? '高相关' : '有缺口/资格不符'}` : '');

  $('joblist').innerHTML = jobs.length ? jobs.map((job) => {
    const m = jobMatch(job), el = m.eligibility, rel = m.relevance, isLocal = job.src === 'local';
    const idx = all.indexOf(job);
    const rows = m.hits.map((h, hi) => `<tr>
      <td><b>${esc(h.name)}</b><small>${TIER_LABEL[h.tier] ? ' · ' + TIER_LABEL[h.tier] : ''}</small></td>
      <td class="jdsnip">${h.snip ? `<span title="${esc(h.kws.join('、'))}">${esc(h.snip)}</span>`
        : `<span class="muted">JD 无原文，仅按技能标签命中（${esc(h.kws.slice(0, 3).join('、'))}）</span>`}</td>
      <td>${h.projects.length ? esc(h.projects.join('、')) : '—'}</td>
      <td><span class="tstat ${h.state[1]}">${h.state[0]}</span></td>
      <td class="rnum">${h.done} / ${h.pool}</td>
      <td><span class="rscore ${h.avg == null ? '' : h.avg >= 3.3 ? 'hi' : h.avg >= 2.5 ? 'mid' : 'lo'}">${h.avg == null ? '未自测' : h.avg.toFixed(1)}</span></td>
      <td><button class="mini" data-jtrain="${hi}">训练</button></td>
    </tr>`).join('');
    const elChips = el.fields.map(([k, v, st]) =>
      `<span class="elc ${st}" title="${st === 'unknown' ? 'JD 未写，不能默认符合' : ''}">${esc(k)} <b>${esc(v)}</b></span>`).join('');
    return `<article class="q jcard" data-ji="${idx}">
      <div class="qh">
        <span class="pid">${esc(job.company)}</span>
        <span class="tag dtag ${decideOf(job, m).cls}" title="${esc(decideOf(job, m).why)}">🎯 ${esc(decideOf(job, m).label)}</span>
        <span class="rscore ${rel.cls}" title="${esc(rel.why)}">相关度 ${esc(rel.lvl)}</span>
        <span class="rscore ${m.cover >= 60 ? 'hi' : m.cover >= 30 ? 'mid' : 'lo'}" title="知识覆盖：命中技能里题库有对应题目的比例，只代表「有资料」">知识覆盖 ${m.cover}%</span>
        <span class="rscore ${masteryCls(m.mastery)}" title="理论掌握：自评均值，仅统计已自测技能；无数据如实显示「数据不足」">掌握 ${esc(m.mastery.txt)}</span>
        <span class="rscore ${m.evidence.total && m.evidence.covered / m.evidence.total >= 0.5 ? 'hi' : 'mid'}" title="工程证据：命中技能中，有项目档案（含代码证据）覆盖的项数">工程证据 ${m.evidence.covered}/${m.evidence.total}</span>
        <span class="rscore ${el.cls}" title="${esc(el.fields.map(f => f[0] + ':' + f[1]).join(' ｜ '))}">资格 ${esc(el.txt)}</span>
        <div class="qt">${esc(job.title)}</div>
        <span class="tag">${esc(job.city || '待核实')}</span>
        <span class="tag">${esc(job.type || '')}</span>
        ${job.family_conf === 'low' ? '<span class="tag warn" title="未归入五大目标岗位族，需人工复核">岗位族待复核</span>' : ''}
        <span class="tag" title="招聘状态（采集/核实后更新）">${esc(job.status || '待核实')}</span>
        ${(job.links || []).length && safeUrl(job.links[0]) ? `<a class="tag jlink" href="${esc(safeUrl(job.links[0]))}" target="_blank" rel="noopener">JD 原文 ↗</a>` : ''}
        ${isLocal ? `<button class="wrongmark" data-jdel="${esc(job.id)}" title="删除本地岗位">删除</button>` : ''}
      </div>
      <div class="jbody" style="display:none">
        <div class="qmeta" style="margin-top:0"><span><b>相关度依据：</b>${esc(rel.why)}</span></div>
        ${m.hits.length
          ? `<table class="rtable"><thead><tr>
              <th>技能要求</th><th>JD 原文依据</th><th>项目证据</th><th>证据状态</th>
              <th>题库（自测/总数）</th><th>掌握</th><th></th>
            </tr></thead><tbody>${rows}</tbody></table>
            <div class="qmeta"><span><b>缺口：</b>${m.gaps.length ? esc(m.gaps.slice(0, 4).join('；')) : '无结构性缺口（仍需按 JD 原文复核）'}</span></div>`
          : `<div class="hempty" style="padding:6px 0 2px">JD 未命中内置技能表（C++/Linux/模型部署/ROS2/感知/嵌入式/机器人学/工业通信…），先人工判断；粘贴完整 JD 原文能提高命中率。</div>`}
        <div class="qmeta"><span><b>招聘资格：</b>${elChips}</span></div>
        ${el.bad.length ? `<div class="qmeta"><span class="lo">硬性不符：${esc(el.bad.join('；'))}</span></div>` : ''}
        ${el.unknown.length ? `<div class="qmeta"><span class="muted">待你确认：${esc(el.unknown.join('、'))}</span></div>` : ''}
        ${job.jd ? `<div class="qmeta"><span title="${esc(job.jd)}">JD 摘要：${esc(job.jd.slice(0, 130))}${job.jd.length > 130 ? '…' : ''}</span></div>` : ''}
      </div>
    </article>`;
  }).join('') : '<div class="hempty">当前筛选下没有岗位。切到「含非技术岗」或放宽适配度筛选。</div>';
}

$('decide_cards').addEventListener('click', e => {
  const c = e.target.closest('[data-decide]'); if (!c) return;
  jobFilter.decide = jobFilter.decide === c.dataset.decide ? 'all' : c.dataset.decide;
  renderJobs();
  const el = $('joblist'); if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
});

$('jobfilter').addEventListener('click', e => {
  const ch = e.target.closest('.chip'); if (!ch) return;
  jobFilter[ch.dataset.jf] = ch.dataset.v;
  document.querySelectorAll(`#jobfilter .chip[data-jf="${ch.dataset.jf}"]`)
    .forEach(x => x.classList.toggle('on', x === ch));
  renderJobs();
  renderRadar();
});

$('joblist').addEventListener('click', e => {
  if (e.target.closest('a')) return;               // 链接不触发展开
  const del = e.target.closest('[data-jdel]');
  if (del) {
    if (!confirm('删除这个本地岗位？')) return;
    const local = JSON.parse(localStorage.getItem(LOCAL_JOBS_KEY) || '[]')
      .filter(j => j.id !== del.dataset.jdel);
    localStorage.setItem(LOCAL_JOBS_KEY, JSON.stringify(local));
    renderJobs(); return;
  }
  const tr = e.target.closest('[data-jtrain]');
  if (tr) {
    const job = loadJobs()[+tr.closest('.jcard').dataset.ji];
    const h = jobMatch(job).hits[+tr.dataset.jtrain];
    if (h && h.mods) {
      $('mod').value = h.mods[0]; refreshSubs();
      showView('bank'); window.scrollTo(0, 0); render();
    }
    return;
  }
  const head = e.target.closest('.qh');
  if (head) {
    const jb = head.parentElement.querySelector('.jbody');
    jb.style.display = jb.style.display === 'none' ? 'block' : 'none';
  }
});

$('j_save').addEventListener('click', () => {
  const co = $('j_co').value.trim(), ti = $('j_ti').value.trim();
  if (!co || !ti) { alert('公司与岗位名称必填'); return; }
  const local = JSON.parse(localStorage.getItem(LOCAL_JOBS_KEY) || '[]');
  local.push({
    id: 'local_' + Date.now(),
    company: co, title: ti,
    city: $('j_city').value.trim() || '待核实',
    type: $('j_ty').value, status: '待核实',
    jd: $('j_jd').value.trim(),
    links: $('j_url').value.trim() ? [$('j_url').value.trim()] : [],
    skills: [], src: 'local',
    found: new Date().toISOString().slice(0, 10),
  });
  localStorage.setItem(LOCAL_JOBS_KEY, JSON.stringify(local));
  ['j_co', 'j_ti', 'j_city', 'j_url', 'j_jd'].forEach(id => $(id).value = '');
  $('jobform').open = false;
  renderJobs(); renderRadar();
});

// ---- 岗位雷达：自动发现的新岗位 → 收藏转正 / 忽略 ----
const DISMISS_KEY = 'ib_jobs_dismiss_v1';
function loadDismiss(){
  try { return new Set(JSON.parse(localStorage.getItem(DISMISS_KEY) || '[]')); }
  catch { return new Set(); }
}
function renderRadar(){
  const jobs = RADAR.jobs || [];
  const dis = loadDismiss();
  const have = new Set(loadJobs().map(j => j.key).filter(Boolean));
  const pending = jobs.filter(j => !dis.has(j.key) && !have.has(j.key));
  const scopeAll = (typeof jobFilter !== 'undefined') && jobFilter.scope === 'all';
  const hiddenNonTech = scopeAll ? 0 : pending.filter(j => j.tech_relevant === false).length;
  const pendingTech = scopeAll ? pending : pending.filter(j => j.tech_relevant !== false);
  const show = pendingTech.slice(0, radarLimit);
  const savedN = jobs.length - pending.length;
  const restN = pendingTech.length - show.length;
  $('radar_meta').textContent = `全部 ${jobs.length} 岗 · 待处理 ${pendingTech.length}`
    + (hiddenNonTech ? `（另隐藏非技术岗 ${hiddenNonTech}）` : '')
    + ` · 快照 ${(RADAR.updated || '').slice(0, 10)}`;
  $('radarlist').innerHTML = show.length
    ? show.map(j => {
        const idx = jobs.indexOf(j);
        const m = jobMatch(j);
        const gcls = m.cover >= 60 ? 'hi' : m.cover >= 30 ? 'mid' : 'lo';
        return `<div class="rcard2">
          <div class="rh"><b>${esc(j.company)}</b>
            ${cbadge(jobClass(j))}
            <span class="rscore ${m.relevance.cls}" title="${esc(m.relevance.why)}">${esc(m.relevance.lvl)}</span>
            <span class="rscore ${gcls}" title="知识覆盖 ${m.cover}% ｜ 掌握 ${m.mastery.txt} ｜ 工程证据 ${m.evidence.covered}/${m.evidence.total}">覆盖 ${m.cover}%</span></div>
          <div class="rt">${esc(j.title)}</div>
          <small>${esc(j.city)} ｜ ${esc((j.families || []).join('/'))}${j.family_conf === 'low' ? '（待复核）' : ''} ｜ 资格 ${esc(m.eligibility.txt)} ｜ ${esc(j.class_basis || '分类待重算')} ｜ 发现 ${esc(j.found || j.first_seen || '')}${j.status === 'suspect' ? ' ｜ ⚠ 疑似下线' : ''}</small>
          <div class="mrow">
            <button class="mini" data-rcollect="${idx}">⭐ 收藏转正</button>
            <button class="mini" data-rdismiss="${idx}">忽略</button>
            ${(j.links || []).length && safeUrl(j.links[0]) ? `<a class="tag jlink" href="${esc(safeUrl(j.links[0]))}" target="_blank" rel="noopener">投递入口 ↗</a>` : ''}
          </div>
        </div>`;
      }).join('') +
      (jobs.length > show.length
        ? `<div class="hempty" style="grid-column:1/-1">本区只列<b>待处理的新发现</b>（显示 ${show.length} / ${pendingTech.length} 条）：已收藏或已忽略 ${savedN} 条${hiddenNonTech ? `、非技术岗 ${hiddenNonTech} 条（切「含非技术岗」可见）` : ''}${restN ? `、未展开 ${restN} 条` : ''}。
           ${restN ? `<button class="mini" data-rmore="1" style="margin-left:8px">再看 ${Math.min(restN, 18)} 条 →</button>` : ''}
           <button class="mini" data-rall="1" style="margin-left:8px">查看全部公司 / 岗位 →</button></div>` : '')
    : '<div class="hempty">没有待处理的新发现（已收藏或已忽略的不再显示在这里）。全部公司、全部岗位（含已处理）请到「🏢 公司」视图查看；雷达由 GitHub Actions 每日 09:30 自动扫描。</div>';
}
$('radarlist').addEventListener('click', e => {
  if (e.target.closest('[data-rmore]')) { radarLimit += 18; renderRadar(); return; }
  const c = e.target.closest('[data-rcollect], [data-rdismiss]'); if (!c) return;
  const j = (RADAR.jobs || [])[+(c.dataset.rcollect ?? c.dataset.rdismiss)];
  if (!j) return;
  if (c.dataset.rcollect !== undefined) {
    const local = JSON.parse(localStorage.getItem(LOCAL_JOBS_KEY) || '[]');
    local.push(Object.assign({}, j, { id: 'radar_' + j.key, src: 'local', status: '待核实' }));
    localStorage.setItem(LOCAL_JOBS_KEY, JSON.stringify(local));
  } else {
    const dis = loadDismiss(); dis.add(j.key);
    localStorage.setItem(DISMISS_KEY, JSON.stringify([...dis]));
  }
  renderJobs(); renderRadar();
});

// ---- V1.8 全部公司 & 全部岗位总览：公司池全量 + 校招/实习/社招分类 ----
const NAME_ALIAS = {'小鹏集团': '小鹏'};
const CLS_CSS = {'校招': 'campus', '实习': 'intern', '社招': 'social', '未标明': 'unknown'};
const CLASS_ORDER = ['实习', '校招', '社招', '未标明'];
function coKey(n){ return NAME_ALIAS[n] || n; }
function tierRank(t){ return t === 'A' ? 0 : t === 'B' ? 1 : t === 'C' ? 2 : 9; }
function cbadge(c){ return `<span class="cbadge ${CLS_CSS[c] || 'unknown'}">${c}</span>`; }

// 兼容尚未重分类的历史快照：前端兜底按标题 / 批次判一次，标成「历史快照未分类」
function jobClass(j){
  if (j.job_class) return j.job_class;
  if (/实习|intern|见习|暑期/i.test(j.title || '')) return '实习';
  if (/社招|社会招聘/i.test(j.title || '')) return '社招';
  if (/校招|届/.test((j.title || '') + ' ' + (j.batch || '') + ' ' + (j.type || ''))) return '校招';
  return '未标明';
}
function allRadarJobs(){
  return (RADAR.jobs || []).map(j => Object.assign({}, j, {
    job_class: jobClass(j),
    class_basis: j.class_basis || '历史快照未分类',
    class_conf: j.class_conf || 'none',
    class_evidence: j.class_evidence || ''}));
}
function allCompanies(){
  const map = new Map();
  (POOL || []).forEach(c => {
    const k = coKey(c.company_name);
    let e = map.get(k);
    if (!e) { e = {name: k, cat: c.category || '—', tier: c.tier || '—', pool: [], target: null}; map.set(k, e); }
    e.pool.push(c);
    if (tierRank(c.tier) < tierRank(e.tier)) e.tier = c.tier;
  });
  ((TARGETS && TARGETS.companies) || []).forEach(t => {
    const k = coKey(t.name);
    let e = map.get(k);
    if (!e) { e = {name: k, cat: t.main || '目标公司池', tier: '—', pool: [], target: null}; map.set(k, e); }
    e.target = t;
  });
  return [...map.values()].sort((a, b) => (tierRank(a.tier) - tierRank(b.tier)) || a.name.localeCompare(b.name, 'zh'));
}
function handleOf(j, dis, have){
  // 第二项加 hs- 前缀：避免与题卡全局 .todo（红色斜体）等类名冲突
  if (dis.has(j.key)) return ['已忽略', 'hs-dismissed'];
  if (have.has(j.key)) return ['已收藏', 'hs-saved'];
  return ['待处理', 'hs-todo'];
}
let compFilter = {cls: 'all', src: 'all', st: 'all', city: 'all', q: ''};
// 城市归一：岗位 city 串（「北京、苏州、上海」「广东·深圳市」「上海等」）→ 命中的重点城市列表
const CITY_LIST = ['苏州', '南京', '无锡', '常州', '合肥', '上海', '北京', '深圳', '广州',
  '杭州', '成都', '西安', '武汉', '宁波', '天津', '重庆', '东莞', '佛山', '珠海',
  '长沙', '香港', '昆山', '惠州', '济南', '郑州', '厦门', '南通'];
function citiesOf(s){
  const t = String(s || '');
  if (t.indexOf('待核实') >= 0 || !t.trim()) return ['待核实'];
  const hit = CITY_LIST.filter(c => t.indexOf(c) >= 0);
  return hit.length ? hit : ['其他'];
}

function renderCompanies(){
  const all = allRadarJobs(), dis = loadDismiss();
  const have = new Set(loadJobs().map(j => j.key).filter(Boolean));
  const cs = {};
  all.forEach(j => cs[j.job_class] = (cs[j.job_class] || 0) + 1);
  document.querySelectorAll('.chip[data-k="cls"]').forEach(ch => {
    const b = ch.querySelector('b');
    if (b) b.textContent = cs[ch.dataset.v] || 0;
  });
  const cityCnt = {};
  all.forEach(j => citiesOf(j.city).forEach(c => cityCnt[c] = (cityCnt[c] || 0) + 1));
  // 城市 chips 动态生成：苏南五城 + 实习五城优先固定，其余按岗位数降序，保证计数全覆盖
  const CITY_PRI = ['苏州', '南京', '无锡', '常州', '合肥', '上海', '北京', '深圳', '杭州'];
  const cityOrder = [
    ...CITY_PRI.filter(c => cityCnt[c]),
    ...Object.keys(cityCnt).filter(c => !CITY_PRI.includes(c) && c !== '待核实')
      .sort((a, b) => (cityCnt[b] - cityCnt[a]) || a.localeCompare(b, 'zh')),
    ...(cityCnt['待核实'] ? ['待核实'] : [])];
  $('city_chips').innerHTML = cityOrder.map(c =>
    `<button class="chip ${compFilter.city === c ? 'on' : ''}" data-k="city" data-v="${esc(c)}">${esc(c)} <b>${cityCnt[c]}</b></button>`).join('');
  // 牛客面经 / 真题卷 → 按公司聚合（公司名做宽松匹配：「华为HUAWEI」↔「华为」）
  const NC_BY_CO = {};
  (NC.experiences || []).forEach(x => {
    const b = NC_BY_CO[x.company] || (NC_BY_CO[x.company] = {exp: 0, papers: 0, last: null});
    b.exp++;
    if (!b.last || (x.collected_at || '') > (b.last.collected_at || '')) b.last = x;
  });
  (NC.papers || []).forEach(p => {
    if (p.company) (NC_BY_CO[p.company] = NC_BY_CO[p.company] || {exp: 0, papers: 0, last: null}).papers++;
  });
  function ncOf(name){
    if (NC_BY_CO[name]) return NC_BY_CO[name];
    let best = null;
    for (const [k, v] of Object.entries(NC_BY_CO)) {
      const hit = k.indexOf(name) >= 0 || (name.indexOf(k) >= 0 && k.length >= 2);
      if (hit && (!best || v.exp + v.papers > best.exp + best.papers)) best = v;
    }
    return best;
  }
  const jobsByCo = {};
  const byCo = {};
  all.forEach(j => {
    const k = coKey(j.company);
    (jobsByCo[k] || (jobsByCo[k] = [])).push(j);
    const c = byCo[k] || (byCo[k] = {'校招': 0, '实习': 0, '社招': 0, '未标明': 0});
    c[j.job_class]++;
  });
  const cos = allCompanies();
  const poolEntries = (POOL || []).length;
  const enabledEntries = (POOL || []).filter(c => c.enabled && c.source).length;
  const lowN = all.filter(j => j.class_conf === 'low').length;
  const savedN = all.filter(j => have.has(j.key)).length;
  const disN = all.filter(j => dis.has(j.key)).length;

  // 公司表：只受「来源 / 搜索」影响，保证「全部公司」始终可见
  const q = compFilter.q;
  const shownCo = cos.filter(e => {
    const enabled = e.pool.filter(c => c.enabled && c.source).length;
    const hay = (e.name + ' ' + e.cat + ' ' + (e.target ? (e.target.main || '') : '') + ' '
                 + e.pool.map(c => (c.ats_type || '') + ' ' + (c.directions || []).join(' ')).join(' ')).toLowerCase();
    if (q && hay.indexOf(q) < 0) return false;
    if (compFilter.city !== 'all') {
      const set = new Set((jobsByCo[e.name] || []).flatMap(j => citiesOf(j.city)));
      if (!set.has(compFilter.city)) return false;
    }
    const s = compFilter.src;
    if (s === 'pool') return e.pool.length > 0;
    if (s === 'enabled') return enabled > 0;
    if (s === 'unset') return e.pool.length > 0 && enabled === 0;
    if (s === 'targets') return e.pool.length === 0 && !!e.target;
    return true;
  });
  const coRows = shownCo.map(e => {
    const c = byCo[e.name] || {'校招': 0, '实习': 0, '社招': 0, '未标明': 0};
    const total = CLASS_ORDER.reduce((a, k) => a + (c[k] || 0), 0);
    const enabled = e.pool.filter(x => x.enabled && x.source).length;
    const ats = [...new Set(e.pool.map(x => x.ats_type || 'unknown'))].join(' / ') || '—';
    const src = [e.pool.length ? '雷达池' : '', e.target ? '目标池' : ''].filter(Boolean).join(' + ');
    const acc = enabled ? `<b>已接入 ${enabled} 源</b>`
      : e.pool.length ? '未接入（入口待适配）' : '仅目标池（无入口）';
    const labels = [...new Set(e.pool.map(x => (x.source || {}).label || (x.source || {}).type_label || ''))]
      .filter(Boolean).join(' / ') || (e.pool.length ? '校园招聘入口' : '—');
    const kinds = [...new Set((jobsByCo[e.name] || []).map(x => x.job_class))].join(' / ') || '—';
    const cities = {};
    (jobsByCo[e.name] || []).forEach(j => citiesOf(j.city).forEach(c => cities[c] = (cities[c] || 0) + 1));
    const cityTxt = Object.entries(cities).sort((a, b) => b[1] - a[1])
      .slice(0, 5).map(x => `${x[0]}${x[1] > 1 ? ' ' + x[1] : ''}`).join(' · ') || '—（尚未采集）';
    const nc = ncOf(e.name);
    const ncTxt = nc
      ? `牛客：面经 <b>${nc.exp}</b> · 真题卷 <b>${nc.papers}</b>` +
        (nc.last ? ` <a class="jlink" href="${esc(nc.last.url)}" target="_blank" rel="noopener">最近面经 ↗</a>` : '')
      : '牛客：暂无命中面经';
    const link = e.pool.find(x => x.enabled && x.source) || e.pool[0] || {};
    const url = link.career_url || (link.source || {}).url || (link.source || {}).base || '';
    return `<tr data-coname="${esc(e.name)}" title="点这行只看该公司的岗位；清空搜索恢复全部">
      <td><b>${esc(e.name)}</b><small>${esc(src)} · 档 ${esc(e.tier)}</small></td>
      <td>${esc(e.cat)}<small>${esc((e.pool[0] && (e.pool[0].directions || []).join(' / ')) || (e.target ? (e.target.roles || []).join(' / ') : ''))}</small></td>
      <td>${acc}<small>${esc(ats)} · 池内 ${e.pool.length} 条</small></td>
      <td>${esc(cityTxt)}<small>按已采集岗位聚合</small></td>
      <td>${total ? CLASS_ORDER.filter(k => c[k]).map(k => `${k} <b>${c[k]}</b>`).join(' · ') : '—（尚未采集）'}
          <small>入口性质：${esc(kinds)} · 批次 ${esc(labels)}</small>
          <small>${ncTxt}</small></td>
      <td>${url && safeUrl(url) ? `<a class="tag jlink" href="${esc(safeUrl(url))}" target="_blank" rel="noopener">招聘入口 ↗</a>` : '—'}
          ${e.target ? '<small>目标公司池有题目/面经索引</small>' : ''}</td>
    </tr>`;
  }).join('');
  $('comp_table').innerHTML = `<table class="rtable ctable"><thead><tr>
      <th>公司</th><th>方向 / 类别</th><th>接入情况</th><th>主要城市</th><th>在招岗位（性质 / 牛客）</th><th>入口</th>
    </tr></thead><tbody>${coRows || '<tr><td colspan="6" class="cempty">没有匹配的公司</td></tr>'}</tbody></table>`;

  // 岗位表：性质 / 状态 / 搜索；含已收藏、已忽略，按性质分组
  const jobs = all.filter(j => {
    if (compFilter.cls !== 'all' && j.job_class !== compFilter.cls) return false;
    const h = handleOf(j, dis, have)[1];
    const st = compFilter.st;
    if (st === 'open' && j.status !== 'open') return false;
    if (st === 'suspect' && j.status !== 'suspect') return false;
    if (['todo', 'saved', 'dismissed'].indexOf(st) >= 0 && h !== 'hs-' + st) return false;
    if (compFilter.city !== 'all' && citiesOf(j.city).indexOf(compFilter.city) < 0) return false;
    if (q) {
      const hay = (j.company + ' ' + j.title + ' ' + (j.city || '') + ' ' + (j.batch || '') + ' '
                   + (j.label || '') + ' ' + (j.families || []).join(' ') + ' '
                   + j.class_basis + ' ' + (j.source_id || '')).toLowerCase();
      if (hay.indexOf(q) < 0) return false;
    }
    return true;
  });
  const groups = CLASS_ORDER.map(c => ({c: c, list: jobs.filter(j => j.job_class === c)}))
    .filter(g => g.list.length);
  $('comp_jobs').innerHTML = groups.length ? groups.map(g => {
    const rows = g.list.map(j => {
      const h = handleOf(j, dis, have);
      const gy = j.grad_year ? j.grad_year + '届' : '届别未标注';
      const eli = j.job_class === '实习' ? '实习可投 · 不限届别'
        : j.grad_year && j.grad_year !== USER_GRAD ? '面向' + j.grad_year + '届 · 仅作 JD 参考'
        : j.grad_year === USER_GRAD ? USER_GRAD + '届匹配' : '届别未标注 · 待核实';
      return `<tr class="cjobrow ${h[1]}">
        <td>${cbadge(g.c)}</td>
        <td><div class="jt">${esc(j.title)}</div><small>${esc(j.company)} · ${esc(j.city || '待核实')} · ${esc((j.families || []).join('/') || '其他')}</small></td>
        <td>${esc(j.batch || j.label || '—')}<small>${gy} · ${eli}${j.jd ? '' : ' · 该源列表无 JD 正文，点入口看原文'}</small></td>
        <td><span class="conf ${j.class_conf}">${esc(j.class_basis)}</span><small>${esc(j.class_evidence || '')}${j.grad_year_raw ? ' · 已清除入口批次届别' : ''}</small></td>
        <td>${j.status === 'suspect' ? '<span class="rscore lo">疑似下线</span>' : '<span class="rscore hi">在招</span>'}
            <small>${h[0]} · 发现 ${esc(j.first_seen || '—')}</small></td>
        <td>${(j.links || []).length ? `<a class="tag jlink" href="${esc(j.links[0])}" target="_blank" rel="noopener">JD ↗</a>` : '—'}</td>
      </tr>`;
    }).join('');
    const gc = CLS_CSS[g.c] === 'campus' ? 'var(--campus)' : CLS_CSS[g.c] === 'intern' ? 'var(--intern)'
      : CLS_CSS[g.c] === 'social' ? 'var(--social)' : 'var(--unknown)';
    return `<div class="rsec" style="border-left:4px solid ${gc};padding-left:8px">${cbadge(g.c)} ${g.list.length} 岗</div>
      <table class="rtable ctable"><thead><tr>
        <th>性质</th><th>公司 · 岗位</th><th>批次 / 届别</th><th>判定依据</th><th>状态 · 处理</th><th>入口</th>
      </tr></thead><tbody>${rows}</tbody></table>`;
  }).join('') : '<div class="cempty">当前筛选下没有岗位（试试切到「全部」或清空搜索）。</div>';

  $('comp_stat').innerHTML = [
    [cos.length, '公司合计（两池去重）', 'sc-co'],
    [poolEntries, '公司池条目 · 启用 ' + enabledEntries + ' 源', 'sc-pool'],
    [all.length, '全部岗位（含已处理）', 'sc-job'],
    [cs['校招'] || 0, '校招', 'sc-campus'],
    [cs['实习'] || 0, '实习', 'sc-intern'],
    [lowN, '入口推定 · 待核实', 'sc-low'],
    [(NC.experiences || []).length + ' / ' + (NC.papers || []).length, '牛客面经 / 真题卷', 'sc-nc'],
  ].map(x => `<div class="scard ${x[2]}"><b>${x[0]}</b><small>${x[1]}</small></div>`).join('');
  const poolNames = new Set((POOL || []).map(c => coKey(c.company_name)));
  $('comp_note').innerHTML =
    `全部 <b>${cos.length} 家公司 / ${all.length} 个岗位</b>都在这里（含已收藏、已忽略，标注处理状态），` +
    `不再被岗位雷达折叠区「只列 40 条待处理」挡住：公司表 ${shownCo.length} 行 · 岗位表 ${jobs.length} 行（已收藏 ${savedN} · 已忽略 ${disN}）。` +
    `真实面经与公司真题卷在下方「📰 真实面经」面板，随搜索词联动。<br>` +
    `筛选时点 <b>↩ 重置</b> 一键清空全部条件；岗位状态与城市筛选收在「⚙ 更多筛选」里，点公司行可只看该公司岗位。<br>` +
    `分类依据：<b>岗位标题明确 &gt; 来源批次标签 &gt; 校园招聘入口推定</b>；「入口推定」不等于官方写明校招批次，` +
    `投递前点 JD 原文核实。实习岗不套用入口批次的届别；校招 2027 届对 ${USER_GRAD} 届仅作 JD 参考。`;
  renderNC(compFilter.q);
  updateReset();
}

// 真实面经 + 公司真题卷面板（牛客同步数据，随搜索词与自身筛选联动）
let ncFilter = {co: 'all', round: 'all', role: 'all', onlyRef: false, limit: 10};
function renderNC(q){
  const all = NC.experiences || [];
  const cos = {};
  all.forEach(x => cos[x.company] = (cos[x.company] || 0) + 1);
  // 公司 chips：目标池公司优先，其余按篇数；避免只显示篇数最多的互联网大厂
  const isTargetCo = c => (POOL || []).some(p => p.company_name === c)
    || ((TARGETS && TARGETS.companies) || []).some(t => t.name === c);
  const topCo = Object.entries(cos)
    .sort((a, b) => (isTargetCo(b[0]) - isTargetCo(a[0])) || (b[1] - a[1]))
    .slice(0, 10);
  const allCo = Object.entries(cos).sort((a, b) => b[1] - a[1]);
  const selAll = $('nc_co_all');
  selAll.innerHTML = '<option value="all">更多公司…</option>' +
    allCo.map(([c, n]) => `<option value="${esc(c)}">${esc(c)}（${n} 篇）</option>`).join('');
  selAll.value = ncFilter.co;
  const chipsCo = topCo.slice();
  if (ncFilter.co !== 'all' && !chipsCo.some(x => x[0] === ncFilter.co) && cos[ncFilter.co]) {
    chipsCo.unshift([ncFilter.co, cos[ncFilter.co]]);   // 选中的公司不在前十也要显示
  }
  $('nc_co_chips').innerHTML =
    `<button class="chip ${ncFilter.co === 'all' ? 'on' : ''}" data-nk="co" data-v="all">全部 <b>${all.length}</b></button>` +
    chipsCo.map(([c, n]) => `<button class="chip ${ncFilter.co === c ? 'on' : ''}" data-nk="co" data-v="${esc(c)}">${esc(c)} <b>${n}</b></button>`).join('');
  const rSel = $('nc_round'), dSel = $('nc_role');
  if (rSel.options.length <= 1) {
    [...new Set(all.map(x => x.round).filter(Boolean))].forEach(r => rSel.add(new Option(r, r)));
  }
  if (dSel.options.length <= 1) {
    [...new Set(all.map(x => x.role).filter(Boolean))].forEach(r => dSel.add(new Option(r, r)));
  }
  const exps = all.filter(x => {
    if (ncFilter.co !== 'all' && x.company !== ncFilter.co) return false;
    if (ncFilter.round !== 'all' && (x.round || '') !== ncFilter.round) return false;
    if (ncFilter.role !== 'all' && (x.role || '') !== ncFilter.role) return false;
    if (ncFilter.onlyRef && !(x.highlights || []).some(h => h.ref)) return false;
    if (q) {
      const hay = (x.company + ' ' + x.title + ' ' + (x.role || '') + ' ' + (x.round || '') + ' '
                   + (x.highlights || []).map(h => h.q + ' ' + (h.ref || '')).join(' ')).toLowerCase();
      if (hay.indexOf(q) < 0) return false;
    }
    return true;
  });
  const papers = (NC.papers || []).filter(p => !q ||
    (p.company + ' ' + p.paperName).toLowerCase().indexOf(q) >= 0);
  const last = all.reduce((a, x) => (x.collected_at || '') > a ? x.collected_at : a, '');
  const refN = exps.filter(x => (x.highlights || []).some(h => h.ref)).length;
  $('nc_meta').textContent = `面经 ${exps.length} / ${all.length} 篇（含题号 ${refN}）· 真题卷 ${papers.length} / ${(NC.papers || []).length} 套 · 最近同步 ${(last || '—').slice(0, 10)}`;
  const roundTxt = x => esc(x.round || '轮次未标注');
  const shown = exps.slice(0, ncFilter.limit);
  $('nc_exp').innerHTML = exps.length ? shown.map(x => {
    const hs = x.highlights || [];
    const rows = hs.map(h => `<li class="nch">
        ${h.ref ? `<a class="qref" href="#bank" data-q="${h.ref}" title="跳到题库做这道题">${h.ref}</a>`
                : h.near ? `<span class="qref near" title="近似题号：考点相近但题干不同">~${h.near}</span>`
                         : '<span class="qref none">未入库</span>'}
        <span class="nchq">${esc(h.q)}</span>
        <span class="rnum">${h.sim ? h.sim.toFixed(2) : ''}</span>
      </li>`).join('');
    return `<details class="nccard">
      <summary>
        <b>${esc(x.company)}</b>
        <span class="tag">${roundTxt(x)}</span>
        <span class="tag">${x.n_questions || 0} 题</span>
        ${x.role ? `<span class="tag">${esc(x.role)}</span>` : ''}
        <span class="rnum">${esc((x.date_raw || x.collected_at || '').slice(0, 10))}</span>
        <div class="nct">${esc(x.title)}</div>
      </summary>
      <div class="ncb">
        ${rows ? `<ol class="nclist">${rows}</ol>` : '<div class="cempty">这篇没有提取到可用题目，点原帖看完整正文。</div>'}
        <div class="mrow" style="display:flex;gap:10px;align-items:center">
          <a class="tag jlink" href="${esc(x.url)}" target="_blank" rel="noopener">原帖全文 ↗</a>
          <span class="rnum">共 ${x.n_questions || 0} 题${x.n_reverses ? ' · 反问 ' + x.n_reverses : ''}；上面是前 ${hs.length} 道原文摘录</span>
        </div>
      </div>
    </details>`;
  }).join('') +
    (exps.length > shown.length
      ? `<div class="mrow" style="margin:8px 0"><button class="mini" data-ncmore="1">显示更多（还有 ${exps.length - shown.length} 篇）</button></div>`
      : '')
    : '<div class="cempty">当前筛选下没有面经（换个公司/轮次，或清空搜索）。</div>';
  const TOPICS = [['C++', 1612], ['操作系统', 1617], ['网络基础', 1820], ['Linux', 638],
    ['推理优化', 190], ['RAG', 192], ['Agent', 191], ['计算机视觉', 199]];
  const TOPIC_URL = 'https://www.nowcoder.com/exam/intelligent?questionJobId=3&subTabName=intelligent_page&tagId=273590';
  $('nc_topics').innerHTML = TOPICS.map(([t, n]) =>
    `<a class="chip" href="${TOPIC_URL}" target="_blank" rel="noopener" title="进入牛客专项练习后按左侧分类选择">${t} <b>${n}</b> ↗</a>`).join('');
  $('nc_papers').innerHTML = papers.length ? `<table class="rtable ctable"><thead><tr>
      <th>公司</th><th>卷名</th><th>题量</th><th>练习人数</th><th>在线作答</th>
    </tr></thead><tbody>${papers.map(p => `<tr>
      <td><b>${esc(p.company || '通用')}</b></td>
      <td>${esc(p.paperName)}</td>
      <td class="rnum">${esc(p.questionCount || '—')}</td>
      <td class="rnum">${esc(p.practiceCnt || '—')}</td>
      <td>${safeUrl(p.summaryUrl) ? `<a class="tag jlink" href="${esc(safeUrl(p.summaryUrl))}" target="_blank" rel="noopener">牛客 ↗</a>` : '—'}</td>
    </tr>`).join('')}</tbody></table>`
    : '<div class="cempty">暂无命中的真题卷。</div>';
}
$('nc_chips').addEventListener('click', e => {
  const ch = e.target.closest('.chip[data-nk]'); if (!ch) return;
  ncFilter[ch.dataset.nk] = ch.dataset.v;
  renderNC(compFilter.q);
});
$('nc_round').addEventListener('change', e => { ncFilter.round = e.target.value; renderNC(compFilter.q); });
$('nc_role').addEventListener('change', e => { ncFilter.role = e.target.value; renderNC(compFilter.q); });
$('nc_co_all').addEventListener('change', e => { ncFilter.co = e.target.value; renderNC(compFilter.q); });
document.addEventListener('click', e => {
  if (!e.target.closest('[data-ncmore]')) return;
  ncFilter.limit += 20;
  renderNC(compFilter.q);
});
$('nc_onlyref').addEventListener('change', e => { ncFilter.onlyRef = e.target.checked; renderNC(compFilter.q); });
document.addEventListener('click', e => {
  const a = e.target.closest('a.qref[data-q]'); if (!a) return;
  e.preventDefault();
  showView('bank');
  $('q').value = a.dataset.q;
  window.scrollTo(0, 0);
  render();
});
$('comp_table').addEventListener('click', e => {
  if (e.target.closest('a')) return;
  const tr = e.target.closest('tr[data-coname]'); if (!tr) return;
  compFilter.q = tr.dataset.coname.toLowerCase();
  $('comp_q').value = tr.dataset.coname;
  renderCompanies();
  $('comp_jobs').scrollIntoView({behavior: 'smooth', block: 'start'});
});
document.addEventListener('click', e => {
  const ch = e.target.closest('.chip[data-k]');
  if (!ch || !ch.closest('#view-comp')) return;
  compFilter[ch.dataset.k] = ch.dataset.v;
  document.querySelectorAll(`.chip[data-k="${ch.dataset.k}"]`)
    .forEach(x => x.classList.toggle('on', x === ch));
  renderCompanies();
});
function updateReset(){
  const n = ['cls', 'src', 'st', 'city'].filter(k => compFilter[k] !== 'all').length
            + (compFilter.q ? 1 : 0);
  const btn = $('comp_reset');
  btn.classList.toggle('act', n > 0);
  btn.textContent = n > 0 ? `↩ 重置(${n})` : '↩ 重置';
  const more = $('comp_more_n');
  const mn = (compFilter.st !== 'all' ? 1 : 0) + (compFilter.city !== 'all' ? 1 : 0);
  more.hidden = mn === 0;
  more.textContent = String(mn);
}
$('comp_reset').addEventListener('click', () => {
  compFilter = {cls: 'all', src: 'all', st: 'all', city: 'all', q: ''};
  ncFilter = {co: 'all', round: 'all', role: 'all', onlyRef: false, limit: 10};
  $('comp_q').value = '';
  if ($('nc_round')) $('nc_round').value = 'all';
  if ($('nc_role')) $('nc_role').value = 'all';
  if ($('nc_onlyref')) $('nc_onlyref').checked = false;
  document.querySelectorAll('#view-comp .chip[data-k]').forEach(x =>
    x.classList.toggle('on', x.dataset.v === 'all'));
  renderCompanies();
  window.scrollTo(0, 0);
});
let compQT;
$('comp_q').addEventListener('input', e => {
  clearTimeout(compQT);
  const v = e.target.value.trim().toLowerCase();
  compQT = setTimeout(() => { compFilter.q = v; renderCompanies(); }, 120);
});
document.addEventListener('click', e => {
  if (e.target.closest('#h_nc_more')) {
    showView('comp');
    setTimeout(() => $('ncbox').scrollIntoView({behavior: 'smooth', block: 'start'}), 60);
    return;
  }
  if (e.target.closest('#h_allco, [data-goall], [data-rall]')) {
    showView('comp'); window.scrollTo(0, 0);
  }
});

refreshSubs();
render();
renderBankNav();
showView(['home', 'bank', 'train', 'jobs', 'comp', 'rep'].includes(location.hash.slice(1))
  ? location.hash.slice(1) : 'home');
</script>
</body>
</html>
"""


def main() -> int:
    qs = load_questions()
    if not qs:
        print("content/ 下没有题卡")
        return 1
    DIST.mkdir(parents=True, exist_ok=True)

    modopts = "\n".join(
        f'<option value="{m}">{MODULE_NAME[m]}</option>'
        for m in MODULE_ORDER if any(q["module"] == m for q in qs))

    # 公司 / 岗位口径：companies/targets.json，缺失时降级为空，不影响构建
    tj = ROOT / "companies" / "targets.json"
    targets = json.loads(tj.read_text(encoding="utf-8")) if tj.exists() else {
        "always": [], "roles": [], "companies": []}
    coopts = "\n".join(f'<option value="{html.escape(c["name"], quote=True)}">'
                       f'{html.escape(c["name"])}</option>'
                       for c in targets.get("companies", []))
    rlopts = "\n".join(f'<option value="{html.escape(r["key"], quote=True)}">'
                       f'{html.escape(r["name"])}</option>'
                       for r in targets.get("roles", []))

    # 岗位三层体系的中层：具体岗位模板（权重 + JD 依据）
    pj = ROOT / "companies" / "job_profiles.json"
    profiles = json.loads(pj.read_text(encoding="utf-8")).get("profiles", []) if pj.exists() else []
    profopts = "\n".join(f'<option value="{html.escape(p["id"], quote=True)}">'
                         f'{html.escape(p["name"])}</option>' for p in profiles)

    # 岗位收藏种子（gen_jobs.py 由 job_profiles 生成；网页上人工添加的存 localStorage）
    jo = ROOT / "companies" / "jobs.json"
    jobs = json.loads(jo.read_text(encoding="utf-8")).get("jobs", []) if jo.exists() else []

    # 岗位雷达快照（tools/job_radar.py 定时产出；缺失时降级为空）
    rr = ROOT / "sources" / "jobs_radar.json"
    radar = json.loads(rr.read_text(encoding="utf-8")) if rr.exists() else {"jobs": []}

    # V1.8 全量公司池（含未接入的源），供「🏢 公司」视图展示全部公司
    cp = ROOT / "companies" / "radar_companies.json"
    pool = json.loads(cp.read_text(encoding="utf-8")).get("companies", []) if cp.exists() else []

    # 牛客同步数据：面经索引（公开帖，含题目与原帖链接）+ 公司真题卷元数据（不抓题干）
    nc = {"experiences": [], "papers": []}
    ne = ROOT / "sources" / "nowcoder_experiences.jsonl"
    if ne.exists():
        nc["experiences"] = [json.loads(x) for x in
                             ne.read_text(encoding="utf-8").splitlines() if x.strip()]
    npp = ROOT / "sources" / "nowcoder_papers.csv"
    if npp.exists():
        with npp.open(encoding="utf-8-sig", newline="") as f:
            nc["papers"] = list(csv.DictReader(f))

    # 牛客面试宝典考点地图（sources/tutorial_map.json）：章/节 → 命中题号，
    # 在构建期算好，页面「章题数」与点进去的筛选结果完全一致
    def _rule_hit(q, rule):
        if not rule:
            return False
        if "modules" in rule and q["module"] not in rule["modules"]:
            return False
        if "subs" in rule and (q.get("sub") or "") not in rule["subs"]:
            return False
        if "terms" in rule:
            # 只匹配 标题 + 标签 + 子方向：正文里「加锁/梯度/期望」这类词太泛，
            # 会把无关题全卷进来（曾把数据库算成 113 题）
            hay = " ".join([q.get("title") or "", q.get("sub") or "",
                            " ".join(q.get("tags") or [])]).lower()
            if not any(t.lower() in hay for t in rule["terms"]):
                return False
        return True

    tut = {"note": "", "tutorials": [], "practice": []}
    tp = ROOT / "sources" / "tutorial_map.json"
    if tp.exists():
        tut = json.loads(tp.read_text(encoding="utf-8"))
        for t in tut["tutorials"]:
            for ch in t["chapters"]:
                ch["ids"] = [q["id"] for q in qs if _rule_hit(q, ch.get("rule"))]
                for sec in ch.get("sections", []):
                    r = sec.get("rule")
                    sec["ids"] = [q["id"] for q in qs if _rule_hit(q, r)] if r else None
                ch["weak"] = sum(1 for q in qs
                                 if q["id"] in set(ch["ids"]) and q["priority"] == "P0")

    # 项目证据档案：技能栈 → 题库项目深挖题量，供「工程证据」维度使用
    proj = {"projects": []}
    pp = ROOT / "companies" / "projects.json"
    if pp.exists():
        proj = json.loads(pp.read_text(encoding="utf-8"))
        sub_n = {}
        for q in qs:
            if q["module"] == "01_project":
                sub_n[q.get("sub") or ""] = sub_n.get(q.get("sub") or "", 0) + 1
        for pr in proj.get("projects", []):
            pr["interview_count"] = sub_n.get(pr.get("sub") or "", 0)

    # 系统健康：数据质量指标（构建期），页面只负责展示 + 补运行时项
    from datetime import date as _date
    jl = radar.get("jobs", []) if isinstance(radar, dict) else []
    hq = {"total": len(qs),
          "dup_id": len(qs) - len({q["id"] for q in qs}),
          "no_answer": sum(1 for q in qs if q.get("status") not in ("answered", "verified")),
          "no_source": sum(1 for q in qs if not (q.get("sourceRef") or q.get("sourceType"))),
          "p0": sum(1 for q in qs if q.get("priority") == "P0")}
    hjob = {"total": len(jl),
            "jd": sum(1 for j in jl if (j.get("jd") or "").strip()),
            "city_unknown": sum(1 for j in jl if "待核实" in (j.get("city") or "")),
            "class_low": sum(1 for j in jl if j.get("class_conf") == "low"),
            "family_low": sum(1 for j in jl if j.get("family_conf") == "low"),
            "non_tech": sum(1 for j in jl if j.get("tech_relevant") is False),
            "req_known": sum(1 for j in jl if (j.get("req") or {}).get("education")
                             or (j.get("req") or {}).get("grad_range")),
            "suspect": sum(1 for j in jl if j.get("status") == "suspect"),
            "sources_ok": sum(1 for x in radar.get("sources", []) if x.get("status") == "success"),
            "sources": len(radar.get("sources", [])),
            "updated": (radar.get("updated") or "")[:19]}
    hco = {"entries": len(pool),
           "enabled": sum(1 for c in pool if c.get("enabled")),
           "no_url": sum(1 for c in pool
                         if not (c.get("career_url") or (c.get("source") or {}).get("url")))}
    _exps = nc.get("experiences") or []
    hnc = {"exps": len(_exps), "papers": len(nc.get("papers") or []),
           "quotes": sum(len(e.get("highlights") or []) for e in _exps),
           "refs": sum(1 for e in _exps for h in (e.get("highlights") or []) if h.get("ref")),
           "last": max([(e.get("collected_at") or "")[:10] for e in _exps] or [""])}
    checks = []
    def _chk(name, status, detail):
        checks.append({"name": name, "status": status, "detail": detail})
    _chk("题库 ID 唯一", "ok" if hq["dup_id"] == 0 else "bad", f"重复 {hq['dup_id']} 个")
    _chk("题卡全部有答案", "ok" if hq["no_answer"] == 0 else "bad",
         f"{hq['total'] - hq['no_answer']} / {hq['total']} 已答")
    _chk("每题有来源", "ok" if hq["no_source"] == 0 else "warn", f"缺来源 {hq['no_source']} 题")
    _chk("采集源成功率", "ok" if hjob["sources_ok"] >= hjob["sources"] * 0.9 else "warn",
         f"{hjob['sources_ok']} / {hjob['sources']} 成功")
    try:
        _age = (_date.today() - _date.fromisoformat(hjob["updated"][:10])).days
    except Exception:
        _age = 999
    _chk("岗位快照新鲜度", "ok" if _age <= 2 else ("warn" if _age <= 7 else "bad"),
         f"{hjob['updated'][:10] or '无快照'}（{_age} 天前）")
    _chk("JD 原文完整率", "ok" if hjob["total"] and hjob["jd"] / hjob["total"] >= 0.9 else "warn",
         f"{hjob['jd']} / {hjob['total']}（{round(hjob['jd'] / max(1, hjob['total']) * 100)}%）")
    _chk("招聘条件可抽取", "ok" if hjob["total"] and hjob["req_known"] / hjob["total"] >= 0.6 else "warn",
         f"{hjob['req_known']} / {hjob['total']}（其余「未说明」，不当成符合）")
    _chk("岗位族待复核", "ok" if hjob["family_low"] <= hjob["total"] * 0.3 else "warn",
         f"{hjob['family_low']} 岗未归入五大目标族")
    _chk("非技术岗隔离", "ok", f"{hjob['non_tech']} 岗默认隐藏（可切「含非技术岗」）")
    _chk("公司入口完整", "ok" if hco["no_url"] == 0 else "warn",
         f"{hco['entries']} 条 / 启用 {hco['enabled']} 源 / 缺入口 {hco['no_url']}")
    _chk("面经题号关联", "ok" if hnc["refs"] else "warn",
         f"{hnc['exps']} 篇 · {hnc['quotes']} 条原文 · 命中题号 {hnc['refs']} 条")
    health = {"built_at": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
              "q": hq, "job": hjob, "co": hco, "nc": hnc, "checks": checks}

    data = json.dumps(qs, ensure_ascii=False, separators=(",", ":"))
    out = (PAGE.replace("__DATA__", data)
               .replace("__TARGETS__", json.dumps(targets, ensure_ascii=False,
                                                 separators=(",", ":")))
               .replace("__PROFILES__", json.dumps(profiles, ensure_ascii=False,
                                                  separators=(",", ":")))
               .replace("__JOBS__", json.dumps(jobs, ensure_ascii=False,
                                               separators=(",", ":")))
               .replace("__RADAR__", json.dumps(radar, ensure_ascii=False,
                                                separators=(",", ":")))
               .replace("__POOL__", json.dumps(pool, ensure_ascii=False,
                                               separators=(",", ":")))
               .replace("__NC__", json.dumps(nc, ensure_ascii=False,
                                             separators=(",", ":")))
               .replace("__TUT__", json.dumps(tut, ensure_ascii=False,
                                              separators=(",", ":")))
               .replace("__PROJ__", json.dumps(proj, ensure_ascii=False,
                                               separators=(",", ":")))
               .replace("__HEALTH__", json.dumps(health, ensure_ascii=False,
                                                 separators=(",", ":")))
               .replace("__PROFOPTS__", profopts)
               .replace("__COOPTS__", coopts)
               .replace("__RLOPTS__", rlopts)
               .replace("__MODOPTS__", modopts)
               .replace("__COUNT__", str(len(qs))))
    target = DIST / "bank.html"
    target.write_text(out, encoding="utf-8")

    from collections import Counter
    c_mod = Counter(q["module"] for q in qs)
    c_pri = Counter(q["priority"] for q in qs)
    c_st = Counter(q["status"] for q in qs)
    print(f"生成 {target}  ({target.stat().st_size/1024:.0f} KB)")
    print(f"题数 {len(qs)}   " + "  ".join(f"{k}:{v}" for k, v in sorted(c_pri.items())))
    print("已答 {} / 待补充 {}".format(
        sum(v for k, v in c_st.items() if k != "indexed"), c_st.get("indexed", 0)))
    print("\n模块分布：")
    for m in MODULE_ORDER:
        if c_mod.get(m):
            print(f"  {MODULE_NAME[m]:<8}{c_mod[m]:>4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
