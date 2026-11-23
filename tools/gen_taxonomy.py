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
    "01_project": "项目深挖", "02_cpp": "C++", "03_linux": "Linux",
    "04_algo": "算法机考", "05_deploy": "模型部署", "06_ros2": "ROS2",
    "07_imaging": "医学影像", "08_robot": "机器人学",
    "09_hardware": "硬件嵌入式", "10_cv_pytorch": "深度学习",
    "11_python": "Python", "12_backend": "后端基础",
    "13_hardware2": "硬件嵌入式·续",
}
BASE = {"01_project": 100, "02_cpp": 600, "03_linux": 1100, "04_algo": 1600,
        "05_deploy": 2100, "06_ros2": 2600, "07_imaging": 3100, "08_robot": 3600,
        "09_hardware": 4100, "10_cv_pytorch": 4600, "11_python": 5100, "12_backend": 5600,
        "13_hardware2": 6100}


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
        lines.append(f"| `{mod}` | `content/{mod}/` | {MODULE_NAME.get(mod, mod)} | {used} | "
                     f"{BASE[mod] + 1}–{BASE[mod] + 499} | {used} | {500 - used} | {len(subs[mod])} |")
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
              "3. **硬件题号段已满**（4101–4599 用尽）。再进硬件题的顺序：",
              "   - 先**并题**：把新考点写成现有卡片的「高频追问」或「讲深一层」，不新增题卡；",
              "   - 确需新卡时，先删/并低价值卡腾号，或**扩号段**——扩号段必须整体后移 `10_cv_pytorch` 及其后所有模块，并同步改 `tools/validate.py` 的 `ID_BASE/SPAN` 与 `tools/gen_taxonomy.py` 的 `BASE`。",
              "4. **改子方向**：只改题卡 frontmatter 的 `sub`，不要动文件名；`id` 只在跨模块迁移时重编。",
              ""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"写入 {OUT}：{total} 题 / {len(subs)} 模块")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
