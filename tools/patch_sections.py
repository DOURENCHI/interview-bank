# -*- coding: utf-8 -*-
"""只替换题卡的指定小节（讲深一层 / 高频追问 / 易错点），其余正文不动。

cards 文件格式：
    @@ Q-1613
    @DEEP
    ...
    @FOLLOW
    1. ...
    @TRAPS
    - ...

用法：python tools/patch_sections.py tools/cards/_fix_algo_a.cards [...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TODAY = "2026-11-21"
KEYS = {"DEEP": "讲深一层", "FOLLOW": "高频追问", "TRAPS": "易错点"}


def parse(path: Path) -> list[dict]:
    cards, cur, key, buf = [], None, None, []

    def flush():
        nonlocal buf
        if cur is not None and key is not None:
            cur.setdefault("secs", {})[key] = "\n".join(buf).strip()
        buf = []

    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^@@\s+(Q-\d+)\s*$", line)
        if m:
            flush()
            if cur:
                cards.append(cur)
            cur, key = {"id": m.group(1)}, None
            continue
        m = re.match(r"^@([A-Z]+)\s*$", line)
        if m and m.group(1) in KEYS:
            flush()
            key = KEYS[m.group(1)]
            continue
        if key is not None:
            buf.append(line)
    flush()
    if cur:
        cards.append(cur)
    return cards


def find(qid: str) -> Path | None:
    hits = list(CONTENT.rglob(f"{qid}-*.md")) + list(CONTENT.rglob(f"{qid}.md"))
    return hits[0] if hits else None


def patch(qid: str, secs: dict[str, str]) -> bool:
    p = find(qid)
    if not p:
        print(f"  ✗ {qid}: 找不到题卡")
        return False
    text = p.read_text(encoding="utf-8")
    for name, body in secs.items():
        if not body.strip():
            continue
        pat = re.compile(rf"(## {name}\n\n).*?(?=\n## |\Z)", re.S)
        if not pat.search(text):
            print(f"  ✗ {qid}: 缺小节 {name}")
            continue
        text = pat.sub(lambda m: m.group(1) + body.strip() + "\n", text, count=1)
    text = re.sub(r"^verified_at: .*$", f"verified_at: {TODAY}", text, count=1, flags=re.M)
    p.write_text(text, encoding="utf-8")
    return True


def main(paths: list[str]) -> int:
    ok = total = 0
    for f in paths:
        cards = parse(Path(f))
        total += len(cards)
        for c in cards:
            if patch(c["id"], c.get("secs", {})):
                ok += 1
        print(f"{f}: {len(cards)} 张")
    print(f"共 {total} 张，成功 {ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
