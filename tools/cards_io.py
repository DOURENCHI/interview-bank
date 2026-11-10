#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补答案用的纯文本卡格式读写。

为什么不用 .py 存题目内容：
    题干和答案里全是中文引号、反引号、代码块，写成 Python 字符串要不停转义，
    一处漏了就整份脚本语法错误（已经踩过）。改成纯文本后正文里出现什么都不用管。

格式（`@@ 题号` 起一张卡，`@节名` 起一节）：

    @@ Q-2601
    @STEM
    背景 / 场景 / 问
    @ANSWER
    口述答案
    @DEEP
    讲深一层（可含代码块、表格）
    @FOLLOW
    1. ...
    @TRAPS
    - ...
    @RELATED
    - ...
    @SOURCE
    ...

用法：
    python tools/apply_cards.py tools/cards/ros2_a.cards
    python tools/apply_cards.py --dry tools/cards/*.cards
"""
from __future__ import annotations

import re
from pathlib import Path

KEYS = {
    "STEM": "stem", "ANSWER": "answer", "DEEP": "deep",
    "FOLLOW": "follow", "TRAPS": "traps",
    "RELATED": "related", "SOURCE": "source",
    "APPEAR": "appearances",
}
_LIST_KEYS = {"follow", "traps", "related"}


def _appearance_rows(body: str) -> list[dict]:
    """APPEAR 节：每行 `日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度`。"""
    rows = []
    for ln in body.splitlines():
        ln = ln.strip().lstrip("-").strip()
        if not ln:
            continue
        parts = [x.strip() for x in ln.split("|")]
        while len(parts) < 6:
            parts.append("")
        rows.append(dict(zip(("日期", "公司", "岗位", "轮次", "来源", "可信度"), parts)))
    return rows


def parse(text: str) -> list[dict]:
    cards: list[dict] = []
    cur: dict | None = None
    key: str | None = None
    buf: list[str] = []

    def flush_section() -> None:
        nonlocal buf, key
        if cur is None or key is None:
            buf = []
            return
        body = "\n".join(buf).strip("\n")
        if key == "appearances":
            cur[key] = _appearance_rows(body)
        elif key in _LIST_KEYS:
            items = []
            for ln in body.splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                items.append(re.sub(r"^(?:[-·]|\d+[.)])\s*", "", ln))
            cur[key] = items
        else:
            cur[key] = body
        buf = []

    for line in text.splitlines():
        m = re.match(r"^@@\s+(Q-\d+)\s*$", line)
        if m:
            flush_section()
            if cur:
                cards.append(cur)
            cur = {"id": m.group(1)}
            key = None
            continue
        m = re.match(r"^@([A-Z]+)\s*$", line)
        if m and m.group(1) in KEYS:
            flush_section()
            key = KEYS[m.group(1)]
            continue
        if key is not None:
            buf.append(line)

    flush_section()
    if cur:
        cards.append(cur)
    return cards


def load(path: str | Path) -> list[dict]:
    return parse(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    import argparse
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import fill  # noqa: PLC0415

    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    total = ok = 0
    for f in args.files:
        cards = load(f)
        total += len(cards)
        if args.dry:
            for c in cards:
                miss = {"stem", "answer"} - set(c)
                flag = "缺字段" + ",".join(miss) if miss else "OK"
                print(f"  {c['id']}  {flag}")
            continue
        ok += fill.batch(cards)

    if args.dry:
        print(f"\n共 {total} 张（--dry，未写入）")
    else:
        print(f"\n共 {total} 张，成功 {ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
