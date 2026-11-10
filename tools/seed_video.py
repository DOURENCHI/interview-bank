#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把三个 B 站面试合集的分P标题落成题卡骨架。

来源（2026-11-10 抓取）：
  BV1pdW86SEAo  GPIO点亮人生    嵌入式八股 82P
  BV17n6PY7EYB  嵌入式自学DeepMeet 嵌入式八股 119P
  BV1Tz9MBTEFi  Linux集结地     C++ 大厂高频 33P

编号统一用各模块号段的 400+ 偏移（自建题都在 1–320），一眼能区分「视频来的」和「自己攒的」。
标题保留视频原话（去掉序号/公司前缀），答案由 tools/cards/*_v*.cards 填。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

PARTS = Path("C:/temp_bili/parts.json")
TODAY = "2026-11-10"
TITLE = {
    "BV1pdW86SEAo": "【备战2027春招】嵌入式面试八股文（GPIO点亮人生，82P）",
    "BV17n6PY7EYB": "嵌入式八股文面试题合集100题（嵌入式自学DeepMeet，119P）",
    "BV1Tz9MBTEFi": "2026最新C++大厂高频面试题八股文（Linux集结地，33P）",
}

# (题号, 模块, 子方向, 优先级, 难度, 题目, 来源bv, 来源P)
ROWS = [
    # ---------------- 02_cpp 号段 0901+
    ("Q-0901", "02_cpp", "语言基础", "P0", 1, "# 和 ## 在宏里分别起什么作用？", "BV1pdW86SEAo", 5),
    ("Q-0902", "02_cpp", "语言基础", "P0", 2, "volatile 关键字到底解决了什么问题？", "BV17n6PY7EYB", 112),
    ("Q-0903", "02_cpp", "语言基础", "P1", 2, "前置自增和后置自增有什么区别？哪个更快？", "BV1pdW86SEAo", 14),
    ("Q-0904", "02_cpp", "语言基础", "P1", 3, "函数调用的参数是按什么顺序压栈的？", "BV1pdW86SEAo", 17),
    ("Q-0905", "02_cpp", "语言基础", "P0", 2, "数组指针和指针数组怎么区分？", "BV1pdW86SEAo", 21),
    ("Q-0906", "02_cpp", "语言基础", "P0", 2, "函数指针和指针函数有什么区别？", "BV17n6PY7EYB", 1),
    ("Q-0907", "02_cpp", "语言基础", "P0", 1, "sizeof 和 strlen 有什么区别？", "BV17n6PY7EYB", 4),
    ("Q-0908", "02_cpp", "语言基础", "P0", 2, "struct 和 union 有什么区别？共用体的大小怎么算？", "BV17n6PY7EYB", 7),
    ("Q-0909", "02_cpp", "语言基础", "P0", 1, "全局变量和局部变量有什么区别？", "BV17n6PY7EYB", 12),
    ("Q-0910", "02_cpp", "语言基础", "P1", 2, "写一个返回两个参数中较小值的宏，要注意什么？", "BV17n6PY7EYB", 10),
    ("Q-0911", "02_cpp", "工程化与 SDK", "P1", 1, "#include <> 和 \"\" 有什么区别？", "BV17n6PY7EYB", 11),
    ("Q-0912", "02_cpp", "对象模型", "P0", 1, "C++ 的类有几种访问权限？分别是什么含义？", "BV17n6PY7EYB", 22),
    ("Q-0913", "02_cpp", "工程化与 SDK", "P1", 2, "内联函数是什么？为什么要有内联函数？", "BV17n6PY7EYB", 23),
    ("Q-0914", "02_cpp", "工程化与 SDK", "P0", 2, "一个程序分为哪几个段？各放什么？", "BV17n6PY7EYB", 25),
    ("Q-0915", "02_cpp", "语言基础", "P2", 1, "队列和栈有什么区别？", "BV17n6PY7EYB", 26),
    ("Q-0916", "02_cpp", "语言基础", "P0", 2, "手写一个 strcpy，要考虑哪些边界？", "BV17n6PY7EYB", 24),
    ("Q-0917", "02_cpp", "语言基础", "P1", 2, "手写一个 strcmp，返回值怎么定义？", "BV17n6PY7EYB", 47),
    ("Q-0918", "02_cpp", "语言基础", "P1", 2, "手写一个 strcat，怎么避免越界？", "BV17n6PY7EYB", 49),
    ("Q-0919", "02_cpp", "语言基础", "P1", 1, "数组和链表有什么区别？各自适合什么场景？", "BV17n6PY7EYB", 9),
    ("Q-0920", "02_cpp", "对象模型", "P0", 1, "面向对象的三大特征是什么？", "BV17n6PY7EYB", 65),
    ("Q-0921", "02_cpp", "对象模型", "P0", 2, "struct 和 class 在 C++ 里有什么区别？", "BV17n6PY7EYB", 114),
    ("Q-0922", "02_cpp", "工程化与 SDK", "P1", 2, "怎么避免头文件被重复包含？", "BV17n6PY7EYB", 115),
    ("Q-0923", "02_cpp", "语言基础", "P1", 2, "数组大小明明已经确定了，为什么还会越界？", "BV17n6PY7EYB", 116),
    ("Q-0924", "02_cpp", "语言基础", "P0", 2, "memcpy 和 memmove 有什么区别？", "BV17n6PY7EYB", 117),
    ("Q-0925", "02_cpp", "语言基础", "P0", 2, "C++ 的四种 cast 和 C 风格强制转换有什么区别？", "BV1Tz9MBTEFi", 10),
    ("Q-0926", "02_cpp", "工程化与 SDK", "P1", 2, "不想让编译器做字节对齐，该怎么办？", "BV17n6PY7EYB", 118),
    ("Q-0927", "02_cpp", "语言基础", "P0", 2, "const 和 static 各自的作用是什么？", "BV1Tz9MBTEFi", 11),
    ("Q-0928", "02_cpp", "语言基础", "P0", 3, "printf 为什么能打印个数不定的参数？", "BV1Tz9MBTEFi", 2),
    ("Q-0929", "02_cpp", "对象模型", "P2", 3, "如何拿到一个类里私有成员变量的值？", "BV1Tz9MBTEFi", 6),
    ("Q-0930", "02_cpp", "对象模型", "P1", 3, "怎么验证虚函数表在内存里的布局？", "BV1Tz9MBTEFi", 5),
    ("Q-0931", "02_cpp", "语言基础", "P1", 2, "C++14 有哪些常用特性？", "BV1Tz9MBTEFi", 7),
    ("Q-0932", "02_cpp", "语言基础", "P0", 2, "C++17 有哪些常用特性？", "BV1Tz9MBTEFi", 8),
    ("Q-0933", "02_cpp", "语言基础", "P1", 3, "C++20 的协程是怎么工作的？", "BV1Tz9MBTEFi", 9),
    ("Q-0934", "02_cpp", "语言基础", "P0", 2, "auto、auto&、auto&& 有什么区别？", "BV1Tz9MBTEFi", 21),
    ("Q-0935", "02_cpp", "STL 容器", "P0", 2, "map 和 unordered_map 有什么区别？怎么选？", "BV1Tz9MBTEFi", 22),
    ("Q-0936", "02_cpp", "语言基础", "P1", 2, "std::thread 和 packaged_task 是什么关系？", "BV1Tz9MBTEFi", 23),
    ("Q-0937", "02_cpp", "语言基础", "P1", 2, "thread_local 的作用是什么？", "BV1Tz9MBTEFi", 24),
    ("Q-0938", "02_cpp", "语言基础", "P0", 3, "std::move 和 std::forward 有什么区别？完美转发怎么实现？", "BV1Tz9MBTEFi", 25),
    ("Q-0939", "02_cpp", "语言基础", "P1", 2, "二级指针有什么用？它和一级指针、引用怎么选？", "BV1Tz9MBTEFi", 26),
    ("Q-0940", "02_cpp", "对象模型", "P1", 3, "在成员函数里 delete this 有什么问题？", "BV1Tz9MBTEFi", 15),
    ("Q-0941", "02_cpp", "对象模型", "P0", 3, "构造函数或析构函数抛异常会发生什么？", "BV1Tz9MBTEFi", 31),
    ("Q-0942", "02_cpp", "语言基础", "P0", 2, "make_shared 和 shared_ptr(new T) 有什么区别？", "BV1Tz9MBTEFi", 18),
    ("Q-0943", "02_cpp", "语言基础", "P0", 3, "weak_ptr 怎么知道 shared_ptr 已经把对象释放了？", "BV1Tz9MBTEFi", 29),
    ("Q-0944", "02_cpp", "STL 容器", "P1", 3, "STL 的内存池是怎么实现的？结构长什么样？", "BV1Tz9MBTEFi", 28),
    ("Q-0945", "02_cpp", "工程化与 SDK", "P0", 2, "静态链接和动态链接有什么区别？", "BV17n6PY7EYB", 89),
    ("Q-0946", "02_cpp", "对象模型", "P1", 3, "单例模式初始化失败怎么办？为什么会出现多份实例？", "BV1Tz9MBTEFi", 33),
    ("Q-0947", "02_cpp", "语言基础", "P2", 2, "if 判断写 0 == a 和 a == 0 有什么讲究？", "BV17n6PY7EYB", 44),

    # ---------------- 03_linux 号段 1501+
    ("Q-1501", "03_linux", "系统与进程", "P0", 2, "进程和线程有什么区别？", "BV17n6PY7EYB", 33),
    ("Q-1502", "03_linux", "系统与进程", "P0", 2, "进程间通信有哪几种方式？哪些需要内核参与？", "BV17n6PY7EYB", 34),
    ("Q-1503", "03_linux", "系统与进程", "P0", 2, "僵尸进程、孤儿进程、守护进程分别是什么？", "BV17n6PY7EYB", 37),
    ("Q-1504", "03_linux", "系统与进程", "P1", 2, "什么是系统调用？它和普通函数调用差在哪？", "BV17n6PY7EYB", 48),
    ("Q-1505", "03_linux", "系统与进程", "P1", 2, "for 循环里调用 fork，一共会创建多少个子进程？", "BV17n6PY7EYB", 70),
    ("Q-1506", "03_linux", "系统与进程", "P1", 3, "fork 之后文件描述符是怎么继承和共享的？", "BV1Tz9MBTEFi", 32),
    ("Q-1507", "03_linux", "并发", "P0", 3, "线程上下文切换的底层都做了什么？", "BV1Tz9MBTEFi", 3),
    ("Q-1508", "03_linux", "并发", "P1", 2, "自旋锁和互斥锁有什么区别？各自适合什么场景？", "BV17n6PY7EYB", 81),
    ("Q-1509", "03_linux", "并发", "P1", 2, "什么是原子操作？它是怎么保证不被中断的？", "BV17n6PY7EYB", 104),
    ("Q-1510", "03_linux", "并发", "P1", 2, "线程池是怎么设计出来的？关键参数有哪些？", "BV17n6PY7EYB", 101),
    ("Q-1511", "03_linux", "系统与进程", "P1", 2, "什么是内存碎片？内部碎片和外部碎片怎么区分？", "BV17n6PY7EYB", 100),
    ("Q-1512", "03_linux", "系统与进程", "P1", 3, "OOM killer 为什么杀进程？它是怎么打分的？", "BV1Tz9MBTEFi", 13),
    ("Q-1513", "03_linux", "系统与进程", "P1", 2, "内存泄漏怎么排查？valgrind 能看出什么？", "BV1Tz9MBTEFi", 27),
    ("Q-1514", "03_linux", "系统与进程", "P1", 2, "常用的调试方法有哪些？各自适合什么场景？", "BV17n6PY7EYB", 96),
    ("Q-1515", "03_linux", "内核与驱动", "P1", 3, "Linux 内核的启动流程分哪几个阶段？", "BV1pdW86SEAo", 77),
    ("Q-1516", "03_linux", "内核与驱动", "P1", 2, "Linux 驱动的三大基础设备类型是什么？", "BV17n6PY7EYB", 58),
    ("Q-1517", "03_linux", "并发", "P0", 2, "什么时候该用多进程，什么时候该用多线程？", "BV17n6PY7EYB", 56),
    ("Q-1518", "03_linux", "网络编程", "P0", 2, "OSI 七层模型和 TCP/IP 四层模型怎么对应？", "BV17n6PY7EYB", 76),
    ("Q-1519", "03_linux", "网络编程", "P0", 2, "TCP 三次握手和四次挥手为什么是 3 和 4？", "BV17n6PY7EYB", 79),
    ("Q-1520", "03_linux", "网络编程", "P0", 2, "TCP 和 UDP 有什么区别？各自的连接流程是什么？", "BV17n6PY7EYB", 51),
    ("Q-1521", "03_linux", "网络编程", "P0", 2, "TCP 粘包是怎么产生的？怎么解决？", "BV1Tz9MBTEFi", 19),
    ("Q-1522", "03_linux", "网络编程", "P0", 2, "TCP 靠什么保证可靠传输？", "BV17n6PY7EYB", 102),
    ("Q-1523", "03_linux", "网络编程", "P1", 2, "DHCP 协议是干什么的？流程是什么？", "BV17n6PY7EYB", 92),
    ("Q-1524", "03_linux", "网络编程", "P1", 1, "IP、子网掩码、网关、DNS 各起什么作用？", "BV17n6PY7EYB", 93),
    ("Q-1525", "03_linux", "网络编程", "P2", 1, "常见的网络拓扑有哪几种？", "BV17n6PY7EYB", 97),

    # ---------------- 04_algo 号段 2001+
    ("Q-2001", "04_algo", "排序算法", "P0", 2, "直接插入排序和希尔排序的思路与复杂度？", "BV1pdW86SEAo", 27),
    ("Q-2002", "04_algo", "排序算法", "P0", 2, "快速排序和冒泡排序的区别？快排最坏情况是什么？", "BV1pdW86SEAo", 28),
    ("Q-2003", "04_algo", "排序算法", "P0", 3, "堆排序和简单选择排序怎么实现？", "BV1pdW86SEAo", 29),
    ("Q-2004", "04_algo", "排序算法", "P1", 2, "归并排序怎么实现？为什么它适合链表？", "BV1pdW86SEAo", 30),
    ("Q-2005", "04_algo", "排序算法", "P1", 2, "基数排序的原理是什么？为什么它不比较元素？", "BV1pdW86SEAo", 31),
    ("Q-2006", "04_algo", "链表", "P0", 2, "怎么判断链表是否有环？入口怎么找？", "BV17n6PY7EYB", 57),
    ("Q-2007", "04_algo", "设计题", "P1", 3, "手写一个跳表：它为什么能替代平衡树？", "BV1Tz9MBTEFi", 14),
    ("Q-2008", "04_algo", "设计题", "P1", 3, "手撕缓存聚合：多种淘汰策略的缓存怎么写？", "BV1Tz9MBTEFi", 12),
    ("Q-2009", "04_algo", "设计题", "P1", 3, "LRU 的工程级实现要注意什么？", "BV1Tz9MBTEFi", 17),

    # ---------------- 09_hardware 号段 4501+
    ("Q-4501", "09_hardware", "ARM 体系", "P1", 2, "哈佛结构和冯诺依曼结构有什么区别？", "BV1pdW86SEAo", 58),
    ("Q-4502", "09_hardware", "ARM 体系", "P1", 2, "ARM 有哪几种工作模式？为什么要分模式？", "BV1pdW86SEAo", 59),
    ("Q-4503", "09_hardware", "ARM 体系", "P0", 2, "ARM 的寄存器有哪些？各自的作用是什么？", "BV17n6PY7EYB", 91),
    ("Q-4504", "09_hardware", "ARM 体系", "P1", 2, "FIQ 和 IRQ 有什么区别？", "BV1pdW86SEAo", 66),
    ("Q-4505", "09_hardware", "ARM 体系", "P0", 2, "什么是大端和小端？怎么用代码判断？", "BV17n6PY7EYB", 46),
    ("Q-4506", "09_hardware", "ARM 体系", "P2", 2, "怎么访问一个绝对地址？", "BV1pdW86SEAo", 70),
    ("Q-4507", "09_hardware", "ARM 体系", "P1", 2, "Cortex-M3 和 Cortex-M4 有什么区别？", "BV17n6PY7EYB", 105),
    ("Q-4508", "09_hardware", "STM32", "P0", 3, "单片机从上电复位到执行 main 之前做了什么？", "BV17n6PY7EYB", 110),
    ("Q-4509", "09_hardware", "STM32", "P1", 2, "中断能有返回值和参数吗？", "BV17n6PY7EYB", 86),
    ("Q-4510", "09_hardware", "STM32", "P1", 2, "C 语言的位域是什么？有什么坑？", "BV17n6PY7EYB", 106),
    ("Q-4511", "09_hardware", "STM32", "P0", 2, "PWM 是什么？频率、占空比、死区各指什么？", "BV17n6PY7EYB", 43),
    ("Q-4512", "09_hardware", "STM32", "P0", 2, "什么是看门狗？独立看门狗和窗口看门狗差在哪？", "BV17n6PY7EYB", 60),
    ("Q-4513", "09_hardware", "硬件基础", "P1", 2, "NAND Flash 和 NOR Flash 有什么区别？", "BV1pdW86SEAo", 54),
    ("Q-4514", "09_hardware", "硬件基础", "P1", 1, "CPU、MPU、MCU、SOC、SOPC 分别是什么？", "BV1pdW86SEAo", 55),
    ("Q-4515", "09_hardware", "硬件基础", "P1", 2, "什么是交叉编译？为什么嵌入式要交叉编译？", "BV17n6PY7EYB", 29),
    ("Q-4516", "09_hardware", "硬件基础", "P2", 2, "ROM 和 RAM 有什么区别？程序是怎么跑起来的？", "BV1pdW86SEAo", 57),
    ("Q-4517", "09_hardware", "硬件基础", "P1", 2, "Cache 是什么？为什么它能提速？", "BV17n6PY7EYB", 95),
    ("Q-4518", "09_hardware", "硬件基础", "P1", 2, "DMA 是什么？没有它行不行？", "BV17n6PY7EYB", 35),
    ("Q-4519", "09_hardware", "总线协议", "P0", 2, "UART、I2C、SPI 有什么区别？各适合什么场景？", "BV17n6PY7EYB", 30),
    ("Q-4520", "09_hardware", "总线协议", "P1", 2, "SPI 有哪几根线？哪些可以省掉？", "BV17n6PY7EYB", 31),
    ("Q-4521", "09_hardware", "总线协议", "P1", 3, "SPI 的四种工作模式是什么？CPOL 和 CPHA 怎么配？", "BV17n6PY7EYB", 71),
    ("Q-4522", "09_hardware", "总线协议", "P1", 2, "SPI 和 I2C 的寻址方式有什么区别？", "BV17n6PY7EYB", 28),
    ("Q-4523", "09_hardware", "总线协议", "P1", 2, "软件模拟 I2C 和硬件 I2C 有什么区别？", "BV17n6PY7EYB", 55),
    ("Q-4524", "09_hardware", "FreeRTOS", "P1", 2, "vTaskDelay 和 vTaskDelayUntil 有什么区别？", "BV1pdW86SEAo", 73),
    ("Q-4525", "09_hardware", "FreeRTOS", "P1", 2, "FreeRTOS 的空闲任务和钩子函数是干什么的？", "BV17n6PY7EYB", 80),
    ("Q-4526", "09_hardware", "FreeRTOS", "P0", 2, "FreeRTOS 的任务有哪几个状态？怎么迁移？", "BV17n6PY7EYB", 41),
    ("Q-4527", "09_hardware", "FreeRTOS", "P1", 2, "FreeRTOS 创建任务有几种方式？动态和静态差在哪？", "BV17n6PY7EYB", 78),
    ("Q-4528", "09_hardware", "FreeRTOS", "P0", 2, "FreeRTOS 里信号量和队列有什么区别？", "BV17n6PY7EYB", 61),
    ("Q-4529", "09_hardware", "FreeRTOS", "P1", 2, "什么是状态机编程？为什么嵌入式常用它？", "BV17n6PY7EYB", 82),
    ("Q-4530", "09_hardware", "硬件基础", "P2", 1, "JSON 格式的数据长什么样？嵌入式里怎么解析？", "BV17n6PY7EYB", 99),
    ("Q-4531", "09_hardware", "硬件基础", "P2", 2, "什么是回调函数？它在嵌入式里怎么用？", "BV17n6PY7EYB", 63),
    ("Q-4532", "09_hardware", "ARM 体系", "P1", 2, "中断和异常有什么区别？两者和睡眠模式什么关系？", "BV1pdW86SEAo", 63),
]


def main() -> int:
    parts = json.loads(PARTS.read_text(encoding="utf-8"))
    idx = {(p["bv"], p["page"]): p for p in parts}
    created = 0
    for qid, mod, sub, pri, diff, q, bv, page in ROWS:
        p = idx[(bv, page)]
        mm, ss = divmod(p["start"], 60)
        ref = f"B站 {bv} P{page}（{mm:02d}:{ss:02d} 起，{p['dur']//60}:{p['dur']%60:02d}）"
        d = ROOT / "content" / mod
        d.mkdir(parents=True, exist_ok=True)
        fm = f"""---
id: {qid}
title: "{q}"
module: {mod}
sub: {sub}
priority: {pri}
difficulty: {diff}
roles: []
companies: []
qtype: principle
status: indexed
source_type: video
source_ref: {ref}
verified_at: {TODAY}
tags: [视频真题]
video_src: {TITLE[bv]}
video_bv: {bv}
video_page: P{page}
vid_seed: true
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

## 关联项目

- 无（通用八股，不绑定具体项目）

## 来源

{TITLE[bv]} · {ref}
"""
        (d / f"{qid}.md").write_text(fm, encoding="utf-8")
        created += 1
    print(f"生成 {created} 张视频题卡")
    from collections import Counter
    print(dict(Counter(r[1] for r in ROWS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
