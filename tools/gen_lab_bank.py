# -*- coding: utf-8 -*-
"""把题库里的 C++ / Python 题导出成两个实验台目录下的「题库」页。

产出：
    D:/工程/教学文档/C++实验台/C++题库.html      （cpp 全部）
    D:/工程/教学文档/Python实验台/Python题库.html （python + algo 的 Python 语言细节）

设计：
- 单文件、零外部依赖，风格沿用实验台的浅蓝灰（不套暖纸模板）。
- 按新分类的 sub 做筛选，带搜索、题量统计、折叠答案。
- 已在实验台「读程序写结果」区的题打标记（按标题比对）。
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402

LAB = Path(r"D:/工程/教学文档")

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{
  --bg:#EDF1F6; --card:#FFFFFF; --line:#D5DEEA; --tx:#16202E; --tx2:#405066;
  --muted:#6B7A90; --accent:#2B6CB0; --soft:#E3EAF3; --ok:#1F7A4D; --warn:#A85B00;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);
  font:15px/1.75 -apple-system,"Segoe UI","Microsoft YaHei",system-ui,sans-serif}
a{color:var(--accent);text-decoration:none}
.wrap{max-width:1080px;margin:0 auto;padding:26px 22px 60px}
header{border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:18px}
.kicker{font:12px/1.6 ui-monospace,Consolas,monospace;color:var(--muted);letter-spacing:.5px}
h1{margin:6px 0 8px;font-size:28px;letter-spacing:-.3px}
h1 .n{color:var(--accent)}
.lede{margin:0;color:var(--tx2);font-size:14px}
.back{display:inline-block;margin-top:10px;font-size:13px;border:1px solid var(--line);
  background:var(--card);border-radius:8px;padding:5px 12px}
.toolbar{position:sticky;top:0;z-index:5;background:var(--bg);padding:12px 0;
  border-bottom:1px solid var(--line);margin-bottom:14px}
.search{width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:9px;
  background:var(--card);font:14px inherit;color:var(--tx);outline:none}
.search:focus{border-color:var(--accent)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.chip{font:12.5px/1.6 inherit;border:1px solid var(--line);background:var(--card);
  color:var(--tx2);border-radius:999px;padding:4px 11px;cursor:pointer}
.chip:hover{border-color:var(--accent)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
.chip b{font-weight:600;opacity:.85}
.meta{display:flex;align-items:center;gap:12px;margin-top:10px;color:var(--muted);font-size:12.5px}
.q{background:var(--card);border:1px solid var(--line);border-radius:11px;margin:10px 0;
  overflow:hidden}
.q>summary{cursor:pointer;padding:12px 16px;list-style:none;display:flex;gap:10px;
  align-items:baseline;flex-wrap:wrap}
.q>summary::-webkit-details-marker{display:none}
.q[open]>summary{border-bottom:1px dashed var(--line);background:#F7FAFD}
.qid{font:12px/1.6 ui-monospace,Consolas,monospace;color:var(--muted)}
.qt{font-weight:600;font-size:15px;flex:1;min-width:220px;display:flex;flex-direction:column;gap:2px}
.qp{font:12px/1.5 ui-monospace,Consolas,monospace;color:var(--muted);font-weight:400;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.b{font-size:11px;border-radius:5px;padding:1px 7px;border:1px solid var(--line);
  color:var(--muted);background:var(--soft);white-space:nowrap}
.b.sub{color:var(--accent);border-color:#BBD0E8;background:#EAF2FB}
.b.p0{color:#A63A2E;border-color:#E5C0B8;background:#FBEFEC}
.b.lab{color:var(--ok);border-color:#BFDCCB;background:#EDF7F1}
.qbody{padding:6px 18px 16px}
.sec{margin:12px 0}
.lbl{font:12px/1.6 ui-monospace,Consolas,monospace;color:var(--muted);
  letter-spacing:.5px;margin-bottom:4px}
.sec blockquote{margin:0;padding:8px 12px;border-left:3px solid var(--accent);
  background:#F4F8FC;border-radius:0 6px 6px 0}
.sec pre{background:#0F1726;color:#E6EDF7;padding:12px 14px;border-radius:8px;
  overflow:auto;font-size:12.5px}
.sec code{background:var(--soft);border-radius:4px;padding:1px 5px;font-size:.92em}
.sec pre code{background:none;padding:0}
.sec table{border-collapse:collapse;width:100%;font-size:13.5px;margin:8px 0}
.sec th,.sec td{border:1px solid var(--line);padding:6px 9px;text-align:left}
.sec th{background:var(--soft)}
.sec ul,.sec ol{margin:6px 0;padding-left:22px}
.sec img{max-width:100%}
details.sub{margin:8px 0;border:1px solid var(--line);border-radius:8px;background:#FBFCFE}
details.sub>summary{cursor:pointer;padding:7px 12px;font-size:13px;color:var(--tx2)}
details.sub>div{padding:2px 12px 10px}
.empty{padding:40px;text-align:center;color:var(--muted)}
footer{margin-top:26px;color:var(--muted);font-size:12.5px;border-top:1px solid var(--line);
  padding-top:14px}
@media (max-width:700px){.wrap{padding:18px 14px 40px}h1{font-size:22px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="kicker">__KICKER__</div>
  <h1>__H1__ <span class="n">__COUNT__ 题</span></h1>
  <p class="lede">__LEDE__</p>
  <a class="back" href="__BACK__">← 返回主实验台</a>
  <a class="back" href="index.html">← 目录索引</a>
</header>

<div class="toolbar">
  <input class="search" id="q" type="search" placeholder="搜题号、标题、关键词…">
  <div class="chips" id="chips"></div>
  <div class="meta"><span id="cnt"></span><span>·</span><span>点标题展开答案</span></div>
</div>

<main id="list"></main>

<footer>
  数据来自面试题库 <code>content/</code>（构建时导出，非手写）：__SRC__。
  分类按题库的 <code>sub</code> 字段，与实验台原有的「九大主题」是两套体系，互不替代。
</footer>
</div>

<script>
const DATA = __DATA__;
const $ = id => document.getElementById(id);
let CUR = '';

function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}

function chips(){
  const m = new Map();
  DATA.forEach(q => m.set(q.sub, (m.get(q.sub)||0)+1));
  const rows = [...m.entries()].sort((a,b)=>b[1]-a[1]);
  $('chips').innerHTML = `<button class="chip on" data-s="">全部 <b>${DATA.length}</b></button>`
    + rows.map(([s,n])=>`<button class="chip" data-s="${esc(s)}">${esc(s)} <b>${n}</b></button>`).join('');
}

function render(){
  const kw = $('q').value.trim().toLowerCase();
  let n = 0;
  document.querySelectorAll('#list .q').forEach(el => {
    const ok = (!CUR || el.dataset.sub === CUR)
      && (!kw || el.dataset.k.includes(kw));
    el.hidden = !ok;
    if (ok) n++;
    if (!ok) el.open = false;
  });
  $('cnt').textContent = `显示 ${n} / ${DATA.length}`;
}

$('chips').addEventListener('click', e => {
  const b = e.target.closest('.chip'); if (!b) return;
  CUR = b.dataset.s || '';
  document.querySelectorAll('#chips .chip').forEach(x => x.classList.toggle('on', x === b));
  render();
});
$('q').addEventListener('input', render);

(function init(){
  $('list').innerHTML = DATA.map(q => `
    <details class="q" data-sub="${esc(q.sub)}" data-k="${esc((q.id+' '+q.title+' '+q.plain).toLowerCase())}">
      <summary>
        <span class="qid">${esc(q.id)}</span>
        <span class="qt">${esc(q.title)}<span class="qp">${esc(q.preview)}</span></span>
        <span class="b sub">${esc(q.sub)}</span>
        <span class="b ${q.priority==='P0'?'p0':''}">${esc(q.priority)}</span>
        ${q.inLab ? '<span class="b lab">读程序区已收录</span>' : ''}
      </summary>
      <div class="qbody">${q.html}</div>
    </details>`).join('');
  chips(); render();
})();
</script>
</body>
</html>
"""


def load(module_pred) -> list[dict]:
    out = []
    for q in build.load_questions():
        if not module_pred(q):
            continue
        out.append(q)
    cnt = {}
    for q in out:
        cnt[q["sub"]] = cnt.get(q["sub"], 0) + 1
    out.sort(key=lambda q: (-cnt[q["sub"]], q["sub"], q["id"]))
    return out


def preview_of(q: dict, stem_html: str) -> str:
    m = re.search(r"<pre><code[^>]*>(.*?)</code></pre>", stem_html, re.S)
    if m:
        line = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip().splitlines()
        return (line[0] if line else "")[:70]
    txt = html.unescape(re.sub(r"<[^>]+>", " ", stem_html))
    return re.sub(r"\s+", " ", txt).strip()[:70]


def card_html(q: dict) -> str:
    """把 build 产出的整篇 html 拆成 题目 / 口述答案 / 折叠小节。"""
    parts = re.split(r"<h2>(.*?)</h2>", q["html"])
    # parts = ['', '题目', '<p>..', '口述答案', '<blockquote>..', ...]
    sec = {}
    for i in range(1, len(parts) - 1, 2):
        sec[parts[i].strip()] = parts[i + 1].strip()
    stem = sec.get("题目", "")
    ans = sec.get("口述答案", "")
    rest = []
    for name in ("讲深一层", "高频追问", "易错点", "关联项目", "来源"):
        if sec.get(name):
            if name == "来源":
                continue
            rest.append(f'<details class="sub"><summary>{name}</summary><div>{sec[name]}</div></details>')
    body = ""
    if stem:
        body += f'<div class="sec"><div class="lbl">题目</div>{stem}</div>'
    if ans:
        body += f'<div class="sec"><div class="lbl">口述答案</div>{ans}</div>'
    body += "".join(rest)
    return body


def lab_titles(path: Path) -> set[str]:
    if not path.exists():
        return set()
    d = json.loads(path.read_text(encoding="utf-8"))
    out = set()
    for q in d.get("quiz", []):
        t = q.get("title") or q.get("t") or ""
        out.add(re.sub(r"\s+", "", t))
    return out


def build_page(cfg: dict) -> Path:
    qs = load(cfg["pred"])
    lab = lab_titles(cfg["lab_data"])
    data = []
    for q in qs:
        data.append({
            "id": q["id"], "title": q["title"], "sub": q["sub"],
            "priority": q["priority"], "plain": q["plain"][:600],
            "html": card_html(q),
            "preview": preview_of(q, card_html(q)),
            "inLab": cfg["mark"](q),
        })
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    page = (PAGE.replace("__TITLE__", cfg["title"])
                .replace("__KICKER__", cfg["kicker"])
                .replace("__H1__", cfg["h1"])
                .replace("__COUNT__", str(len(data)))
                .replace("__LEDE__", cfg["lede"])
                .replace("__BACK__", cfg["back"])
                .replace("__SRC__", cfg["src"])
                .replace("__DATA__", payload))
    out = LAB / cfg["out"]
    out.write_text(page, encoding="utf-8")
    print(f"{out}  {len(data)} 题  {out.stat().st_size/1024:.0f} KB  已收录标记 {sum(1 for x in data if x['inLab'])}")
    return out


def main() -> int:
    build_page({
        "pred": lambda q: q["module"] == "cpp",
        "out": "C++实验台/C++题库.html",
        "title": "C++ 题库 · 251 题（按新分类）",
        "kicker": "// 面试题库 · cpp · 与实验台同一套浅蓝灰",
        "h1": "C++ 题库",
        "lede": "题库里 <b>cpp</b> 的全部题，按新的子方向分类（指针与内存 / 类型与语义 / 对象模型 / 模板与泛型 / "
                "STL 容器 / 并发与多线程 / 编译链接 / 工程化与 SDK / Qt 与 GUI / 时间与算法）。"
                "实验台原来的 62 道读程序题属于 algo 的「C++语言细节」，不在这 251 道里——两套互为补充："""
                "读程序练手，这里补概念面。",
        "back": "C++考点实验台.html",
        "lab_data": LAB / "C++实验台/_work/data.json",
        "mark": lambda q: False,
        "src": "cpp 全部",
    })
    build_page({
        "pred": lambda q: q["module"] == "python" or (q["module"] == "algo" and q["sub"] in
                                                          ("语法与类型", "容器与切片", "函数与异常", "并发与性能")),
        "out": "Python实验台/Python题库.html",
        "title": "Python 题库 · 155 题（按新分类）",
        "kicker": "// 面试题库 · python + algo · 与实验台同一套浅蓝灰",
        "h1": "Python 题库",
        "lede": "题库里 <b>python</b> 的 40 道语言机制题，加上 <b>algo</b> 的 115 道 Python 语言细节题，"
                "按新分类（语法与类型 / 容器与切片 / 函数与异常 / 并发与性能 / 语言机制 / 性能与工程等）。"
                "其中 115 道就是实验台「读程序写结果」区的原题，已标「读程序区已收录」；另外 40 道是新补的语言机制题。",
        "back": "Python考点实验台.html",
        "lab_data": LAB / "Python实验台/_work/data.json",
        "mark": lambda q: q["module"] == "algo",
        "src": "python 40 题 + algo Python 语言细节 115 题",
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
