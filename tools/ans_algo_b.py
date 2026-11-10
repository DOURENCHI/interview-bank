#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算法题补答案（第 2 批：双指针 / 滑动窗口，15 道）。

用法: python tools/ans_algo_b.py [--dry]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "04_algo"

TAIL = ("\n\n## 关联项目\n\n无（算法题）。刷的时候用 LeetCode 按题名搜，别背题号。"
        "\n\n## 来源\n\n算法题通用解法整理（预测题，非真实面经）\n")

ITEMS = [
    {
        "kw": "盛最多水的容器", "diff": 2,
        "body": """## 题目

**输入**：`height = [1,8,6,2,5,4,8,3,7]`
**输出**：`49`（下标 1 和 8，高 7，宽 7）
**要求**：O(n)，不能枚举所有组合。

**问**：为什么移动矮的一侧不会漏掉最优解？

## 口述答案

> 面积 = `min(左高, 右高) × 宽度`。宽度只会因为移动而变小，
> 所以想让面积变大只能靠**高度变大**。
> 而高度由两侧中较矮的那个决定——移动高的一侧，短板没变、宽度还变小了，面积必然不变或更小。
> 所以只能移动矮的一侧，这样每次移动都可能找到更大的高度，不会漏解。

## 讲深一层

```cpp
int maxArea(vector<int>& h) {
    int l = 0, r = h.size() - 1, best = 0;
    while (l < r) {
        best = max(best, min(h[l], h[r]) * (r - l));
        if (h[l] < h[r]) ++l;     // 移矮的一侧
        else --r;
    }
    return best;
}
```

**正确性证明思路**：设当前 `h[l] < h[r]`，则「以 l 为左端点的所有组合」的面积上限就是当前这个
（因为宽度最大时就已经是当前值，再往右移宽度更小、高度不会超过 h[l]）。所以 l 可以安全排除。

## 高频追问

1. **相等时移哪边？** —— 都可以，因为两边都不会是更优解的短板了。
2. **能排序吗？** —— 不能，下标即宽度，排序就丢了位置信息。
3. **如果是二维（容器接雨水）？** —— 那是另一道题，要用左右最大值。

## 易错点

- ❌ 移动高的一侧 —— 逻辑错，会漏解
- ❌ 用 `<=` 判断导致重复移动
- ✅ 能说出正确性证明的核心那一句
""",
    },
    {
        "kw": "无重复字符的最长子串", "diff": 2,
        "body": """## 题目

**输入**：`s = "abcabcbb"`
**输出**：`3`（`"abc"`）

**问**：窗口左边界为什么要取 max？

## 口述答案

> 用哈希记录每个字符**最后出现的下标**。右指针一路往前扩，
> 遇到重复字符时，左边界应该跳到「这个字符上次出现的下标 + 1」。
> 但必须写 `left = max(left, last[c] + 1)`——因为上次出现的下标可能**比当前 left 还小**，
> 那是更早的过期记录，直接赋值会把窗口往回拉，导致重复计算。

## 讲深一层

```cpp
int lengthOfLongestSubstring(string s) {
    vector<int> last(128, -1);
    int left = 0, best = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
        if (last[s[r]] >= left)          // 上次出现在当前窗口内
            left = last[s[r]] + 1;
        last[s[r]] = r;
        best = max(best, r - left + 1);
    }
    return best;
}
```

`last[c] >= left` 这个判断等价于取 max，写法更直观。

## 高频追问

1. **为什么要 `>= left` 而不是无条件跳？** —— 无条件跳会被过期记录拉回左边。
2. **能处理 Unicode 吗？** —— 上面假设 ASCII；Unicode 要用 `unordered_map<char32_t,int>`。
3. **要求返回子串本身？** —— 记录 best 对应的 `left/right`。

## 易错点

- ❌ 直接 `left = last[c] + 1` —— 窗口回退
- ❌ 忘了更新 `last[c]`
- ✅ 记住「左边界只能往前走」
""",
    },
    {
        "kw": "最小覆盖子串", "diff": 3,
        "body": """## 题目

**输入**：`s = "ADOBECODEBANC", t = "ABC"`
**输出**：`"BANC"`

**问**：need 和 window 两个计数器怎么维护？

## 口述答案

> 三个东西：`need` 记 t 里每个字符要多少，`window` 记当前窗口里有多少，
> 再用一个 `valid` 记「已经满足数量的字符种类数」。
> 右指针扩张时更新 window，如果某字符数量刚好等于 need，valid 加一；
> 当 `valid == need.size()` 说明窗口覆盖了 t，此时尝试收缩左边界，边收缩边记录最短。

## 讲深一层

```cpp
string minWindow(string s, string t) {
    unordered_map<char,int> need, win;
    for (char c : t) ++need[c];
    int needKinds = need.size(), valid = 0;
    int l = 0, start = 0, len = INT_MAX;

    for (int r = 0; r < (int)s.size(); ++r) {
        char c = s[r];
        if (need.count(c)) {
            ++win[c];
            if (win[c] == need[c]) ++valid;
        }
        while (valid == needKinds) {            // 已覆盖，尝试收缩
            if (r - l + 1 < len) { len = r - l + 1; start = l; }
            char d = s[l++];
            if (need.count(d)) {
                if (win[d] == need[d]) --valid;  // 先判再减
                --win[d];
            }
        }
    }
    return len == INT_MAX ? "" : s.substr(start, len);
}
```

## 高频追问

1. **为什么用 `valid` 而不是每次比较两个 map？** —— 比较是 O(k)，valid 让判断变 O(1)。
2. **收缩时为什么先判 `win[d] == need[d]`？** —— 减之前相等，说明减完就不满足了。
3. **含重复字符的 t 行吗？** —— 行，need 记的是数量。

## 易错点

- ❌ 收缩时先减再判 —— valid 少算
- ❌ 返回空串的条件写错
- ✅ 说清「valid 记的是种类数，不是字符总数」
""",
    },
    {
        "kw": "找到字符串中所有字母异位词", "diff": 2,
        "body": """## 题目

**输入**：`s = "cbaebabacd", p = "abc"`
**输出**：`[0,6]`（`"cba"` 和 `"bac"`）

**问**：固定窗口怎么滑动？

## 口述答案

> 窗口长度固定为 p 的长度。先把窗口填满，比较一次计数数组；
> 之后每次右进一个字符、左出一个字符，再比较。
> 用长度 26 的数组而不是排序——比较两个 26 元数组是 O(26)，常数极小。
> 更进一步可以用一个 `diff` 变量记录「有多少个字符的计数不同」，把比较降到 O(1)。

## 讲深一层

```cpp
vector<int> findAnagrams(string s, string p) {
    vector<int> res;
    int n = s.size(), m = p.size();
    if (n < m) return res;
    vector<int> need(26,0), win(26,0);
    for (char c : p) ++need[c-'a'];
    for (int i = 0; i < m; ++i) ++win[s[i]-'a'];
    if (win == need) res.push_back(0);
    for (int i = m; i < n; ++i) {
        ++win[s[i]-'a'];
        --win[s[i-m]-'a'];
        if (win == need) res.push_back(i - m + 1);
    }
    return res;
}
```

## 高频追问

1. **为什么不用排序比较？** —— 每次排序 O(m log m)，滑动时白白浪费。
2. **`diff` 优化怎么做？** —— 维护计数不同的字符个数，为 0 即匹配。
3. **大小写混合？** —— 数组扩到 128 或 256。

## 易错点

- ❌ 窗口边界算错（起点是 `i-m+1`）
- ❌ 忘了判断 `n < m`
- ✅ 说清「固定窗口 + 计数数组」
""",
    },
    {
        "kw": "长度最小的子数组", "diff": 2,
        "body": """## 题目

**输入**：`target = 7, nums = [2,3,1,2,4,3]`
**输出**：`2`（`[4,3]`）
**要求**：元素全为正。

**问**：滑动窗口和前缀和+二分怎么选？

## 口述答案

> **全是正数**时用滑动窗口：窗口和单调递增，右扩左缩都不会回退，O(n)。
> **有负数**时滑窗失效——加了负数窗口和可能变小，左指针的移动依据就没了，
> 这时要用前缀和 + 二分（O(n log n)）或单调队列。
> 所以先问题目有没有「正数」这个前提。

## 讲深一层

```cpp
int minSubArrayLen(int target, vector<int>& a) {
    int l = 0, sum = 0, best = INT_MAX;
    for (int r = 0; r < (int)a.size(); ++r) {
        sum += a[r];
        while (sum >= target) {              // 满足条件就尝试缩
            best = min(best, r - l + 1);
            sum -= a[l++];
        }
    }
    return best == INT_MAX ? 0 : best;
}
```

## 高频追问

1. **有负数怎么办？** —— 前缀和 `pre[j]-pre[i] >= target`，对每个 j 二分最小的 i。
2. **为什么 while 不是 if？** —— 缩一次可能还满足，要继续缩。
3. **要返回子数组本身？** —— 记录 best 对应的区间。

## 易错点

- ❌ 有负数还用滑窗
- ❌ 用 if 只缩一次 —— 漏掉更短解
- ✅ 先确认「元素是否全正」
""",
    },
    {
        "kw": "滑动窗口最大值", "diff": 3,
        "body": """## 题目

**输入**：`nums = [1,3,-1,-3,5,3,6,7], k = 3`
**输出**：`[3,3,5,5,6,7]`

**问**：单调队列为什么能做到 O(n)？

## 口述答案

> 维护一个**下标**队列，队列里的值从队头到队尾单调递减。
> 新元素进来时，把队尾所有比它小的都弹掉（它们不可能再成为最大值），再入队；
> 同时把「已经滑出窗口」的队头弹掉。这样队头永远是当前窗口最大值。
> 每个元素最多进队一次、出队一次，所以总复杂度 O(n)。

## 讲深一层

```cpp
vector<int> maxSlidingWindow(vector<int>& a, int k) {
    deque<int> dq;                 // 存下标
    vector<int> res;
    for (int i = 0; i < (int)a.size(); ++i) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();   // 过期
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();   // 更小的没用了
        dq.push_back(i);
        if (i >= k - 1) res.push_back(a[dq.front()]);
    }
    return res;
}
```

| 方法 | 时间 | 说明 |
|---|---|---|
| 暴力 | O(nk) | 每个窗口扫一遍 |
| 大顶堆 | O(n log n) | 要处理过期 |
| **单调队列** | **O(n)** | 最优 |

## 高频追问

1. **为什么存下标不存值？** —— 要判断是否滑出窗口。
2. **`<=` 还是 `<`？** —— 用 `<=` 弹掉相等值，队列更短，结果不变。
3. **求窗口最小值？** —— 改成单调递增队列。

## 易错点

- ❌ 存值不存下标 —— 无法判断过期
- ❌ 先弹过期再弹小值，顺序反了会残留
- ✅ 说清「每元素进出各一次」
""",
    },
    {
        "kw": "移动零", "diff": 1,
        "body": """## 题目

**输入**：`nums = [0,1,0,3,12]`
**输出**：`[1,3,12,0,0]`
**要求**：原地，保持非零元素相对顺序。

**问**：快慢指针原地怎么做？

## 口述答案

> 慢指针 `slow` 指向「下一个非零元素该放的位置」，快指针扫全数组。
> 遇到非零就和 `slow` 位置交换，然后 `slow++`。
> 这样非零元素被依次挤到前面，零自然被换到后面，且相对顺序不变。

## 讲深一层

```cpp
void moveZeroes(vector<int>& a) {
    int slow = 0;
    for (int fast = 0; fast < (int)a.size(); ++fast)
        if (a[fast] != 0) swap(a[slow++], a[fast]);
}
```

不用额外数组，也不需要「先统计零的个数再补零」。

## 高频追问

1. **交换会不会打乱顺序？** —— 不会，`slow` 之前的都已是稳定排列。
2. **不交换、直接覆盖行吗？** —— 行，但要记非零个数，最后补零。
3. **要保持零的顺序吗？** —— 题目通常不要求；要的话这个写法也满足。

## 易错点

- ❌ 用额外数组 —— 不满足原地
- ❌ `slow++` 位置写错
- ✅ 说清「slow 是写指针」
""",
    },
    {
        "kw": "删除有序数组中的重复项", "diff": 1,
        "body": """## 题目

**输入**：`nums = [1,1,2]`
**输出**：返回 `2`，且 `nums` 前两个元素为 `[1,2]`

**问**：为什么返回长度而不是新数组？

## 口述答案

> 题目要求原地修改，返回的是**有效长度 k**，调用方按前 k 个元素读取。
> 这样不用分配新数组，O(1) 空间。
> 做法是快慢指针：`slow` 指向已处理的最后一个不重复位置，
> `fast` 扫，遇到和 `nums[slow]` 不同的就写到 `slow+1`。

## 讲深一层

```cpp
int removeDuplicates(vector<int>& a) {
    if (a.empty()) return 0;
    int slow = 0;
    for (int fast = 1; fast < (int)a.size(); ++fast)
        if (a[fast] != a[slow]) a[++slow] = a[fast];
    return slow + 1;
}
```

## 高频追问

1. **允许最多重复两次呢？** —— 判断改成 `a[fast] != a[slow-1]`（前提 slow ≥ 1）。
2. **无序数组呢？** —— 这题依赖有序，无序要用哈希。
3. **返回的 k 之后的数据要不要清？** —— 不用，题目不关心。

## 易错点

- ❌ 返回 `slow` 而不是 `slow+1`
- ❌ 空数组没处理
- ✅ 说清「原地 + 返回有效长度」的约定
""",
    },
    {
        "kw": "颜色分类", "diff": 3,
        "body": """## 题目

**输入**：`nums = [2,0,2,1,1,0]`
**输出**：`[0,0,1,1,2,2]`
**要求**：一趟扫描，常数空间。

**问**：三指针的边界怎么定才不出错？

## 口述答案

> 三个指针：`p0` 指向 0 区右边界（下一个 0 该放的位置），
> `p2` 指向 2 区左边界，`p` 是当前扫描位置。
> 遇到 0 就和 `p0` 交换、`p0++`、`p++`；
> 遇到 2 就和 `p2` 交换、`p2--`，但 **`p` 不能自增**——因为换过来的是还没检查过的元素。

## 讲深一层

```cpp
void sortColors(vector<int>& a) {
    int p0 = 0, p = 0, p2 = a.size() - 1;
    while (p <= p2) {
        if (a[p] == 0)      swap(a[p0++], a[p++]);
        else if (a[p] == 2) swap(a[p], a[p2--]);   // p 不动
        else                ++p;
    }
}
```

`p` 不动的原因：`a[p2]` 是未处理区，换过来可能是 0 或 2，必须重新判断。

## 高频追问

1. **为什么 `p <= p2` 不是 `<`？** —— `p == p2` 时那个元素还没判断。
2. **遇到 0 为什么 p 可以动？** —— `a[p0]` 一定已处理过（是 1 或 p 自己）。
3. **稳定性？** —— 不保证，但题目不要求。

## 易错点

- ❌ 遇到 2 时 `p++` —— 跳过未检元素
- ❌ 循环条件写成 `<`
- ✅ 记住「换 2 时 p 不动」
""",
    },
    {
        "kw": "接雨水", "diff": 3,
        "body": """## 题目

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
""",
    },
    {
        "kw": "环形链表", "diff": 1,
        "body": """## 题目

**输入**：链表头节点，判断是否有环。

**问**：快慢指针为什么一定相遇？

## 口述答案

> 快指针每次走两步、慢指针一步。如果无环，快指针先到 null，循环结束。
> 如果有环，两个指针都进环后，快指针每步**追近慢指针 1 个节点**，
> 而环长有限，所以最多「环长」步必然追上。
> 不相遇只可能是无环，不存在「一直在环里追不上」的情况。

## 讲深一层

```cpp
bool hasCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

**为什么追近 1 而不是 2**：快走 2、慢走 1，相对速度是 1，所以每步距离减 1，不会「跳过」。

## 高频追问

1. **快指针走 3 步行不行？** —— 行，也能相遇，但可能多绕几圈；走 2 最简单。
2. **找环入口呢？** —— 相遇后把一个指针放回头部，两个都每次走一步，再次相遇处即入口。
3. **为什么入口算法成立？** —— 设头到入口 a、入口到相遇点 b、环长 L，可推出 a ≡ (L-b) mod L。

## 易错点

- ❌ 循环条件漏 `fast->next` —— 空指针解引用
- ❌ 先移动后比较 / 先比较后移动的顺序混
- ✅ 记住「相对速度 1，必然追上」
""",
    },
    {
        "kw": "相交链表", "diff": 2,
        "body": """## 题目

**输入**：两个链表头节点，返回第一个公共节点（无则 null）。

**问**：长度差法和「走两遍」各自的原理？

## 口述答案

> 「走两遍」最优雅：指针 A 走完链表 A 接着走 B，指针 B 走完 B 接着走 A，
> 两者走的总路程相同（a+b），所以**一定同时到达交点**；若无交点则同时到 null。
> 长度差法本质相同：先算出长度差，让长的先走差那么多步，再同时走。
> 前者代码更短，后者更好理解。

## 讲深一层

```cpp
ListNode *getIntersectionNode(ListNode *ha, ListNode *hb) {
    ListNode *a = ha, *b = hb;
    while (a != b) {
        a = a ? a->next : hb;
        b = b ? b->next : ha;
    }
    return a;
}
```

循环终止条件 `a != b`：要么在交点相遇，要么都变成 null。

## 高频追问

1. **会死循环吗？** —— 不会，最多 2×(a+b) 步。
2. **长度差法怎么算？** —— 两次遍历求长度，长的先走 |diff| 步。
3. **如何判断有交点？** —— 看两个尾节点是否相同。

## 易错点

- ❌ 用值相等判断交点 —— 值可能重复
- ❌ 走两遍时忘了在 null 时切换
- ✅ 说清「总路程相同所以同时到达」
""",
    },
    {
        "kw": "回文链表", "diff": 3,
        "body": """## 题目

**输入**：链表头节点，判断是否回文。
**要求**：O(n) 时间，O(1) 空间。

**问**：不额外开数组怎么做？

## 口述答案

> 三步：**快慢指针找中点** → **反转后半段** → **逐个比较**。
> 奇偶长度的处理要小心：奇数长度时慢指针正好在中点，后半段从中点的下一个开始比。
> 比较完可以把后半段再反转回来（好习惯，但不强制）。

## 讲深一层

```cpp
bool isPalindrome(ListNode* head) {
    if (!head || !head->next) return true;
    ListNode *slow = head, *fast = head;
    while (fast->next && fast->next->next) {     // 奇数时 slow 停在中点
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode *p = reverse(slow->next);           // 反转后半段
    ListNode *q = head;
    while (p) {
        if (p->val != q->val) return false;
        p = p->next; q = q->next;
    }
    return true;
}
```

循环条件用 `fast->next && fast->next->next` 而不是 `fast && fast->next`——后者偶数时 `slow` 会落在右中点，切分点要跟着变。

## 高频追问

1. **奇偶怎么统一？** —— 上面写法让 `slow` 总是左中点，`slow->next` 开始反转即可。
2. **比较完要恢复链表吗？** —— 严谨的话要，否则调用方的链表被改了。
3. **能用栈吗？** —— 能，但 O(n) 空间。

## 易错点

- ❌ 快慢指针条件写错 —— 中点位置偏一位
- ❌ 忘了判断空链表和单节点
- ✅ 掌握「找中点 + 反转 + 比较」三步
""",
    },
    {
        "kw": "有序数组的平方", "diff": 2,
        "body": """## 题目

**输入**：`nums = [-4,-1,0,3,10]`（非递减）
**输出**：`[0,1,9,16,100]`

**问**：为什么从两端取最大？

## 口述答案

> 因为负数平方后可能最大——数组两端的绝对值最大，所以平方后的最大值**必在两端之一**。
> 用两个指针从两端往中间走，每次取绝对值大的那个，平方后**从后往前填**结果数组。
> 从后往前填是关键：这样不用搬移元素。

## 讲深一层

```cpp
vector<int> sortedSquares(vector<int>& a) {
    int n = a.size(), l = 0, r = n - 1, k = n - 1;
    vector<int> res(n);
    while (l <= r) {
        if (abs(a[l]) > abs(a[r])) res[k--] = a[l] * a[l++];
        else                       res[k--] = a[r] * a[r--];
    }
    return res;
}
```

## 高频追问

1. **全是正数/全是负数还成立吗？** —— 成立，退化成简单情况。
2. **能原地吗？** —— 可以，但元素会互相覆盖，不推荐。
3. **为什么不用排序？** —— 平方后排序是 O(n log n)，双指针是 O(n)。

## 易错点

- ❌ 从前往后填 —— 需要额外搬移
- ❌ 比较平方值而不是绝对值（效果相同但容易溢出）
- ✅ 记住「两端绝对值最大」
""",
    },
    {
        "kw": "验证回文串", "diff": 1,
        "body": """## 题目

**输入**：`s = "A man, a plan, a canal: Panama"`
**输出**：`true`（忽略大小写和非字母数字）

**问**：怎么跳过非字母数字字符？

## 口述答案

> 双指针从两端往中间走，遇到非字母数字就跳过，比较时统一转小写。
> 关键是**两个指针都要跳过**，且跳过之后要重新检查边界，别越界。

## 讲深一层

```cpp
bool isPalindrome(string s) {
    int i = 0, j = s.size() - 1;
    while (i < j) {
        while (i < j && !isalnum(s[i])) ++i;
        while (i < j && !isalnum(s[j])) --j;
        if (tolower(s[i]) != tolower(s[j])) return false;
        ++i; --j;
    }
    return true;
}
```

`isalnum` 对负 char 是未定义行为，严格要 `isalnum((unsigned char)c)`。

## 高频追问

1. **中文怎么办？** —— `isalnum` 只处理 ASCII，Unicode 要自己判。
2. **能先把过滤后的串提出来吗？** —— 能，但 O(n) 额外空间。
3. **只考虑字母数字的另一种理解？** —— 有些题只要求字母，看清题面。

## 易错点

- ❌ 内层 while 不带 `i < j` —— 越界
- ❌ 用 `char` 直接传 `isalnum` —— 负数未定义
- ✅ 记住「双指针 + 跳过 + 统一大小写」
""",
    },
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    hits = 0
    for f in CONTENT.glob("Q-*.md"):
        txt = f.read_text(encoding="utf-8")
        m = re.search(r"^title:\s*(.+)$", txt, re.M)
        if not m:
            continue
        title = m.group(1)
        if "status: answered" in txt:
            continue
        for it in ITEMS:
            if it["kw"] not in title:
                continue
            fm = txt[:txt.index("\n---", 3) + 4]
            fm = re.sub(r"^status: .*$", "status: answered", fm, count=1, flags=re.M)
            fm = re.sub(r"^difficulty: .*$", f"difficulty: {it['diff']}", fm, count=1, flags=re.M)
            if not args.dry:
                f.write_text(fm + "\n\n" + it["body"] + TAIL, encoding="utf-8")
            hits += 1
            print(f"  ✓ {f.stem} {title[:32]}")
            break

    print(f"\n{'预览' if args.dry else '已补答案'} {hits} 道")
    return 0


if __name__ == "__main__":
    sys.exit(main())
