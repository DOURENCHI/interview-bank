---
id: Q-1780
title: 这段 Python 代码输出什么？（07 分类：逻辑回归与交叉熵 · 第 87 题）
module: algo
sub: 容器与切片
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
logits = torch.tensor([2.0, 1.0, 0.1])
print(round(float(torch.nn.CrossEntropyLoss()(logits, torch.tensor([0]))), 6),
      round(float(torch.nn.CrossEntropyLoss()(logits, torch.tensor([0.9, 0.05, 0.05]))), 6))
```

- **A.** 0.41703 0.56203
- **B.** (0.41703, 0.41703)
- **C.** (0.56203, 0.41703)
- **D.** (0.0, 0.0)

## 口述答案

答案是 **A. 0.41703 0.56203**，实际输出 `0.41703 0.56203`。

CrossEntropyLoss 的输入是 logits 不是概率、目标是类别下标。传概率 [0.9,0.05,0.05] 会被当成 logits 再做一次 softmax，损失就变了。

## 讲深一层

`CrossEntropyLoss` = `log_softmax` + `NLLLoss`，输入必须是 logits，target 是 long 类标。传概率 `[0.9,0.05,0.05]` 会被再 softmax 一次，损失变 0.56203。0.41703 就是 `−log(0.665241)`。

## 高频追问

1. **为什么不能传概率？** —— 会二次 softmax，loss 与梯度都错，且不报错，属于静默 bug
2. **target 能用 one-hot 吗？** —— 这个接口不行，要传类标索引；one-hot 得手写 `−Σy·log_softmax`
3. **0.41703 怎么算出来？** —— softmax 后正确类概率 0.665241，取负对数即 0.41703

## 易错点

- 先 softmax 再喂 CE——最常见的错，损失偏大且训练变慢
- target 传 float——报 `expected scalar type Long`
- 认为 CE 输入是概率——这是本题的核心考点，答反就全错

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 07 分类：逻辑回归与交叉熵
