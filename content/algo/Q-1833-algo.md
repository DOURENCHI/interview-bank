---
id: Q-1833
title: 螺旋矩阵：边界怎么收缩才不会漏或重？
module: algo
sub: 数组哈希
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [矩阵, 模拟]
hint: 维护上下左右四个边界，每走完一条边收缩一格，循环条件是 top<=bottom 且 left<=right。
auto: true
algo_seed: true
---

## 题目

**输入**：`matrix = [[1,2,3],[4,5,6],[7,8,9]]`
**输出**：`[1,2,3,6,9,8,7,4,5]`

**问**：边界怎么收缩才不会漏或重？

## 口述答案

> 维护四个边界：上 `top`、下 `bottom`、左 `left`、右 `right`。
> 按「从左到右、从上到下、从右到左、从下到上」走四条边，每走完一条就把对应边界内缩一格。
> 循环条件是 `top <= bottom && left <= right`。
> 关键细节：**走完上和右之后要重新判断边界**，否则单行/单列矩阵会被重复访问。

## 讲深一层

```cpp
vector<int> spiralOrder(vector<vector<int>>& m) {
    vector<int> res;
    int top = 0, bottom = m.size()-1, left = 0, right = m[0].size()-1;
    while (top <= bottom && left <= right) {
        for (int j = left; j <= right; ++j) res.push_back(m[top][j]);
        ++top;
        for (int i = top; i <= bottom; ++i) res.push_back(m[i][right]);
        --right;
        if (top <= bottom) {                       // 关键判断
            for (int j = right; j >= left; --j) res.push_back(m[bottom][j]);
            --bottom;
        }
        if (left <= right) {                       // 关键判断
            for (int i = bottom; i >= top; --i) res.push_back(m[i][left]);
            ++left;
        }
    }
    return res;
}
```

## 高频追问

1. **不加那两个 if 会怎样？** —— 单行矩阵会重复输出，单列矩阵会错乱。
2. **生成螺旋矩阵（反向）呢？** —— 用同样的边界法往里填数。
3. **能不能用方向数组 + 转向？** —— 能，但边界法更不容易错。

## 易错点

- ❌ 忘了走完两条边后重新判断边界
- ❌ 边界内缩时机错（应该在走完那条边后立刻缩）
- ✅ 手画 3×3 和 1×4 各推一遍


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
