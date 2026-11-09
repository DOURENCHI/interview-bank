#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给没有本地文档可抽取的模块补索引级题卡。

这些题不是从你的文档里抽出来的，是按岗位 JD 推导的高频考点（source_type: inferred）。
只有题目和标签，答案留空，等补。目的只是让目录完整、覆盖可检索。

用法: python tools/seed.py
重复执行不会重复生成（按 title 去重）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ID_BASE = {"04_algo": 1600, "07_imaging": 3100, "08_robot": 3600, "10_cv_pytorch": 4600}

# (模块, 优先级, 子方向, 题目, 难度, 标签)
SEED = [
    # ---------------- 04 算法与机考（P0，华为机考是硬门槛）
    ("04_algo", "P0", "ACM模式", "华为机考为什么必须用 ACM 模式写输入输出？", 1, ["机考", "ACM", "输入输出"]),
    ("04_algo", "P0", "ACM模式", "读一行不定长整数、读到文件末尾，C++ 怎么写才不出错？", 2, ["机考", "getline", "cin"]),
    ("04_algo", "P0", "ACM模式", "输入输出格式错会掉多少分，怎么自查？", 1, ["机考", "边界", "调试"]),
    ("04_algo", "P0", "字符串", "字符串处理常考哪几类？", 1, ["机考", "字符串", "回文"]),
    ("04_algo", "P0", "哈希", "哈希表在这类题里一般解决什么问题？", 1, ["机考", "哈希", "去重"]),
    ("04_algo", "P0", "双指针", "双指针和滑动窗口的区别是什么？", 2, ["机考", "双指针", "滑动窗口"]),
    ("04_algo", "P0", "滑动窗口", "滑动窗口什么条件下能用？", 2, ["机考", "滑动窗口", "单调性"]),
    ("04_algo", "P0", "搜索", "DFS 和 BFS 怎么选？", 2, ["机考", "DFS", "BFS"]),
    ("04_algo", "P0", "搜索", "二叉树遍历的递归写法和非递归写法差别在哪？", 2, ["机考", "二叉树", "遍历"]),
    ("04_algo", "P0", "DP", "动态规划的状态怎么定义？", 3, ["机考", "DP", "状态设计"]),
    ("04_algo", "P0", "DP", "0-1 背包和完全背包的区别是什么？", 2, ["机考", "DP", "背包"]),
    ("04_algo", "P0", "DP", "最长递增子序列的 O(n log n) 解法思路是什么？", 3, ["机考", "DP", "LIS", "二分"]),
    ("04_algo", "P0", "策略", "机考第二题只拿一半样例，怎么排优先级？", 2, ["机考", "策略", "得分"]),

    # ---------------- 07 医学影像（P1，佗道医疗/佗道手术机器人的落点）
    ("07_imaging", "P1", "DICOM", "DICOM 文件里到底存了什么？", 2, ["DICOM", "元数据", "医学影像"]),
    ("07_imaging", "P1", "DICOM", "窗宽窗位是什么，为什么 CT 必须调窗？", 2, ["DICOM", "窗宽窗位", "CT"]),
    ("07_imaging", "P1", "DICOM", "HU 值是什么，为什么它比原始灰度有用？", 2, ["DICOM", "HU", "CT"]),
    ("07_imaging", "P1", "UNet", "UNet 为什么适合医学图像分割？", 2, ["UNet", "分割", "网络结构"]),
    ("07_imaging", "P1", "UNet", "UNet 的跳跃连接解决了什么问题？", 3, ["UNet", "跳跃连接", "感受野"]),
    ("07_imaging", "P1", "UNet", "上采样用转置卷积还是双线性插值，怎么选？", 3, ["UNet", "转置卷积", "棋盘效应"]),
    ("07_imaging", "P1", "评价指标", "Dice 系数和 IoU 的区别是什么，为什么分割更常用 Dice？", 2, ["Dice", "IoU", "指标"]),
    ("07_imaging", "P1", "数据问题", "医学图像类别极不平衡怎么处理？", 3, ["类别不平衡", "损失函数", "Dice Loss"]),
    ("07_imaging", "P1", "数据问题", "医学数据集很小的时候，数据增强该怎么做才不引入伪影？", 3, ["数据增强", "小样本"]),
    ("07_imaging", "P1", "方案选择", "3D 分割和逐层 2D 分割怎么选？", 3, ["3D分割", "2D分割", "显存"]),
    ("07_imaging", "P1", "工具链", "ITK、VTK、MITK 各自负责什么？", 2, ["ITK", "VTK", "MITK"]),
    ("07_imaging", "P1", "工具链", "分割结果怎么和原始 DICOM 的空间信息对齐？", 3, ["DICOM", "空间坐标", "配准"]),

    # ---------------- 08 机器人学（P1，亿嘉和感知规控 / 佗道手术机器人）
    ("08_robot", "P1", "运动学", "DH 参数是什么，怎么用它建运动学模型？", 3, ["DH参数", "运动学", "机械臂"]),
    ("08_robot", "P1", "运动学", "正运动学和逆运动学的区别是什么？", 2, ["正运动学", "逆运动学"]),
    ("08_robot", "P1", "运动学", "逆运动学有多解时怎么选？", 3, ["逆解", "多解", "避障"]),
    ("08_robot", "P1", "运动学", "雅可比矩阵的物理意义是什么？", 3, ["Jacobian", "速度映射", "奇异点"]),
    ("08_robot", "P1", "运动学", "奇异点在什么情况下出现，工程上怎么规避？", 3, ["奇异点", "可操作度"]),
    ("08_robot", "P1", "力控", "六维力传感器的数据怎么用到控制回路里？", 3, ["力传感器", "力控", "阻抗控制"]),
    ("08_robot", "P1", "力控", "导纳控制和阻抗控制的区别是什么？", 3, ["导纳控制", "阻抗控制", "力控"]),
    ("08_robot", "P1", "控制", "PID 三个参数各自起什么作用，为什么要积分限幅？", 2, ["PID", "积分饱和", "控制"]),
    ("08_robot", "P1", "工具链", "MoveIt 的规划流程是怎样的？", 2, ["MoveIt", "运动规划", "ROS2"]),
    ("08_robot", "P1", "工程", "ROS2 里机械臂怎么做实时控制，为什么普通节点不够？", 3, ["ROS2", "实时", "控制器"]),
    ("08_robot", "P1", "标定", "手眼标定解决什么问题，标定误差会怎样传导？", 3, ["手眼标定", "标定", "误差"]),

    # ---------------- 10 深度学习（P1，靠 UNet 项目本身练）
    ("10_cv_pytorch", "P1", "基础", "Tensor 和 numpy array 的区别是什么？", 1, ["Tensor", "PyTorch", "numpy"]),
    ("10_cv_pytorch", "P1", "基础", "autograd 是怎么工作的？", 2, ["autograd", "计算图", "反向传播"]),
    ("10_cv_pytorch", "P1", "训练", "为什么每次反向传播前要 zero_grad？", 2, ["梯度累积", "zero_grad", "训练"]),
    ("10_cv_pytorch", "P1", "数据", "Dataset 和 DataLoader 各自负责什么？", 1, ["Dataset", "DataLoader"]),
    ("10_cv_pytorch", "P1", "数据", "num_workers 设大了会有什么问题？", 2, ["DataLoader", "多进程", "显存"]),
    ("10_cv_pytorch", "P1", "训练", "model.train() 和 model.eval() 到底改变了什么？", 2, ["train", "eval", "BN", "Dropout"]),
    ("10_cv_pytorch", "P1", "训练", "BatchNorm 在训练和推理时的行为有什么不同？", 3, ["BatchNorm", "滑动平均"]),
    ("10_cv_pytorch", "P1", "训练", "学习率调度器什么时候该用，Cosine 和 Step 怎么选？", 2, ["学习率", "调度器"]),
    ("10_cv_pytorch", "P1", "优化", "混合精度训练省的是什么，为什么不会掉精度？", 3, ["混合精度", "AMP", "FP16"]),
    ("10_cv_pytorch", "P1", "工程", "保存模型该存 state_dict 还是整个模型？", 2, ["state_dict", "模型保存"]),
    ("10_cv_pytorch", "P1", "工程", "显存不够有哪些降显存的手段，各自代价是什么？", 2, ["显存", "梯度检查点", "batch size"]),
]

TEMPLATE = """---
id: {qid}
title: {title}
module: {module}
sub: {sub}
priority: {pri}
difficulty: {diff}
roles: []
companies: [华为车BU, 亿嘉和]
qtype: principle
status: indexed
source_type: inferred
source_ref: 按岗位 JD 推导，非真实面经
verified_at: 2026-11-09
tags: [{tags}]
---

## 口述答案

> 待补充。200–320 字，口语，结构：结论 → 为什么 → 落到"我做过"。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

待补充。

## 来源

按华为（车BU / 计算产品线）与亿嘉和岗位 JD 推导的高频考点，**不是真实面经**。
"""


def main() -> int:
    created = 0
    for module, pri, sub, title, diff, tags in SEED:
        d = CONTENT / module
        d.mkdir(parents=True, exist_ok=True)
        # 按 title 去重
        exists = False
        for f in d.glob("Q-*.md"):
            if title in f.read_text(encoding="utf-8", errors="ignore"):
                exists = True
                break
        if exists:
            continue
        nums = [int(m.group(1)) for f in d.glob("Q-*.md")
                if (m := re.match(r"Q-(\d+)", f.name))]
        nxt = max(nums + [ID_BASE[module]]) + 1
        qid = f"Q-{nxt:04d}"
        (d / f"{qid}.md").write_text(
            TEMPLATE.format(qid=qid, title=title, module=module, sub=sub,
                            pri=pri, diff=diff, tags=", ".join(tags)),
            encoding="utf-8")
        created += 1
    print(f"新增索引题卡 {created} 道")
    return 0


if __name__ == "__main__":
    sys.exit(main())
