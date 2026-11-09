---
id: Q-1806
title: 这段 Python 代码输出什么？（09 优化、正则化与工程化 · 第 112 题）
module: 04_algo
sub: Python语言细节
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: answered
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
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

待补充：把这条规则扩到相邻场景（换个运算符、换个类型、换个边界值会不会变）。
机考里这类题错一次就是整题分，靠的是把规则记准而不是临场推。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
