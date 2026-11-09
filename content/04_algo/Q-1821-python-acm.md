---
id: Q-1821
title: 权重存取与可复现性 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: [华为车BU, 亿嘉和]
qtype: coding
status: draft
source_type: self_doc
source_ref: 教学文档/Python实验台/Python考点实验台.html
verified_at: 2026-11-09
tags: [Python, ACM, 输入输出, 机考]
auto: true
lab_src: snip
---

## 题目

机考要在 ACM 模式下自己读输入、自己输出，没有函数签名提示。
下面这段 Python 程序对应的读入与输出写法是什么？

```python
import os
import tempfile

import torch
import torch.nn as nn

torch.manual_seed(11)
m = nn.Linear(2, 1)
sd = {k: v.clone() for k, v in m.state_dict().items()}
m2 = nn.Linear(2, 1)
m2.load_state_dict(sd)
print("state_dict 键", tuple(m.state_dict().keys()))
print("权重一致", bool(torch.equal(m.weight, m2.weight)),
      "偏置一致", bool(torch.equal(m.bias, m2.bias)))

torch.manual_seed(12)
m3 = nn.Linear(3, 2)
path = os.path.join(tempfile.gettempdir(), "_py_lab_state.pt")
torch.save(m3.state_dict(), path)
m4 = nn.Linear(3, 2)
m4.load_state_dict(torch.load(path, weights_only=True))
os.remove(path)
print("存盘往返一致", bool(torch.equal(m3.weight, m4.weight)))

torch.manual_seed(13)
a = torch.randn(3).tolist()
torch.manual_seed(13)
b = torch.randn(3).tolist()
print("固定 seed 可复现", a == b, [round(v, 6) for v in a])
```

输出样例：

```
state_dict 键 ('weight', 'bias')
权重一致 True 偏置一致 True
存盘往返一致 True
固定 seed 可复现 True [-0.111659, -1.14561, 1.410316]
```

## 口述答案

待补充。重点说清三件事：怎么读到不定长输入、怎么处理行尾、怎么保证输出格式一字不差。

## 讲深一层

待补充。

## 高频追问

待补充。

## 易错点

待补充。

## 关联项目

无。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 09 优化、正则化与工程化
