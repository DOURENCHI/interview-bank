---
id: Q-1805
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 112 题）
module: algo
sub: 语法与类型
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-21
tags: [Python, 读程序写结果, 机考, 语言细节]
auto: true
lab_src: quiz
---

## 题目

```python
import torch, tempfile, os
torch.manual_seed(12)
m = torch.nn.Linear(3, 2)
path = os.path.join(tempfile.gettempdir(), "_lab_state.pt")
torch.save(m.state_dict(), path)
m2 = torch.nn.Linear(3, 2)
m2.load_state_dict(torch.load(path, weights_only=True))
os.remove(path)
print(bool(torch.equal(m.weight, m2.weight)), tuple(m.weight.shape))
```

- **A.** True (2, 3)
- **B.** (False, (2, 3))
- **C.** (True, (3, 2))
- **D.** (True, (6,))

## 口述答案

答案是 **A. True (2, 3)**，实际输出 `True (2, 3)`。

存的是 state_dict（不是整个模型），所以新模型结构必须一致才能 load；weight 形状 (out=2, in=3)。

## 讲深一层

`torch.save` 用 pickle 序列化，`weights_only=True` 只允许张量与基本容器，阻断反序列化执行任意代码（2.6 起成默认）。所以加载不可信文件也安全。结构必须一致：`Linear(3,2)` 的 weight 是 `(2,3)`，换成 `Linear(2,3)` 就 size mismatch。

## 高频追问

1. **形状不一致会怎样？** —— 报 `size mismatch for weight: copying a param with shape torch.Size([2,3])`
2. **为什么用 state_dict？** —— 与代码解耦，类重构后仍能加载
3. **`weights_only` 的意义？** —— 防 pickle 反序列化执行任意代码，是加载外部权重的安全开关

## 易错点

- 直接 `torch.load` 整个模型再改类——反序列化失败，找不到旧类
- GPU 存、CPU 读不加 `map_location`——报 CUDA 不可用
- 以为 save 存了网络结构——只存张量，结构要自己重建

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
