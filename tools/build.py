#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 content/**.md 编译成单文件题库网页 dist/bank.html。

零依赖：自己解析 frontmatter、自己渲染 Markdown，不需要 pyyaml / markdown。
产物是单个 HTML，双击即开，手机可用，可直接托管到 GitHub Pages。
"""
from __future__ import annotations

import html
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
    "11_python": "Python",
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
<title>面试题库 · __COUNT__ 题</title>
<style>
:root{
  --bg:#faf3e2; --soft:#f3e9d2; --paper:#fffcf3; --line:#dbcba5;
  --tx:#2d2a21; --muted:#665c49; --blue:#1b5e8c; --green:#2e6b3e;
  --red:#a63a2e; --orange:#9a5a12; --purple:#6b4fa8; --yellow:#6f5520;
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
@media(max-width:640px){
  h1{font-size:20px}.qt{flex:1 1 100%}.wrap{padding:0 12px 60px}
  .bar{gap:6px}input[type=search]{flex:1 1 100%}
}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>面试题库</h1>
  <div class="meta" id="stat"></div>
</header>

<div class="bar">
  <input type="search" id="q" placeholder="搜题目 / 正文 / 公司 / 岗位，如 Momenta、推理部署">
  <select id="co"><option value="">全部公司</option>__COOPTS__</select>
  <select id="rl"><option value="">全部岗位</option>__RLOPTS__</select>
  <select id="mod"><option value="">全部模块</option>__MODOPTS__</select>
  <select id="sub"><option value="">全部子方向</option></select>
  <select id="pri"><option value="">全部优先级</option>
    <option value="P0">P0 必答</option><option value="P1">P1 进阶</option><option value="P2">P2 长期</option></select>
  <select id="st"><option value="">全部状态</option>
    <option value="answered">已答</option><option value="draft">草稿</option>
    <option value="indexed">待补充</option></select>
  <label class="chk"><input type="checkbox" id="wrong"> 只看错题</label>
  <label class="chk"><input type="checkbox" id="hidepred" title="隐藏 S4 岗位推导预测题，只看真实面经与一手题"> 隐藏预测题</label>
  <label class="chk"><input type="checkbox" id="selftest" title="自测模式：搜索不再自动展开答案，先自己答再看"> 自测模式</label>
  <select id="rev" title="间隔复习：按自评分安排">
    <option value="">全部复习状态</option>
    <option value="due">今日该复习</option>
    <option value="weak">薄弱（自评≤2）</option>
    <option value="never">从未自测</option>
  </select>
  <button id="exp" class="mini" title="导出错题与自评记录（JSON）">备份↓</button>
  <button id="impb" class="mini" title="从 JSON 恢复复习数据">恢复↑</button>
  <input type="file" id="imp" accept=".json" hidden>
</div>
<div class="hint" id="hint"></div>

<div id="list"></div>
<div class="empty" id="empty" style="display:none">没有匹配的题目</div>
</div>

<script>
const DATA = __DATA__;
const TARGETS = __TARGETS__;
const WRONG_KEY = 'ib_wrong_v1';
const REV_KEY = 'ib_review_v1';
// 间隔复习：自评分 1~4 → 下次复习间隔天数（SM-2 简化版）
const REV_DAYS = {1: 1, 2: 3, 3: 7, 4: 21};
const OPEN_ALL = location.hash === '#all';   // 调试用：全部展开
let wrong = new Set(JSON.parse(localStorage.getItem(WRONG_KEY) || '[]'));
let review = JSON.parse(localStorage.getItem(REV_KEY) || '{}');
let SELFTEST = false;
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
      title="${{1:'完全不会',2:'想不起来',3:'基本掌握',4:'可答追问'}[v]}">${v}</button>`).join('')}
    <span class="gstat">${when}</span></div>`;
}
function card(q){
  const isW = wrong.has(q.id);
  const st = q.status === 'indexed' ? '<span class="tag">待补充</span>' : '';
  const ap = (q.appearances || []).map(a =>
      `<span class="tag appear" title="真实出现记录">${esc(a)}</span>`).join('');
  const ev = `<span class="ev ev${q.evidence}" title="证据等级：${{S1:'官方文档/JD',S2:'本人一手',S3:'社区面经',S4:'岗位推导预测'}[q.evidence]}">${q.evidence}</span>`;
  return `<article class="q" data-id="${q.id}">
    <div class="qh">
      <span class="pid">${q.id}</span>
      <span class="pri ${q.priority}">${q.priority}</span>
      <div class="qt">${esc(q.title)}</div>
      <span class="tag">${esc(q.sub || q.moduleName)}</span>
      ${ev}${st}${ap}
      <button class="wrongmark ${isW?'on':''}" data-w="${q.id}">${isW?'已标错':'标错'}</button>
    </div>
    <div class="body">${q.html}${gradeBar(q)}</div>
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

function render(){
  const kw = $('q').value.trim().toLowerCase();
  const mod = $('mod').value, pri = $('pri').value, st = $('st').value;
  const sub = $('sub').value;
  const onlyW = $('wrong').checked;
  const coDef = TARGETS.companies.find(c => c.name === $('co').value);
  const rlDef = ROLE_BY_KEY[$('rl').value];

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
    if (sub && q.sub !== sub) return false;
    if (pri && q.priority !== pri) return false;
    if (st && q.status !== st) return false;
    if (onlyW && !wrong.has(q.id)) return false;
    if ($('hidepred').checked && q.evidence === 'S4') return false;
    const rv = $('rev').value;
    if (rv && revState(q) !== rv) return false;
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
  $('empty').style.display = hit.length ? 'none' : 'block';
  SELFTEST = $('selftest').checked;
  // 搜索/筛选时自动展开，省一次点击；自测模式下不展开，先自己答
  if (!SELFTEST && (kw || mod || pri || st || sub || onlyW || coDef || rlDef || OPEN_ALL)) {
    list.querySelectorAll('.q').forEach(el => el.classList.add('open'));
  }
  if (SELFTEST) list.classList.add('selftest'); else list.classList.remove('selftest');
  const dueCnt = DATA.filter(q => revState(q) === 'due').length;
  $('stat').textContent = `共 ${DATA.length} 题 ｜ 当前 ${hit.length} 题 ｜ `
    + `已答 ${DATA.filter(q=>q.status==='answered'||q.status==='verified').length} ｜ 草稿 ${DATA.filter(q=>q.status==='draft').length} ｜ 错题 ${wrong.size} ｜ `
    + `有出现记录 ${DATA.filter(q=>(q.appearances||[]).length).length} ｜ `
    + `已自测 ${Object.keys(review).length} ｜ 今日该复习 ${dueCnt}`;

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
    review[qid] = { g: v, ts: Date.now() };
    localStorage.setItem(REV_KEY, JSON.stringify(review));
    const bar = gbtn.closest('.grade');
    bar.querySelectorAll('.gbtn').forEach(b =>
      b.classList.toggle('on', +b.dataset.v === v));
    const gs = bar.querySelector('.gstat');
    if (gs) gs.textContent = `上次自评 ${v} · ${new Date().toLocaleDateString()}`
      + (v <= 2 ? ' · 已标薄弱' : ` · ${REV_DAYS[v]} 天后复习`);
    if (v <= 2 && !wrong.has(qid)) {          // 自评不会 → 自动进错题
      wrong.add(qid);
      localStorage.setItem(WRONG_KEY, JSON.stringify([...wrong]));
    }
    render();
    return;
  }
  const head = e.target.closest('.qh');
  if (head) head.parentElement.classList.toggle('open');
});

// 复习数据备份：导出/导入 JSON（跨设备迁移用）
$('exp').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify({ wrong: [...wrong], review }, null, 1)],
    { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'interview-bank-progress.json';
  a.click();
});
$('impb').addEventListener('click', () => $('imp').click());
$('imp').addEventListener('change', e => {
  const f = e.target.files[0];
  if (!f) return;
  const rd = new FileReader();
  rd.onload = () => {
    try {
      const d = JSON.parse(rd.result);
      if (d.wrong) wrong = new Set(d.wrong);
      if (d.review) review = d.review;
      localStorage.setItem(WRONG_KEY, JSON.stringify([...wrong]));
      localStorage.setItem(REV_KEY, JSON.stringify(review));
      render();
      alert(`已导入：错题 ${wrong.size}，自测记录 ${Object.keys(review).length}`);
    } catch { alert('导入失败：不是有效的备份文件'); }
  };
  rd.readAsText(f);
});

// 支持 ?co=Momenta&rl=C&q=关键字，链接可直接分享
const _p = new URLSearchParams(location.search);
[['co','co'],['rl','rl'],['mod','mod'],['q','q']].forEach(([k, id]) => {
  const v = _p.get(k);
  if (v) $(id).value = v;
});

['q','mod','pri','st','sub','co','rl','wrong','hidepred','selftest','rev'].forEach(id => $(id).addEventListener('input', render));
$('mod').addEventListener('input', () => { refreshSubs(); render(); });
refreshSubs();
render();
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

    data = json.dumps(qs, ensure_ascii=False, separators=(",", ":"))
    out = (PAGE.replace("__DATA__", data)
               .replace("__TARGETS__", json.dumps(targets, ensure_ascii=False,
                                                 separators=(",", ":")))
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
