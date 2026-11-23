#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""牛客面经 → 题库骨架（自动入库的机械部分）。

把 _cache/nc_posts/ 里已渲染、且命中公司注册表的帖子落成题卡骨架：
  · 公司归属：companies/targets.json 的 nc_keywords 匹配（title + 正文）
  · 模块归属：按题目内容关键词映射（CAN/驱动→09，进程/线程→03，训练/模型→10 …）
  · 编号：各模块现有最大 id + 1（自建/视频/牛客三层号段互不冲突）
  · 去重：题面归一化后与库内现有标题 Dice ≥0.75 视为重复，跳过
  · 状态：indexed（待补充）——答案由自动化代理择优用 .cards 补写

只做机械部分；"质量合适"的判断和答案撰写交给自动化代理。
幂等：以 sources/nowcoder_seeded.json 记账，同一帖不会二次入库。
"""
from __future__ import annotations
import json, re, sys, unicodedata
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from nc_collect import POSTS, match_company  # noqa: E402

SEEDED = ROOT / "sources" / "nowcoder_seeded.json"
TODAY = datetime.now().strftime("%Y-%m-%d")

# 模块归属规则：自上而下第一个命中的为准
MODULE_RULES = [
    ("06_ros2",   r"ros2?|ROS|SLAM|slam|导航算法|话题|TF2?|激光雷达"),
    ("09_hardware", r"\bCAN\b|CANopen|驱动|U-Boot|[Uu]-?[Bb]oot|Bootloader|单片机|STM32|FreeRTOS|"
                    r"\bRTOS\b|嵌入式|PWM|I2C|IIC|SPI|UART|串口|Flash|寄存器|PCB|运放|GPIO|"
                    r"中断|DMA|Cache一致性|晶振|示波器"),
    ("05_deploy", r"k8s|K8s|KubeVirt|容器|docker|Docker|推理服务|ONNX|[Oo]nnx|TensorRT|"
                  r"端侧|[Jj]etson|CUDA|cuda|算子|量化部署"),
    ("10_cv_pytorch", r"训练|模型|transformer|Transformer|attention|Attention|量化|KV [Cc]ache|"
                      r"大模型|深度学习|卷积|梯度|过拟合|激活函数|损失|YOLO|检测|分割|"
                      r"pytorch|PyTorch|LLM|[Tt]oken|词表|batch|epoch|预训练|微调|"
                      r"推理优化|batch=|kv_heads"),
    ("04_algo", r"手撕|实现一个|时间复杂度|空间复杂度|动态规划|二叉树|链表|排序|回文|"
                r"top[Kk]| LeetCode |算法题|求出|输出.{0,12}(多少|结果)"),
    ("03_linux", r"进程|线程|锁|epoll|TCP|UDP|Linux|linux|内核|信号|socket|Socket|"
                 r"调度|死锁|内存泄漏|TIME_WAIT| fork |管道|虚拟内存|页表|GCC|gdb|GDB"),
    ("02_cpp", r"C\+\+|c\+\+|虚函数|STL|指针|引用|构造|析构|智能指针|多态|编译|链接|"
               r"template|模板|lambda"),
]
SUB_RULES = {
    "03_linux": [(r"锁|线程|进程|死锁|信号|fork", "并发"),
                 (r"TCP|UDP|epoll|socket|TIME_WAIT|网络", "网络编程"),
                 (r"内核|页表|内存泄漏|中断", "内核与驱动")],
    "09_hardware": [(r"\bCAN\b|CANopen|SocketCAN", "总线协议"),
                    (r".*", "嵌入式软件")],
    "10_cv_pytorch": [(r"训练|梯度|过拟合|预训练|微调|epoch|DDP|多卡", "训练"),
                      (r"KV [Cc]ache|大模型|LLM|Transformer|attention|Attention|量化|"
                       r"推理|Token|词表", "大模型与推理"),
                      (r".*", "基础")],
    "05_deploy": [(r".*", "部署工程化")],
    "04_algo": [(r".*", "模拟")],
    "06_ros2": [(r".*", "ROS2")],
    "02_cpp": [(r".*", "语言基础")],
}
DEFAULT_MODULE = "02_cpp"


def module_of(text: str) -> tuple[str, str]:
    for mod, pat in MODULE_RULES:
        if re.search(pat, text):
            sub = DEFAULT_SUB = mod
            for sp, sname in SUB_RULES.get(mod, [(r".*", "语言基础")]):
                if re.search(sp, text):
                    sub = sname
                    break
            return mod, sub
    return DEFAULT_MODULE, SUB_RULES[DEFAULT_MODULE][0][1]


def dice(a: str, b: str) -> float:
    def bg(s):
        s = re.sub(r"[\s，。、？！：:（）()\[\]【】“”\"'…·—+,.?《》/\\]", "", s.lower())
        return {s[i:i + 2] for i in range(len(s) - 1)} or {s}
    A, B = bg(a), bg(b)
    return 2 * len(A & B) / (len(A) + len(B)) if A and B else 0.0


def load_manifest() -> dict:
    if SEEDED.exists():
        return json.loads(SEEDED.read_text(encoding="utf-8"))
    return {}


def save_manifest(m: dict):
    SEEDED.parent.mkdir(parents=True, exist_ok=True)
    SEEDED.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# 行为面 / 非技术题黑名单（实测来自 od 测试岗与叙述帖）
JUNK_RE = re.compile(
    r"自我介绍|加班|想问的吗|个人规划|职业规划|项目介绍|了解.{0,6}od|"
    r"测试流程|抓包|学习到|怎么看|怎么推进|遇到了什么|印象最深的|最难的 bug|"
    r"^(讲|聊|分享)一个|项目内容|个人情况|技术学习")
# 残句特征（实测来自笔试解析帖的断行）
FRAGMENT_RE = re.compile(r"^[的了吗呢吧（），、：；。]|^而不是|^就是|^先看|；$|）$")


def is_quality(q: str) -> bool:
    t = q.strip()
    if not (10 <= len(t) <= 90):
        return False
    if JUNK_RE.search(t) or FRAGMENT_RE.search(t):
        return False
    if t.count(" ") > 10:                       # 表格/代码碎行
        return False
    return True


def is_dup(q: str, bank_titles: list[str]) -> bool:
    """dice ≥0.68，或与较短一方包含率 ≥0.80（长短题名 dice 会偏低）。"""
    for t in bank_titles:
        if dice(q, t) >= 0.68:
            return True
        A = _bigrams(q)
        B = _bigrams(t)
        inter = len(A & B)
        if inter and inter / min(len(A), len(B)) >= 0.80:
            return True
    return False


def _bigrams(s: str) -> set:
    s = re.sub(r"[\s，。、？！：:（）()\[\]【】“”\"'…·—+,.?《》/\\]", "", s.lower())
    return {s[i:i + 2] for i in range(len(s) - 1)} or {s}


def clean_title(q: str) -> str:
    t = re.sub(r"^(考点|延伸考点|复盘|追问)[:：]\s*", "", q.strip())
    t = re.sub(r"^(让我|问我|问我怎么|问我为什么|问我怎么|问怎么|面试官问|面试官让我)", "", t)
    t = t.strip(" -—:：,，。")
    if len(t) > 58:
        t = t[:57].rstrip("，, ") + "…"
    if not t.endswith(("？", "?")):
        t += "？"
    return t


ID_BASE = {"01_project": 100, "02_cpp": 600, "03_linux": 1100, "04_algo": 1600,
           "05_deploy": 2100, "06_ros2": 2600, "07_imaging": 3100,
           "08_robot": 3600, "09_hardware": 4100, "10_cv_pytorch": 4600,
           "11_python": 5100, "12_backend": 5600, "13_hardware2": 6100}
SPAN = 500


def alloc_id(mod: str, nxt: dict):
    """返回模块 mod 的下一个空闲编号：跳过磁盘上已存在的卡文件，且不越出号段。

    修复 2026-11-13 覆盖事故：旧逻辑在号段顶部回退到"最小空位"后，
    循环里 nxt += 1 盲增，会一路穿过被占用的编号，把旧卡覆盖掉。
    新逻辑每次分配都检查目标文件是否存在，号段满返回 None（调用方决定溢出或跳过）。
    （号段与 tools/validate.py 的 ID_BASE 保持一致）"""
    lo, hi = ID_BASE.get(mod, 0) + 1, ID_BASE.get(mod, 0) + SPAN - 1
    n = max(nxt.get(mod, lo), lo)
    while n <= hi:
        # 前缀匹配：Q-0767.md 与 Q-0767-sdk.md 这类变体名都算占用
        if not list((ROOT / "content" / mod).glob(f"Q-{n:04d}*.md")):
            nxt[mod] = n + 1
            return n
        n += 1
    return None


# 号段溢出：09_hardware（4101~4599）2026-11-23 已满 499/499，
# 硬件题自动落到 13_hardware2（6101~6599），模块名/子类保持硬件语义
OVERFLOW_MODULE = {"09_hardware": "13_hardware2"}


def skeleton(qid, title, mod, sub, comp, role, url, rnd) -> str:
    rnd_cell = rnd or ""
    return f"""---
id: {qid}
title: "{title}"
module: {mod}
sub: {sub}
priority: P1
difficulty: 2
roles: []
companies: []
qtype: principle
status: indexed
source_type: nowcoder
source_ref: 牛客面经（{comp}·{role}）
verified_at: {TODAY}
tags: [牛客面经, {comp}]
appearances: ["{comp}·{role}"]
nc_url: {url}
---

## 题目

待补充。

## 口述答案

待补充。

## 讲深一层

待补充。

## 高频追问

1. 待补充

## 易错点

- 待补充

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| {TODAY} 抓取 | {comp} | {role} | {rnd_cell} | [牛客面经]({url}) | 社区经验 |

## 关联项目

- 无（通用八股，不绑定具体项目）

## 来源

牛客面经 {comp}·{role}：{url}
"""


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=60, help="单次最多生成骨架数")
    ap.add_argument("--min-questions", type=int, default=2,
                    help="帖子至少提取到几道题才入库")
    args = ap.parse_args()

    manifest = load_manifest()
    # 现有库内标题，用于跨源去重
    sys.path.insert(0, str(ROOT / "tools"))
    from build import load_questions
    bank_titles = [q["title"] for q in load_questions()]
    bank_norm = {re.sub(r"[\s，。、？！：:（）()\[\]【】“”\"'…·—+,.?]", "", t.lower())
                 for t in bank_titles}

    # 编号分配器状态（alloc_id 逐张检查磁盘占用，避免覆盖既有卡）
    nxt: dict = {}
    all_posts = sorted(POSTS.glob("*.json")) if POSTS.exists() else []

    made, skipped_dup, skipped_junk, skipped_nocomp, unmatched = 0, 0, 0, 0, []
    for p in all_posts:
        if made >= args.max:
            break
        d = json.loads(p.read_text(encoding="utf-8"))
        pid = d["id"]
        if pid in manifest:
            continue
        if "笔试" in d["title"]:      # 笔试解析帖行级噪声大，机考题由人工批次处理
            manifest[pid] = {"company": "", "url": d["url"], "cards": [],
                             "seeded_at": TODAY, "note": "笔试解析帖，跳过"}
            continue
        comp = match_company(d["title"] + " " + " ".join(d.get("body", [])[:80]))
        if not comp:
            skipped_nocomp += 1
            unmatched.append(d["title"][:40])
            continue
        qs = [q for q in (d.get("questions") or []) if q.get("q")]
        if len(qs) < args.min_questions:
            continue
        # 岗位只从标题推断——题面混入被拒的行为面词会污染（实测"测试工作"→"测试"岗）
        role = next((w for w in ["C++", "嵌入式", "推理", "部署", "机器人", "算法",
                                 "软件开发", "软件工程师", "驱动", "SLAM", "后端",
                                 "平台研发", "测试开发"]
                     if w.lower() in d["title"].lower()), "软件研发")
        url = d["url"]
        cards = []
        for q in qs:
            norm = re.sub(r"[\s，。、？！：:（）()\[\]【】“”\"'…·—+,.?《》]", "", q["q"].lower())
            if is_dup(q["q"], bank_titles):
                skipped_dup += 1
                continue
            if not is_quality(q["q"]):
                skipped_junk += 1
                continue
            mod, sub = module_of(q["q"] + " " + d["title"])
            n = alloc_id(mod, nxt)
            if n is None and mod in OVERFLOW_MODULE:
                mod = OVERFLOW_MODULE[mod]
                n = alloc_id(mod, nxt)
            if n is None:
                print(f"  ⚠ {comp} 号段满跳过：{q['q'][:44]}")
                continue
            qid = f"Q-{n:04d}"
            title = clean_title(q["q"])
            target = ROOT / "content" / mod / f"{qid}.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(skeleton(qid, title, mod, sub, comp, role, url,
                                       d.get("round") or ""), encoding="utf-8")
            bank_norm.add(norm)
            cards.append(qid)
            made += 1
            if made >= args.max:
                break
        if cards:
            manifest[pid] = {"company": comp, "url": url, "cards": cards,
                             "seeded_at": TODAY}
        else:
            manifest[pid] = {"company": comp, "url": url, "cards": [],
                             "seeded_at": TODAY, "note": "全部与库内重复"}
    save_manifest(manifest)

    print(f"骨架 {made} 张 | 重复跳过 {skipped_dup} | 低质跳过 {skipped_junk} | 未命中公司 {skipped_nocomp} 帖")
    if unmatched:
        print("未命中公司（可考虑新增类别后重跑）：")
        for t in unmatched[:10]:
            print("   -", t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
