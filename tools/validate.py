#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题卡校验。CI 里跑这个，不通过就别发布。

检查项：
  1. ID 唯一，且落在自己模块的号段内（曾发生 C++ 编号越界撞进 Linux 段）
  2. 必填字段齐全、取值合法
  3. 六个正文小节齐全
  4. status=answered 时答案不能还是「待补充」
  5. 标题必须是问句（否则提醒改写）
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

ID_BASE = {"01_project": 100, "02_cpp": 600, "03_linux": 1100, "04_algo": 1600,
           "05_deploy": 2100, "06_ros2": 2600, "07_imaging": 3100,
           "08_robot": 3600, "09_hardware": 4100, "10_cv_pytorch": 4600,
           "11_python": 5100}
SPAN = 500
REQUIRED = ["id", "title", "module", "priority", "difficulty", "status",
            "source_type", "source_ref", "tags"]
VALID_PRI = {"P0", "P1", "P2"}
VALID_STATUS = {"indexed", "draft", "answered", "verified"}
VALID_SRC = {"self_doc", "self_exp", "upstream", "official", "inferred"}
SECTIONS = ["口述答案", "讲深一层", "高频追问", "易错点", "关联项目", "来源"]
# 代码题型额外要求题面小节
CODING_SECTIONS = ["题目"]


def parse_fm(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    meta = {}
    for line in text[3:end].splitlines():
        line = line.rstrip()
        if line and ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            v = re.sub(r"\s+#.*$", "", v).strip()
            meta[k.strip()] = v.strip().strip('"\'')
    return meta, text[end + 4:]


def main() -> int:
    errors: list[str] = []
    warns: list[str] = []
    by_id: dict[str, list[Path]] = defaultdict(list)
    n = 0

    for f in sorted(CONTENT.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        meta, body = parse_fm(text)
        if not meta.get("id"):
            errors.append(f"{f}: 缺少 id")
            continue
        n += 1
        qid, mod = meta["id"], meta.get("module", "")
        by_id[qid].append(f)

        # 字段
        for k in REQUIRED:
            if k not in meta or not str(meta[k]).strip():
                errors.append(f"{qid}: 缺字段 {k}")
        if meta.get("priority") not in VALID_PRI:
            errors.append(f"{qid}: priority 非法 → {meta.get('priority')}")
        if meta.get("status") not in VALID_STATUS:
            errors.append(f"{qid}: status 非法 → {meta.get('status')}")
        if meta.get("source_type") not in VALID_SRC:
            errors.append(f"{qid}: source_type 非法 → {meta.get('source_type')}")

        # 号段
        base = ID_BASE.get(mod)
        if base is None:
            errors.append(f"{qid}: 未知模块 {mod}")
        else:
            m = re.match(r"Q-(\d+)$", qid)
            if not m:
                errors.append(f"{qid}: ID 格式应为 Q-数字")
            else:
                num = int(m.group(1))
                if not (base < num < base + SPAN):
                    errors.append(
                        f"{qid}: 编号越界，{mod} 应为 {base+1}~{base+SPAN-1}")

        # 目录与模块一致
        if f.parent.name != mod:
            errors.append(f"{qid}: 文件在 {f.parent.name}/，但 module={mod}")

        # 正文小节
        need = list(SECTIONS)
        # 项目深挖不要求「来源」：出处已经写进「关联项目」的文档路径里
        if meta.get("qtype") == "project":
            need = [s for s in need if s != "来源"]
        # 只有「给出代码片段让你判断输出」的题才需要 ## 题目 节
        if meta.get("qtype") == "coding" and meta.get("lab_src"):
            need += CODING_SECTIONS
        for s in need:
            if not re.search(rf"^##+\s*{s}", body, re.M):
                errors.append(f"{qid}: 缺小节「{s}」")

        # 已答不能是空壳（只看「口述答案」本节，不跨到下一节）
        if meta.get("status") in ("answered", "verified"):
            m = re.search(r"^##\s*口述答案\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S)
            seg = m.group(1) if m else ""
            if "待补充" in seg or not seg.strip():
                errors.append(f"{qid}: status={meta.get('status')} 但口述答案仍是空的")

        # 标题问句化（祈使式提问算合规；问号不必在末尾，括号补充说明也算）
        title = meta.get("title", "")
        if not (("？" in title or "?" in title)
                or re.match(r"^(用一句话|介绍|讲讲|说说|描述|解释|谈谈|聊)", title)):
            warns.append(f"{qid}: 标题不是问句 → {title[:30]}")

    for qid, fs in by_id.items():
        if len(fs) > 1:
            errors.append(f"ID 重复 {qid}: " + ", ".join(str(x) for x in fs))

    print(f"校验 {n} 张题卡")
    if warns:
        print(f"\n提醒 {len(warns)} 条（不阻塞）：")
        for w in warns[:10]:
            print("  ·", w)
        if len(warns) > 10:
            print(f"  ... 还有 {len(warns)-10} 条")
    if errors:
        print(f"\n❌ 错误 {len(errors)} 条：")
        for e in errors[:25]:
            print("  ✗", e)
        if len(errors) > 25:
            print(f"  ... 还有 {len(errors)-25} 条")
        return 1
    print("\n✅ 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
