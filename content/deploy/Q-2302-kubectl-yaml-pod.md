---
id: Q-2302
title: "kubectl 提交 YAML 之后，Pod 是怎么被创建和调度的？"
module: deploy
sub: 部署工程化
priority: P1
difficulty: 3
roles: []
companies: []
qtype: principle
status: answered
source_type: nowcoder
source_ref: 牛客面经（小鹏·深度学习平台研发·校招面试）
verified_at: 2026-11-10
tags: [牛客面经, 小鹏]
appearances: ["小鹏·深度学习平台研发"]
video_src: ""
video_bv: ""
video_page: ""
nc_url: https://www.nowcoder.com/discuss/945709685955395584
---

## 题目

**背景**：平台岗基础题：kubectl 提交一个 YAML 之后，到容器真正跑起来，中间发生了什么？
**问**：请描述 Pod 的创建与调度链路，以及 Pause 容器的作用。

## 口述答案

> 链路五步：① `kubectl` 把 YAML 发给 API Server，经过认证、鉴权、准入控制后，把 Pod 对象写入 **etcd**——此时它只是个期望状态；② **Scheduler** 监听到未绑定的 Pod，按两阶段选节点：先过滤（资源够不够、亲和性、污点容忍），再打分（负载均衡、亲和权重），选出节点并绑定；③ 对应节点的 **kubelet** 监听到"这个 Pod 归我管"，调用容器运行时接口 **CRI**（containerd）拉镜像、创建容器；④ 网络由 **CNI** 插件分配 Pod IP；⑤ 容器起来后 kubelet 持续做探针和状态上报。Pause 容器是 Pod 里第一个被创建的特殊容器，它**持有网络命名空间**（还有 IPC 等），业务容器全部加入它的命名空间——这就是同一个 Pod 里容器能 localhost 互访的原因；Pause 还承担回收孤儿进程的 init 职责，它挂了整个 Pod 重建。

## 讲深一层

```
kubectl → API Server(认证/鉴权/准入) → etcd
        → Scheduler(过滤+打分) → 绑定节点
        → kubelet → CRI(containerd) → CNI → 容器运行
```
- 控制循环思想：声明式期望状态 + 各组件 watch-and-reconcile

## 高频追问

1. Scheduler 打分看什么？——资源均衡、镜像本地性、亲和权重
2. 探针失败会怎样？——liveness 重启容器，readiness 摘出 Service 端点

## 易错点

- 说 kubelet 直接调 Docker——中间是 CRI 抽象，运行时可换
- 不知道 Pause 容器，答不出 Pod 内 localhost 互通的原理

## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2026-11-10 抓取 | 小鹏 | 深度学习平台研发 | 校招面试 | https://www.nowcoder.com/discuss/945709685955395584 | 社区经验 |

## 关联项目

- `05_deploy` Q-2301/Q-2303

## 来源

牛客面经 小鹏·深度学习平台研发·校招面试：https://www.nowcoder.com/discuss/945709685955395584
