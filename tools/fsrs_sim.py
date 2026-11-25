# -*- coding: utf-8 -*-
"""G3 复习调度模拟：固定间隔表（现版）vs FSRS。

两种模式：
  python tools/fsrs_sim.py --demo              合成学习曲线（每天新学 12 张，评分 Good）
  python tools/fsrs_sim.py --backup x.json     读题库「导出备份」（backupPayload 结构
                                               data.review = {qid: {score, due, ...}}），
                                               按每张卡当前自评分模拟未来 30 天负载。

固定间隔表与 tools/build.py 的 REV_DAYS 一致：{1:1, 2:3, 3:7, 4:21}（grade→隔几天再考）。
FSRS 用 open-spaced-repetition 的 py-fsrs（pip install fsrs，MIT）；未安装时提示退化。

输出为纯文本表，可直接贴进周报（周检 A4/G4 的负载预测节）。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta

REV_DAYS = {1: 1, 2: 3, 3: 7, 4: 21}
DAYS = 30
NEW_PER_DAY = 12  # 今日训练容量


def _fsrs_available():
    try:
        import fsrs  # noqa: F401
        return True
    except ImportError:
        return False


def _fsrs_rating(score: int):
    """题库自评分 1-4 → FSRS Rating 1-4（Again/Hard/Good/Easy）。"""
    from fsrs import Rating
    return {1: Rating.Again, 2: Rating.Hard, 3: Rating.Good, 4: Rating.Easy}[score]


def simulate_fixed(scores: list[int]) -> list[int]:
    """固定间隔表：每张卡从今天起按 grade 间隔反复到期，返回 30 天每日到期数。"""
    load = [0] * DAYS
    today = date.today()
    for g in scores:
        d = REV_DAYS.get(g, 3)
        day = (today + timedelta(days=d) - today).days
        while day < DAYS:
            load[day] += 1
            day += REV_DAYS.get(g, 3)
    return load


def simulate_fsrs(scores: list[int]) -> list[int] | None:
    """FSRS：按自评分初始化卡片，模拟 30 天复习负载。"""
    if not _fsrs_available():
        return None
    from fsrs import Card, Scheduler
    sched = Scheduler()
    cards = []
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)  # py-fsrs 要求带 tzinfo 的 UTC datetime
    for g in scores:
        c = Card()
        try:
            c, _ = sched.review_card(c, _fsrs_rating(g), today)
        except TypeError:  # 旧版 py-fsrs 的 review_card 不收日期
            c, _ = sched.review_card(c, _fsrs_rating(g))
        cards.append(c)
    load = [0] * DAYS
    for day_i in range(DAYS):
        d = today + timedelta(days=day_i)
        due_today = [c for c in cards if c.due <= d]
        for _ in due_today:
            load[day_i] += 1
        for c in due_today:
            try:
                c2, _ = sched.review_card(c, _fsrs_rating(3), d)
            except TypeError:
                c2, _ = sched.review_card(c, _fsrs_rating(3))
            cards[cards.index(c)] = c2
    return load


def _table(rows: list[tuple], headers: list[str]) -> str:
    out = " | ".join(headers)
    out += "\n" + "-" * len(out)
    for r in rows:
        out += "\n" + " | ".join(str(x) for x in r)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--demo", action="store_true", help="合成学习曲线模拟")
    ap.add_argument("--backup", help="题库导出备份 JSON 路径")
    args = ap.parse_args()

    if args.backup:
        with open(args.backup, encoding="utf-8") as f:
            data = json.load(f)
        review = (data.get("data") or {}).get("review") or data.get("review") or {}
        scores = [int(v.get("score") or 3) for v in review.values() if isinstance(v, dict)]
        print(f"备份内复习卡：{len(scores)} 张（按当前自评分初始化）")
    elif args.demo:
        scores = []
        for d in range(DAYS):
            scores += [3] * NEW_PER_DAY  # 每天新学 12 张，首评 Good
        print(f"合成场景：每天新学 {NEW_PER_DAY} 张（首评 Good），共 {DAYS} 天累计 {len(scores)} 张")
    else:
        ap.error("需要 --demo 或 --backup")

    fixed = simulate_fixed(scores)
    fsrs = simulate_fsrs(scores)
    if fsrs is None:
        print("未安装 py-fsrs（pip install fsrs），仅输出固定间隔表现状：")
        print(_table([(f"D+{i+1}", fixed[i]) for i in range(DAYS) if fixed[i]], ["日", "到期数"]))
        return 0

    rows = [(f"D+{i+1}", fixed[i], fsrs[i]) for i in range(DAYS)]
    print(_table([r for r in rows if r[1] or r[2]], ["日", "固定间隔", "FSRS"]))
    tf, ts = sum(fixed), sum(fsrs)
    pf, ps = max(fixed), max(fsrs)
    print(f"\n30 天总复习量：固定间隔 {tf} 张 / FSRS {ts} 张；单日峰值 {pf} / {ps}")
    print("解读：FSRS 前期负载通常更高（间隔初期更短），但按记忆状态分配、长期更省——")
    print("决策仍在你：先用 py-fsrs 模拟观察 2-3 周，负载可接受再考虑前端切换（A1 前端版）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
