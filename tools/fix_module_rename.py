# -*- coding: utf-8 -*-
"""V2.10 模块改名收尾：把数据文件与公司笔记里残留的旧模块名换成新名。

背景：模块目录 git mv 改名（01_project→project 等）时，批量替换只覆盖了
content/*/frontmatter 和 tools/*.py；sources/、companies/ 下的数据文件没扫到。
后果：宝典地图章节 rule["modules"] 查不到题（ids 空 → ui_test 超时）、
岗位族 weights 旧键查不到（岗位准备度/今日训练权重全 0）。

映射表与 tools/validate.py ID_BASE、build.py MODULE_NAME 保持一致。
旧名只改「活数据」；CHANGELOG/历史脚本的旧名是历史记录，有意保留。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 长键在前，避免前缀误替换
RENAME = [
    ("13_hardware2", "hardware"),
    ("10_cv_pytorch", "cv_pytorch"),
    ("01_project", "project"),
    ("02_cpp", "cpp"),
    ("03_linux", "linux"),
    ("04_algo", "algo"),
    ("05_deploy", "deploy"),
    ("06_ros2", "ros2"),
    ("07_imaging", "imaging"),
    ("08_robot", "robot"),
    ("09_hardware", "hardware"),
    ("11_python", "python"),
    ("12_backend", "backend"),
    ("14_agent", "agent"),
]

JSON_FILES = [
    ROOT / "sources" / "tutorial_map.json",
    ROOT / "companies" / "job_profiles.json",
    ROOT / "companies" / "targets.json",
    ROOT / "sources" / "douyin_candidates.json",
    ROOT / "sources" / "douyin_candidates_b2.json",
    ROOT / "sources" / "douyin_candidates_b3.json",
]

# 公司笔记（含 README），纯文档，裸词替换即可
MD_FILES = sorted((ROOT / "companies").glob("*.md"))

TOKEN = re.compile(
    r"(01_project|02_cpp|03_linux|04_algo|05_deploy|06_ros2|07_imaging|"
    r"08_robot|09_hardware|10_cv_pytorch|11_python|12_backend|13_hardware2|14_agent)"
)


def new_name(m: re.Match) -> str:
    old = m.group(1)
    for a, b in RENAME:
        if a == old:
            return b
    return old


def fix_json(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    n = len(TOKEN.findall(text))
    if n == 0:
        return 0
    out = TOKEN.sub(new_name, text)
    json.loads(out)  # 改完必须仍是合法 JSON（重复键也能解析，但先保证语法）
    p.write_text(out, encoding="utf-8")
    return n


def fix_md(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    n = len(TOKEN.findall(text))
    if n == 0:
        return 0
    p.write_text(TOKEN.sub(new_name, text), encoding="utf-8")
    return n


def check_weights(p: Path) -> None:
    """改完后确认没有 profile 出现重复权重键（如 09/13 都映射到 hardware）。"""
    data = json.loads(p.read_text(encoding="utf-8"))
    for prof in data.get("profiles", []):
        w = prof.get("weights") or {}
        # json 解析后同键自动去重，只能从原文检查：逐行找 weights 行
    text = p.read_text(encoding="utf-8")
    for line in text.splitlines():
        if '"weights"' in line:
            keys = re.findall(r'"([a-z0-9_]+)"\s*:', line.split("{", 1)[1])
            if len(keys) != len(set(keys)):
                raise SystemExit(f"重复权重键：{line.strip()}")


def main() -> None:
    total = 0
    for p in JSON_FILES:
        if p.exists():
            n = fix_json(p)
            print(f"{p.relative_to(ROOT)}: {n} 处")
            total += n
    check_weights(ROOT / "companies" / "job_profiles.json")
    for p in MD_FILES:
        n = fix_md(p)
        if n:
            print(f"{p.relative_to(ROOT)}: {n} 处")
            total += n
    print(f"合计 {total} 处旧模块名已替换")


if __name__ == "__main__":
    main()
