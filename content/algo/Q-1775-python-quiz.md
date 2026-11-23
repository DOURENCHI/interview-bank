---
id: Q-1775
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 82 题）
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
import torch
s = torch.sigmoid(torch.tensor([0.0, 2.0, 4.0]))
print([round(v, 6) for v in s.tolist()])
```

- **A.** [0.5, 0.880797, 0.982014]
- **B.** [0.5, 0.5, 0.5]
- **C.** [0.5, 0.119203, 0.017986]
- **D.** [0.0, 2.0, 4.0]

## 口述答案

答案是 **A. [0.5, 0.880797, 0.982014]**，实际输出 `[0.5, 0.880797, 0.982014]`。

sigmoid 把任意实数压进 (0,1)，0 → 0.5、2 → 0.8808、4 → 0.9820。它是单调的，不能区分 2 和 4 这种大小关系。

## 讲深一层

`σ(x)=1/(1+e^{−x})`，0→0.5、2→0.8808、4→0.9820，值域 (0,1) 且单调。饱和区梯度极小，`σ'(4)≈0.0177`，层一多连乘就趋零，这是梯度消失根源。多标签用 sigmoid，单标签多分类必须 softmax。

## 高频追问

1. **sigmoid 与 softmax 的区别？** —— softmax 各类互相竞争、和恒为 1；sigmoid 每个输出独立，和可以是任意值
2. **深层网络为什么改用 ReLU？** —— sigmoid 在饱和区梯度接近 0，连乘后梯度消失；ReLU 正区间梯度恒为 1
3. **`σ(−2)` 是多少？** —— 0.119203，正好等于 `1 − σ(2)`，这是 sigmoid 的对称性

## 易错点

- 把 `σ(4)` 算成 0.999——实际 0.982014，饱和不等于到 1
- 认为 sigmoid 输出之和为 1——只有两个互补输入时才恰好为 1
- 多分类用 sigmoid 再算交叉熵——各类概率不归一，loss 与梯度都不对

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
