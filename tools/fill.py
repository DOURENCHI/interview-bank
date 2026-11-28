#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补答案的公共写卡器。

统一六节结构与口述稿体，避免每个补答案脚本各写一套模板。
写卡规则：
  · 前端字段（id/module/sub/priority/source_ref…）原样保留，只改 status / verified_at
  · 正文整体重写，固定节序：题目 → 口述答案 → 讲深一层 → 高频追问 → 易错点 → 关联项目 → 来源
  · 项目深挖（qtype: project）不写「来源」，与既有约定一致
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TODAY = "2026-11-28"


def _find(qid: str) -> Path:
    hits = list(CONTENT.rglob(f"{qid}-*.md")) + list(CONTENT.rglob(f"{qid}.md"))
    if not hits:
        raise FileNotFoundError(f"找不到题卡 {qid}")
    return hits[0]


def _bullets(items: list[str], mark: str = "·") -> str:
    return "\n".join(f"- {mark} {x}" if mark != "·" else f"- {x}" for x in items)


def _numbered(items: list[str]) -> str:
    return "\n".join(f"{i}. {x}" for i, x in enumerate(items, 1))


def oral(text: str) -> str:
    """口述答案统一走引用块：这是「面试时能直接说出口的话」。"""
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    return "\n".join("> " + ln for ln in lines)


def _appearance_table(rows: list[dict]) -> str:
    """出现记录表：只在有真实面经时由调用方传入。"""
    head = "| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |"
    sep = "|---|---|---|---|---|---|"
    body = "\n".join(
        f"| {r.get('日期','')} | {r.get('公司','')} | {r.get('岗位','')} | "
        f"{r.get('轮次','')} | {r.get('来源','')} | {r.get('可信度','社区经验')} |"
        for r in rows)
    return "\n".join([head, sep, body])


def write(
    qid: str,
    *,
    stem: str,
    answer: str,
    deep: str = "",
    follow: list[str] | None = None,
    traps: list[str] | None = None,
    related: list[str] | None = None,
    source: str = "",
    difficulty: int | None = None,
    priority: str | None = None,
    appearances: list[dict] | None = None,
) -> bool:
    """写一张已答题卡。stem 是「题目」节正文（背景 / 场景 / 问）。"""
    path = _find(qid)
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 3)
    if end < 0:
        raise ValueError(f"{path} 前端格式异常")
    fm = text[: end + 4]
    qtype = (re.search(r"^qtype: (\S+)", fm, re.M) or [None, ""])[1]

    fm = re.sub(r"^status: .*$", "status: answered", fm, count=1, flags=re.M)
    fm = re.sub(r"^verified_at: .*$", f"verified_at: {TODAY}", fm, count=1, flags=re.M)
    if difficulty is not None:
        fm = re.sub(r"^difficulty: .*$", f"difficulty: {difficulty}", fm, count=1, flags=re.M)
    if priority is not None:
        fm = re.sub(r"^priority: .*$", f"priority: {priority}", fm, count=1, flags=re.M)
    # 索引期的 hint 已被正文取代
    fm = re.sub(r"^hint: .*\n", "", fm, count=1, flags=re.M)

    parts = ["## 题目", "", stem.strip(), "", "## 口述答案", "", oral(answer)]
    if deep.strip():
        parts += ["", "## 讲深一层", "", deep.strip()]
    parts += ["", "## 高频追问", "",
              _numbered(follow) if follow else "1. 待补充"]
    parts += ["", "## 易错点", "", _bullets(traps) if traps else "- 待补充"]
    if appearances:
        parts += ["", "## 出现记录", "", _appearance_table(appearances)]
    parts += ["", "## 关联项目", "",
              _bullets(related) if related else "- 无（通用八股，不绑定具体项目）"]
    if qtype != "project":
        parts += ["", "## 来源", "", source.strip() or
                  "领域通用知识整理（预测题，非真实面经）"]

    path.write_text(fm + "\n\n" + "\n".join(parts) + "\n", encoding="utf-8")
    return True


def batch(cards: list[dict]) -> int:
    """批量写卡，返回成功条数。缺 id 或文件不存在会打印出来，不中断。"""
    ok = 0
    for c in cards:
        c = dict(c)
        qid = c.pop("id")
        try:
            write(qid, **c)
            ok += 1
        except Exception as exc:                      # noqa: BLE001
            print(f"  ✗ {qid}: {exc}")
    print(f"写入 {ok}/{len(cards)} 张")
    return ok


def pending(module: str) -> list[tuple[str, str]]:
    """列出某模块还没答的题（id, title），供补答案脚本对表。"""
    out = []
    for f in sorted((CONTENT / module).glob("Q-*.md")):
        s = f.read_text(encoding="utf-8")
        if re.search(r"^status: indexed", s, re.M):
            m = re.search(r"^id: (\S+)", s, re.M)
            t = re.search(r"^title: (.+)$", s, re.M)
            out.append((m.group(1), t.group(1)))
    return out
