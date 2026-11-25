# -*- coding: utf-8 -*-
"""生成 docs/taxonomy.md：模块 / 子方向 / 题量 / 号段 一览。

用法：python tools/gen_taxonomy.py
数据源：content/**/*.md 的 frontmatter（module / sub / id）。
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "docs" / "taxonomy.md"

MODULE_NAME = {
    "project": "项目深挖", "cpp": "C++",
    "algo": "算法机考", "deploy": "模型部署", "ros2": "ROS2",
    "imaging": "医学影像", "robot": "机器人学",
    "hardware": "硬件嵌入式", "cv_pytorch": "深度学习",
    "python": "Python", "backend": "后端基础",
    "agent": "Agent 应用",
    "scene": "场景系统设计", "ai_native": "AI-Native 能力",
    "career": "薪资和路线分享", "embodied": "具身智能",
}
BASE = {"project": 100, "cpp": 600, "algo": 1600,
        "deploy": 2100, "ros2": 2600, "imaging": 3100, "robot": 3600,
        "hardware": 4100, "cv_pytorch": 4600, "python": 5100, "backend": 5600,
        "agent": 6600, "scene": 7100, "ai_native": 7600, "career": 8100,
        "embodied": 8600}
# cpp 吸收了旧 linux(1100) 号段；hardware 合并了旧 09_hardware(4100) 与 13_hardware2(6100) 两段，
# 且原 linux 的内核驱动题（11xx/15xx 段）并入 hardware 时保留原编号（2026-11-24 补）
EXTRA_BASES = {"hardware": (6100, 1100), "cpp": (1100,)}


def main() -> int:
    subs = defaultdict(Counter)
    ids = defaultdict(list)
    for p in CONTENT.rglob("*.md"):
        s = p.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^module: (\S+)", s, re.M)
        u = re.search(r"^sub: (.*)$", s, re.M)
        i = re.search(r"^id: (Q-(\d+))", s, re.M)
        if not (m and u and i):
            continue
        subs[m.group(1)][u.group(1).strip()] += 1
        ids[m.group(1)].append(int(i.group(2)))

    lines = ["# 题库分类与号段（自动生成，勿手改）", "",
             "> 由 `tools/gen_taxonomy.py` 从 `content/**/*.md` 统计生成。改完题卡的 `module` / `sub` 后重跑一次即可。", ""]
    total = sum(sum(c.values()) for c in subs.values())
    lines += [f"总题量 **{total}**，模块 {len(subs)} 个，子方向 {sum(len(c) for c in subs.values())} 个。", ""]

    lines += ["## 一、模块与号段", "",
              "| 模块 | 目录 | 名称 | 题量 | 号段 | 已用 | 余量 | 子方向数 |",
              "|---|---|---|---|---|---|---|---|"]
    for mod in sorted(subs):
        used = len(ids[mod])
        segs = [(BASE[mod] + 1, BASE[mod] + 499)] + \
               [(b + 1, b + 499) for b in EXTRA_BASES.get(mod, ())]
        seg_txt = " / ".join(f"{a}–{z}" for a, z in segs)
        capacity = 499 * len(segs)
        lines.append(f"| `{mod}` | `content/{mod}/` | {MODULE_NAME.get(mod, mod)} | {used} | "
                     f"{seg_txt} | {used} | {capacity - used} | {len(subs[mod])} |")
    lines.append("")

    lines += ["## 二、子方向与题量", ""]
    for mod in sorted(subs):
        lines.append(f"### {MODULE_NAME.get(mod, mod)}（`{mod}`，{sum(subs[mod].values())} 题）")
        lines.append("")
        lines.append("| 子方向 | 题量 |")
        lines.append("|---|---|")
        for k, v in subs[mod].most_common():
            lines.append(f"| {k} | {v} |")
        lines.append("")

    lines += ["## 三、维护规则", "",
              "1. **新题先找归属**：优先并入已有子方向；只有当某类题超过 25 道且考点明显不同时，才新开子方向。",
              "2. **子方向粒度**：一个子方向 10–60 道为宜。低于 5 道的合并到相邻方向；超过 80 道的考虑拆分。",
              "3. **硬件号段**：主段 4101–4599 已满，续段 6101–6599（原 13_hardware2 并入 hardware）。再进硬件题的顺序：",
              "   - 先**并题**：把新考点写成现有卡片的「高频追问」或「讲深一层」，不新增题卡；",
              "   - 确需新卡时先进续段 6101–6599；号段全满再扩号段——扩号段必须整体后移后续模块，并同步改 `tools/validate.py` 的 `ID_BASE/SPAN` 与 `tools/gen_taxonomy.py` 的 `BASE`。",
              "4. **改子方向**：只改题卡 frontmatter 的 `sub`，不要动文件名；`id` 只在跨模块迁移时重编。",
              ""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"写入 {OUT}：{total} 题 / {len(subs)} 模块")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
