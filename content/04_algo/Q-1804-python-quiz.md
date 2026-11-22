---
id: Q-1804
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 111 题）
module: 04_algo
sub: 并发与性能
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
import torch
torch.manual_seed(11)
m = torch.nn.Linear(2, 1)
sd = {k: v.clone() for k, v in m.state_dict().items()}
m(torch.randn(2, 2)).sum().backward()
m2 = torch.nn.Linear(2, 1)
m2.load_state_dict(sd)
print(tuple(m.state_dict().keys()), bool(torch.equal(m.weight, m2.weight)), bool(torch.equal(m.bias, m2.bias)))
```

- **A.** ('weight', 'bias') True True
- **B.** ('weight', 'bias') False True
- **C.** ('param',) True True
- **D.** ('weight', 'bias') True False

## 口述答案

答案是 **A. ('weight', 'bias') True True**，实际输出 `('weight', 'bias') True True`。

state_dict 是有序字典，键为 weight/bias；load_state_dict 把保存的值装回新模型，两个布尔都为 True。

## 讲深一层

`state_dict()` 是 OrderedDict，只含参数与 buffer，不含结构与超参，键名按层级拼（如 `0.weight`）。`load_state_dict` 默认 strict，键集合必须完全一致。正因只存张量，才能跨代码重构加载。

## 高频追问

1. **为什么不存整个模型？** —— pickle 依赖类的定义路径，重构后 `torch.load` 直接失败
2. **`strict=False` 的作用？** —— 允许缺键/多键，返回 missing_keys 与 unexpected_keys 供检查
3. **optimizer 也要存吗？** —— 续训必须存 `opt.state_dict()`，否则动量与步数丢失

## 易错点

- 以为 state_dict 含结构——只有张量，重建模型要另写代码
- 键名写错——报 `Missing key(s)` 或 `Unexpected key(s)`
- 用 `torch.save(model)` 存整个对象再改类定义——加载时 AttributeError

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
