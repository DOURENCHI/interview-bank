---
id: Q-1864
title: 接雨水：双指针法的正确性怎么证？
module: algo
sub: 双指针滑窗
priority: P0
difficulty: 3
roles: [AI算法, 端侧部署]
companies: []
qtype: coding
status: answered
source_type: inferred
source_ref: 按华为机考题型分布推导，题名对照 LeetCode
verified_at: 2026-11-09
tags: [双指针, 单调栈]
hint: 每格水量取决于左右最大值的较小者。移动较小一侧时那一侧的 max 已确定，可安全结算。
auto: true
algo_seed: true
---

## 题目

**输入**：`height = [0,1,0,2,1,0,1,3,2,1,2,1]`
**输出**：`6`

**问**：双指针法的正确性怎么证？

## 口述答案

> 每一格的雨水量 = `min(左边最大值, 右边最大值) - 当前高度`。
> 双指针的做法是：维护 `leftMax` 和 `rightMax`，每次移动**较矮**那一侧。
> 因为矮的那一侧，它的 `min(左max, 右max)` 已经确定了——另一边只会更高或相等，
> 所以可以立刻结算这一格的水量，不用等另一边算完。

## 讲深一层

```cpp
int trap(vector<int>& h) {
    int l = 0, r = h.size() - 1, lm = 0, rm = 0, res = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            lm = max(lm, h[l]);
            res += lm - h[l];        // lm 一定 <= rm，所以 min 就是 lm
            ++l;
        } else {
            rm = max(rm, h[r]);
            res += rm - h[r];
            --r;
        }
    }
    return res;
}
```

| 方法 | 时间 | 空间 |
|---|---|---|
| 暴力（每格找左右最大） | O(n²) | O(1) |
| 预处理左右最大值数组 | O(n) | O(n) |
| **双指针** | **O(n)** | **O(1)** |
| 单调栈 | O(n) | O(n) |

## 高频追问

1. **为什么 `lm - h[l]` 一定非负？** —— `lm` 是包含 `h[l]` 在内的历史最大，所以 ≥ 它。
2. **为什么要移矮的一侧？** —— 只有矮侧的水量能确定。
3. **和「盛最多水的容器」什么区别？** —— 那题求最大面积，这题求总容量。

## 易错点

- ❌ 先更新 res 再更新 max（顺序反了会算出负数）
- ❌ 移动高的一侧
- ✅ 说清「矮侧水量可确定」


## 关联项目

无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。

## 来源

算法题通用解法整理（预测题，非真实面经）
