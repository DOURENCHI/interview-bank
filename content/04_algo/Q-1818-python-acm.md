---
id: Q-1818
title: RNN / LSTM / GRU 的形状对照 的 ACM 输入输出怎么写？
module: 04_algo
sub: Python ACM输入输出
priority: P0
difficulty: 1
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: indexed
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
import torch
import torch.nn as nn

seq = torch.randn(2, 7, 4)

rnn = nn.RNN(4, 5, batch_first=True)
out, h = rnn(seq)
print("RNN  输出", tuple(out.shape), "hidden", tuple(h.shape))

lstm = nn.LSTM(4, 5, batch_first=True)
print("LSTM 输出", tuple(lstm(seq)[0].shape))

gru = nn.GRU(4, 5, batch_first=True)
print("GRU  输出", tuple(gru(seq)[0].shape))

cell = nn.RNNCell(4, 5)
hh = torch.zeros(2, 5)
for t in range(3):
    hh = cell(torch.randn(2, 4), hh)
    print(f"第 {t + 1} 个时间步 hidden", tuple(hh.shape))
```

输出样例：

```
RNN  输出 (2, 7, 5) hidden (1, 2, 5)
LSTM 输出 (2, 7, 5)
GRU  输出 (2, 7, 5)
第 1 个时间步 hidden (2, 5)
第 2 个时间步 hidden (2, 5)
第 3 个时间步 hidden (2, 5)
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

`教学文档/Python实验台/Python考点实验台.html` · 08 CNN 与 RNN
