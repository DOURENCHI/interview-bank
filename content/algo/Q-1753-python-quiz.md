---
id: Q-1753
title: 这段 Python 代码输出什么？（03 autograd 与计算图 · 第 60 题）
module: algo
sub: 函数与异常
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
a = torch.tensor([1, 2])
b = torch.tensor([3, 4])
print(torch.cat([a, b]).tolist(), tuple(torch.stack([a, b]).shape))
```

- **A.** [1, 2, 3, 4] (2, 2)
- **B.** ([1, 2, 3, 4], (2,))
- **C.** ([1, 3, 2, 4], (2, 2))
- **D.** ([1, 2, 3, 4], (4,))

## 口述答案

答案是 **A. [1, 2, 3, 4] (2, 2)**，实际输出 `[1, 2, 3, 4] (2, 2)`。

cat 是拼接（形状变长），stack 是堆叠（新增一个维度），所以 stack 后是 (2,2)。

## 讲深一层

`cat` 沿已有维拼接，其余维必须完全相同；`stack` 新建一维，两个 `(2,)` 堆成 `(2,2)`。若 a、b 是 `(2,3)`：`cat` 得 `(4,3)`，`stack` 得 `(2,2,3)`。`stack` 等价于先 `unsqueeze` 再 `cat`，dtype 不同会报错。

## 高频追问

1. **`cat` 的 `dim` 怎么影响结果？** —— 对 `(2,2)` 张量 `dim=0` 得 `(4,2)`、`dim=1` 得 `(2,4)`；1-D 张量传 `dim=1` 越界报错
2. **`stack` 之后怎么拆回去？** —— `torch.unbind(y, dim=0)` 得到两个 `(2,)`，或直接 `y[0]`、`y[1]`
3. **变长序列能直接 `cat` 吗？** —— 不能，除拼接维外其余维必须一致，得先 pad 到等长或改用 `pad_sequence`

## 易错点

- 把 `stack` 当 `cat`——期望 `(4,)` 实得 `(2,2)`，后面接 Linear 时输入维度算错
- 认为 `stack` 不改变总元素数——元素数不变但秩加 1，`ndim` 判断会错
- 用 `cat` 拼不同 dtype——int64 与 float32 混拼直接报错，需先 `.float()`

## 关联项目

无（语言基础题）。

## 来源

`教学文档/Python实验台/Python考点实验台.html` · 03 autograd 与计算图
