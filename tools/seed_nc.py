#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""牛客面经 → 正式题卡骨架。

收录清单手工核定（见 docs/nowcoder_feasibility.md §九），
正文由 tools/cards/nc_*.cards 提供，apply_cards.py 灌入。
号段约定：nowcoder 来源 = 各模块 base+201 起（04_algo 用 1921+）（自建 1~300、视频 400+、牛客 200+）。
幂等：已存在的题卡跳过，重跑不会覆盖已填内容。
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = "2026-11-10"

U = {
    "hw_linux": "https://www.nowcoder.com/discuss/947059125291118592",
    "dpx1":     "https://www.nowcoder.com/discuss/945100596145553408",
    "dpx2":     "https://www.nowcoder.com/discuss/945100814861815808",
    "hw_t1":    "https://www.nowcoder.com/discuss/945497946403971072",
    "hw_t2":    "https://www.nowcoder.com/discuss/948632550891593728",
    "xp":       "https://www.nowcoder.com/discuss/945709685955395584",
}

# (id, title, module, sub, pri, diff, qtype, 来源key, 公司, 岗位, 轮次)
ROWS = [
    # ---- A. 03_linux：华为 Linux 一/二面 + 地平线内核 ----
    ("Q-1201", "select、poll、epoll 有什么区别？epoll 为什么高效？", "03_linux", "网络编程", "P0", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1202", "malloc 申请的内存 free 之后还能继续访问吗？会发生什么？", "03_linux", "系统与进程", "P0", 2, "principle", "hw_linux", "华为", "Linux 软件开发", "一面"),
    ("Q-1203", "给一个结构体怎么算大小？怎么调整成员顺序更省内存？", "03_linux", "系统与进程", "P0", 2, "principle", "hw_linux", "华为", "Linux 软件开发", "一面"),
    ("Q-1204", "多线程为什么需要锁？不加锁在 CPU 层面会出什么问题？", "03_linux", "并发", "P0", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1205", "服务器上出现大量 TIME_WAIT 是什么原因？怎么处理？", "03_linux", "网络编程", "P0", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1206", "TIME_WAIT 为什么要存在？为什么等 2MSL？", "03_linux", "网络编程", "P0", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1207", "一个进程的内存一直涨，怎么定位是哪里泄漏？说完整流程。", "03_linux", "系统与进程", "P0", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1208", "死锁的四个必要条件是什么？项目里怎么避免、怎么检测？", "03_linux", "并发", "P0", 2, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1209", "互斥锁在内核里是怎么实现的？加锁失败的线程去哪了？", "03_linux", "并发", "P1", 4, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1210", "读写锁和互斥锁有什么区别？什么场景读写锁反而更慢？", "03_linux", "并发", "P1", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1211", "TCP 滑动窗口和拥塞控制是怎么配合工作的？", "03_linux", "网络编程", "P1", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1212", "拥塞控制的几个阶段分别在干什么？为什么要有慢启动？", "03_linux", "网络编程", "P1", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1213", "volatile 能保证线程安全吗？为什么？", "03_linux", "并发", "P0", 2, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1214", "原子操作是怎么实现的？和加锁比开销差在哪？", "03_linux", "并发", "P0", 3, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1215", "内存屏障是干什么的？什么时候需要？", "03_linux", "并发", "P1", 4, "principle", "hw_linux", "华为", "Linux 软件开发", "二面"),
    ("Q-1216", "二级指针什么时候用？举个实际场景。", "03_linux", "系统与进程", "P1", 2, "principle", "hw_linux", "华为", "Linux 软件开发", "一面"),
    ("Q-1217", "手撕：判断字符串是不是回文，要求不申请额外空间。", "03_linux", "系统与进程", "P0", 1, "coding", "hw_linux", "华为", "Linux 软件开发", "一面"),
    ("Q-1218", "单核 CPU 上高优先级任务就绪后会发生什么？禁抢占时怎么办？", "03_linux", "内核与驱动", "P1", 3, "principle", "dpx1", "地平线", "嵌入式软件", "一面"),
    ("Q-1219", "原子操作解决什么问题？适合保护一组复杂操作吗？", "03_linux", "内核与驱动", "P1", 2, "principle", "dpx1", "地平线", "嵌入式软件", "一面"),
    ("Q-1220", "Tasklet 里要访问共享数据怎么保证临界区安全？为什么不能用 mutex？", "03_linux", "内核与驱动", "P1", 3, "principle", "dpx1", "地平线", "嵌入式软件", "一面"),
    ("Q-1221", "中断处理为什么分上半部和下半部？中断里为什么不能用 mutex？", "03_linux", "内核与驱动", "P0", 3, "principle", "dpx1", "地平线", "嵌入式软件", "一面"),
    ("Q-1222", "fork 创建子进程时地址空间怎么处理？什么是写时复制？", "03_linux", "系统与进程", "P0", 2, "principle", "dpx1", "地平线", "嵌入式软件", "一面"),
    ("Q-1223", "互斥锁和自旋锁有什么区别？获取不到锁时各自会怎样？", "03_linux", "并发", "P0", 2, "principle", "dpx1", "地平线", "嵌入式软件", "一面"),
    # ---- B. 09_hardware：地平线 CAN / 驱动 ----
    ("Q-4301", "U-Boot 在 Linux 启动过程中负责哪些工作？典型启动流程是什么？", "09_hardware", "嵌入式软件", "P0", 2, "principle", "dpx1", "地平线", "嵌入式软件", "一面"),
    ("Q-4302", "SocketCAN 在用户空间怎么收发 CAN 报文？过滤器怎么设？", "09_hardware", "总线协议", "P1", 3, "principle", "dpx1", "地平线", "嵌入式软件", "一面"),
    ("Q-4303", "CAN 驱动用 DMA 要注意什么？Cache 一致性怎么处理？", "09_hardware", "嵌入式软件", "P1", 4, "principle", "dpx2", "地平线", "嵌入式软件", "二面"),
    ("Q-4304", "CAN 驱动突然 Kernel Panic，你怎么定位？", "09_hardware", "嵌入式软件", "P1", 3, "principle", "dpx2", "地平线", "嵌入式软件", "二面"),
    ("Q-4305", "给 CAN DMA 申请大块连续内存有哪些方式？CMA 是什么？", "09_hardware", "嵌入式软件", "P1", 3, "principle", "dpx2", "地平线", "嵌入式软件", "二面"),
    ("Q-4306", "CAN 总线的错误处理有哪些？Bus-Off 是什么？怎么恢复？", "09_hardware", "总线协议", "P1", 3, "principle", "dpx2", "地平线", "嵌入式软件", "二面"),
    ("Q-4307", "驱动里的 probe 函数负责什么？设备和驱动怎么匹配？", "09_hardware", "嵌入式软件", "P0", 2, "principle", "dpx2", "地平线", "嵌入式软件", "二面"),
    # ---- C. 10_cv_pytorch：华为 AI 笔试 + 小鹏 ----
    ("Q-4701", "下列激活函数中，值域为开区间 (0,1) 的是哪一个？", "10_cv_pytorch", "基础", "P1", 1, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4702", "向量 v = Mu 中，矩阵 M 在这里起什么作用？", "10_cv_pytorch", "基础", "P1", 2, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4703", "Agent 范式 ReAct 的名字是哪两个英文单词拼起来的？", "10_cv_pytorch", "大模型与推理", "P1", 1, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4704", "训练困惑度一直降、真实用户提问上先降后升，怎么分析和处理？", "10_cv_pytorch", "训练", "P1", 3, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4705", "a* = 1.49（绝对误差限 0.004），a*+b* 的绝对误差限是多少？", "10_cv_pytorch", "基础", "P1", 1, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4706", "量化怎么和推理实现配合？INT4 权重直接参与计算吗？", "10_cv_pytorch", "大模型与推理", "P0", 3, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4707", "Agent 处理复杂任务要分解任务，下列说法哪项是对的？", "10_cv_pytorch", "大模型与推理", "P1", 2, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4708", "给大模型 Agent 接入工具时，哪种做法对减少调用错误是无效的？", "10_cv_pytorch", "大模型与推理", "P1", 2, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4709", "Sigmoid 的导数最大能取到多少？在哪取到？", "10_cv_pytorch", "基础", "P1", 1, "principle", "hw_t2", "华为", "AI 软件", "笔试"),
    ("Q-4710", "batch=1、序列 128、kv_heads=8、head_dim=64、FP16，一层 KV Cache 占多少显存？", "10_cv_pytorch", "大模型与推理", "P0", 2, "principle", "hw_t2", "华为", "AI 软件", "笔试"),
    ("Q-4711", "残差块写成 y = F(x) + x，缓解退化的核心逻辑是什么？", "10_cv_pytorch", "基础", "P0", 2, "principle", "hw_t2", "华为", "AI 软件", "笔试"),
    ("Q-4712", "5 万词的词表，One-Hot 表示一个词的维度由什么决定？", "10_cv_pytorch", "基础", "P1", 1, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4713", "推理时把 Q、K、V 三次投影合并成一次大矩阵乘，主要收益是什么？", "10_cv_pytorch", "大模型与推理", "P0", 2, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4714", "训练接近收敛时参数在最优点附近震荡，怎么让更新更平缓？", "10_cv_pytorch", "训练", "P1", 2, "principle", "hw_t2", "华为", "AI 软件", "笔试"),
    ("Q-4715", "卷积层的输出通道数通常由什么决定？", "10_cv_pytorch", "基础", "P1", 1, "principle", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-4716", "H100 和 B200 有什么区别？LLM 推理瓶颈在哪？", "10_cv_pytorch", "大模型与推理", "P0", 3, "principle", "xp", "小鹏", "深度学习平台研发", "校招面试"),
    ("Q-4717", "多卡训练是怎么同步梯度的？DDP 的底层机制是什么？", "10_cv_pytorch", "训练", "P0", 3, "principle", "xp", "小鹏", "深度学习平台研发", "校招面试"),
    ("Q-4718", "DDP 和 DP 有什么区别？为什么说 DDP 不省显存？", "10_cv_pytorch", "训练", "P1", 3, "principle", "xp", "小鹏", "深度学习平台研发", "校招面试"),
    # ---- D. 05_deploy：小鹏云原生 ----
    ("Q-2301", "深度学习平台要强隔离环境，怎么让 K8s 管虚拟机？", "05_deploy", "部署工程化", "P1", 3, "principle", "xp", "小鹏", "深度学习平台研发", "校招面试"),
    ("Q-2302", "kubectl 提交 YAML 之后，Pod 是怎么被创建和调度的？", "05_deploy", "部署工程化", "P1", 3, "principle", "xp", "小鹏", "深度学习平台研发", "校招面试"),
    ("Q-2303", "深度学习平台怎么管理异构算力（不同代次的 GPU）？", "05_deploy", "部署工程化", "P1", 3, "principle", "xp", "小鹏", "深度学习平台研发", "校招面试"),
    ("Q-2304", "平台对外提供推理服务，接口应该怎么设计？", "05_deploy", "部署工程化", "P0", 3, "principle", "xp", "小鹏", "深度学习平台研发", "校招面试"),
    # ---- E. 04_algo：华为机考 ----
    ("Q-1921", "KV 缓存批处理调度：按接纳规则模拟，输出总时间步数。", "04_algo", "模拟", "P0", 4, "coding", "hw_t2", "华为", "AI 软件", "笔试"),
    ("Q-1922", "两个位数可能极长的非负整数相加，怎么实现？", "04_algo", "数组哈希", "P0", 1, "coding", "hw_t1", "华为", "AI 软件", "笔试"),
    ("Q-1923", "纸张一行有字数上限，把所有短语印完最少要多少行？", "04_algo", "模拟", "P1", 2, "coding", "hw_t2", "华为", "AI 软件", "笔试"),
]


def appearance(comp: str, role: str, rnd: str, key: str) -> list[dict]:
    return [{"日期": "2026-11-10 抓取", "公司": comp, "岗位": role,
             "轮次": rnd, "来源": f"[牛客面经]({U[key]})", "可信度": "社区经验"}]


def make_skeleton(row) -> str:
    qid, title, mod, sub, pri, diff, qtype, src, comp, role, rnd = row
    url = U[src]
    return f"""---
id: {qid}
title: "{title}"
module: {mod}
sub: {sub}
priority: {pri}
difficulty: {diff}
roles: []
companies: []
qtype: {qtype}
status: indexed
source_type: nowcoder
source_ref: 牛客面经（{comp}·{role}·{rnd}）
verified_at: {TODAY}
tags: [牛客面经, {comp}]
appearances: ["{comp}·{role}"]
video_src: ""
video_bv: ""
video_page: ""
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
| 2026-11-10 抓取 | {comp} | {role} | {rnd} | [牛客面经]({url}) | 社区经验 |

## 关联项目

- 无（通用八股，不绑定具体项目）

## 来源

牛客面经 {comp}·{role}·{rnd}：{url}
"""


def main() -> int:
    content = ROOT / "content"
    made = skipped = 0
    for row in ROWS:
        qid = row[0]
        hits = list(content.rglob(f"{qid}-*.md")) + list(content.rglob(f"{qid}.md"))
        if hits:
            skipped += 1
            continue
        # 题卡文件名：号 + 从标题取的短标识
        slug = re.sub(r"[^0-9a-zA-Z]+", "-", row[1][:28]).strip("-").lower()[:40]
        target = content / row[2] / f"{qid}-{slug}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(make_skeleton(row), encoding="utf-8")
        made += 1
    print(f"骨架 {made} 张，跳过已存在 {skipped} 张")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
