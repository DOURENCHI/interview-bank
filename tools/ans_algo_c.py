#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算法题补答案（第 3 批：DFS/BFS 15 道 + DP 15 道）。

用法: python tools/ans_algo_c.py [--dry]
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
    # ==================== DFS / BFS ====================
    {"kw": "岛屿数量", "diff": 2, "body": """## 题目

**输入**：`grid = [["1","1","0"],["1","0","0"],["0","0","1"]]`
**输出**：`2`

**问**：DFS 和 BFS 各自的取舍？

## 口述答案

> 遍历每个格子，遇到 `'1'` 就计数加一，然后从这个格子开始把连通的所有 `'1'` 都「淹掉」（改成 `'0'`）。
> 淹的过程用 DFS（代码短）或 BFS（队列，不会爆栈）。
> 关键一步是**访问后立刻标记**，否则会重复访问甚至死循环。

## 讲深一层

```cpp
void dfs(vector<vector<char>>& g, int i, int j) {
    if (i < 0 || i >= (int)g.size() || j < 0 || j >= (int)g[0].size() || g[i][j] != '1') return;
    g[i][j] = '0';                                  // 立刻标记
    dfs(g, i+1, j); dfs(g, i-1, j); dfs(g, i, j+1); dfs(g, i, j-1);
}
int numIslands(vector<vector<char>>& g) {
    int cnt = 0;
    for (int i = 0; i < (int)g.size(); ++i)
        for (int j = 0; j < (int)g[0].size(); ++j)
            if (g[i][j] == '1') { ++cnt; dfs(g, i, j); }
    return cnt;
}
```

| 方式 | 优点 | 缺点 |
|---|---|---|
| DFS | 代码短 | 大规模网格可能爆栈 |
| BFS | 不爆栈 | 要显式队列 |

## 高频追问

1. **网格很大怎么办？** —— 改 BFS 或迭代栈，避免递归深度。
2. **不能修改原网格呢？** —— 用 `visited` 数组，多 O(mn) 空间。
3. **八连通呢？** —— 方向数组扩到 8 个。

## 易错点

- ❌ 访问后才标记（应先标记再递归）
- ❌ 边界判断漏一个方向
- ✅ 说清「淹岛」这个思路
"""},
    {"kw": "岛屿的最大面积", "diff": 2, "body": """## 题目

**输入**：`grid = [[0,0,1,0],[1,1,1,0],[0,1,0,0]]`
**输出**：`4`

**问**：怎么在递归里累计面积？

## 口述答案

> `dfs` 返回 `1 + 四周返回值之和`，越界或为 0 时返回 0。
> 本质是把「这格算 1 个，再加上邻居的」写成递归式。
> 同样要访问后立刻置 0。

## 讲深一层

```cpp
int dfs(vector<vector<int>>& g, int i, int j) {
    if (i < 0 || i >= (int)g.size() || j < 0 || j >= (int)g[0].size() || g[i][j] == 0) return 0;
    g[i][j] = 0;
    return 1 + dfs(g,i+1,j) + dfs(g,i-1,j) + dfs(g,i,j+1) + dfs(g,i,j-1);
}
int maxAreaOfIsland(vector<vector<int>>& g) {
    int best = 0;
    for (int i = 0; i < (int)g.size(); ++i)
        for (int j = 0; j < (int)g[0].size(); ++j)
            if (g[i][j]) best = max(best, dfs(g, i, j));
    return best;
}
```

## 高频追问

1. **会不会重复计数？** —— 不会，置 0 后不会再进入。
2. **最大岛屿的坐标也要？** —— 额外记录路径。
3. **和岛屿数量的区别？** —— 一个计数连通块，一个求最大块。

## 易错点

- ❌ 忘了 `g[i][j] = 0`
- ❌ 返回值写成 `+1` 的位置错
- ✅ 说清「1 + 四周之和」
"""},
    {"kw": "被围绕的区域", "diff": 3, "body": """## 题目

**输入**：`board`，把被 `'X'` 完全包围的 `'O'` 翻成 `'X'`，边界上的 `'O'` 保留。

**问**：为什么从边界反向 DFS？

## 口述答案

> 正向判断「这个 O 是否被包围」要搜到边界才知道，每个 O 都可能搜一遍，代价高。
> 反过来想：**与边界连通的 O 一定不会被包围**。所以先从四条边上的 O 出发，
> 把能到达的都标记成特殊字符（如 `'#'`），这些是安全区；
> 最后扫一遍：安全区还原成 O，剩下的 O 翻成 X。

## 讲深一层

```cpp
void dfs(vector<vector<char>>& b, int i, int j) {
    if (i<0||i>=(int)b.size()||j<0||j>=(int)b[0].size()||b[i][j]!='O') return;
    b[i][j] = '#';
    dfs(b,i+1,j); dfs(b,i-1,j); dfs(b,i,j+1); dfs(b,i,j-1);
}
void solve(vector<vector<char>>& b) {
    int R = b.size(), C = b[0].size();
    for (int i = 0; i < R; ++i) { dfs(b,i,0); dfs(b,i,C-1); }
    for (int j = 0; j < C; ++j) { dfs(b,0,j); dfs(b,R-1,j); }
    for (auto& row : b) for (auto& c : row)
        c = (c == '#') ? 'O' : 'X';
}
```

## 高频追问

1. **为什么标 `'#'` 而不是直接改 `'O'`？** —— 需要区分「安全」和「原始」，最后统一归一化。
2. **能不用递归吗？** —— 用栈或队列做 BFS。
3. **只翻内部所有 O 呢？** —— 那就是全翻，不用判断。

## 易错点

- ❌ 正向逐个判断 —— 复杂度高
- ❌ 忘了四条边都要扫
- ✅ 记住「从边界反推安全区」
"""},
    {"kw": "腐烂的橘子", "diff": 2, "body": """## 题目

**输入**：`grid = [[2,1,1],[1,1,0],[0,1,1]]`（2 腐烂、1 新鲜、0 空）
**输出**：`4`（分钟数），无法全部腐烂返回 -1。

**问**：多源 BFS 的分钟数怎么算？

## 口述答案

> 所有腐烂橘子**同时入队**作为第 0 层，然后逐层 BFS，每扩一层分钟数加一。
> BFS 结束后再检查是否还有新鲜橘子，有就返回 -1。
> 关键点是「同时入队」——这保证每一层都是同一时刻被感染的，层数才等价于时间。

## 讲深一层

```cpp
int orangesRotting(vector<vector<int>>& g) {
    int R = g.size(), C = g[0].size(), fresh = 0;
    queue<pair<int,int>> q;
    for (int i = 0; i < R; ++i) for (int j = 0; j < C; ++j) {
        if (g[i][j] == 2) q.push({i,j});
        else if (g[i][j] == 1) ++fresh;
    }
    if (!fresh) return 0;
    int dir[4][2] = {{1,0},{-1,0},{0,1},{0,-1}}, mins = 0;
    while (!q.empty()) {
        int sz = q.size();
        bool spread = false;
        for (int k = 0; k < sz; ++k) {
            auto [i,j] = q.front(); q.pop();
            for (auto& d : dir) {
                int x = i+d[0], y = j+d[1];
                if (x>=0&&x<R&&y>=0&&y<C&&g[x][y]==1) {
                    g[x][y] = 2; q.push({x,y}); --fresh; spread = true;
                }
            }
        }
        if (spread) ++mins;
    }
    return fresh ? -1 : mins;
}
```

## 高频追问

1. **为什么要按层（记 size）循环？** —— 不按层就没法算分钟数。
2. **初始没有腐烂橘子但有新鲜的？** —— 直接返回 -1。
3. **没有新鲜橘子？** —— 返回 0。

## 易错点

- ❌ 一个一个入队 —— 层数不等于时间
- ❌ 忘了最后检查 fresh
- ✅ 说清「多源同时入队 = 同一时刻」
"""},
    {"kw": "01 矩阵", "diff": 2, "body": """## 题目

**输入**：`mat = [[0,0,0],[0,1,0],[1,1,1]]`
**输出**：每个格子到最近 0 的距离

**问**：多源 BFS 求最近距离怎么初始化？

## 口述答案

> 把**所有 0 都入队**，距离设为 0，其余设为 -1（未访问）。
> 然后 BFS 逐层外扩，每到一个未访问格子就写「当前距离 + 1」。
> 因为是多源同时出发，**第一次到达某格时就是最短距离**，不用比较。

## 讲深一层

```cpp
vector<vector<int>> updateMatrix(vector<vector<int>>& m) {
    int R = m.size(), C = m[0].size();
    vector<vector<int>> d(R, vector<int>(C, -1));
    queue<pair<int,int>> q;
    for (int i = 0; i < R; ++i) for (int j = 0; j < C; ++j)
        if (m[i][j] == 0) { d[i][j] = 0; q.push({i,j}); }
    int dir[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    while (!q.empty()) {
        auto [i,j] = q.front(); q.pop();
        for (auto& dd : dir) {
            int x = i+dd[0], y = j+dd[1];
            if (x>=0&&x<R&&y>=0&&y<C&&d[x][y]==-1) {
                d[x][y] = d[i][j] + 1; q.push({x,y});
            }
        }
    }
    return d;
}
```

## 高频追问

1. **为什么不用对每个 1 单独 BFS？** —— 那是 O(mn) 次 BFS，太慢。
2. **DP 两遍法呢？** —— 也可以：左上、右下各扫一遍取 min，O(mn)。
3. **距离是曼哈顿距离吗？** —— 四连通 BFS 得到的就是曼哈顿距离。

## 易错点

- ❌ 只从一个 0 出发
- ❌ 用 -1 当未访问又拿它参与运算
- ✅ 说清「多源 + 首达即最短」
"""},
    {"kw": "课程表", "diff": 2, "body": """## 题目

**输入**：`numCourses = 2, prerequisites = [[1,0]]`（学 1 前要先学 0）
**输出**：能否修完（即图中有无环）

**问**：拓扑排序怎么判断有环？

## 口述答案

> 统计每个节点的入度，入度为 0 的先入队；出队时把它指向的节点入度减一，减到 0 就入队。
> 最后看**出队节点数是否等于总节点数**：少了就说明剩下的节点互相依赖，在环里。
> 这就是 Kahn 算法。

## 讲深一层

```cpp
bool canFinish(int n, vector<vector<int>>& pre) {
    vector<vector<int>> g(n);
    vector<int> indeg(n, 0);
    for (auto& p : pre) { g[p[1]].push_back(p[0]); ++indeg[p[0]]; }
    queue<int> q;
    for (int i = 0; i < n; ++i) if (!indeg[i]) q.push(i);
    int done = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop(); ++done;
        for (int v : g[u]) if (--indeg[v] == 0) q.push(v);
    }
    return done == n;
}
```

| 方法 | 判断环 |
|---|---|
| Kahn（BFS） | 完成数 < n 则有环 |
| DFS 三色标记 | 遇到「正在访问」的节点则有环 |

## 高频追问

1. **DFS 版怎么写？** —— 白/灰/黑三色，灰色表示在当前路径上，遇到灰色即有环。
2. **为什么入度 0 可以安全移除？** —— 没有前驱依赖了。
3. **有多个解怎么办？** —— 拓扑序不唯一，Kahn 出队顺序即一个合法解。

## 易错点

- ❌ 忘了把 `prerequisites` 的方向建对（先学 → 后学）
- ❌ 用「出队数 == n」判断写成 `<=`
- ✅ 说清「完成数不足即环」
"""},
    {"kw": "课程表 II", "diff": 2, "body": """## 题目

**输入**：`numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]`
**输出**：`[0,2,1,3]`（任一合法顺序），无解返回空数组。

**问**：BFS 拓扑排序的输出顺序就是答案吗？

## 口述答案

> 是。Kahn 算法里节点出队的顺序天然就是一个合法拓扑序——每个节点出队时它的所有前驱都已处理完。
> 有环时出队数量不足 n，返回空数组。

## 讲深一层

```cpp
vector<int> findOrder(int n, vector<vector<int>>& pre) {
    vector<vector<int>> g(n);
    vector<int> indeg(n, 0), res;
    for (auto& p : pre) { g[p[1]].push_back(p[0]); ++indeg[p[0]]; }
    queue<int> q;
    for (int i = 0; i < n; ++i) if (!indeg[i]) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop(); res.push_back(u);
        for (int v : g[u]) if (--indeg[v] == 0) q.push(v);
    }
    return res.size() == (size_t)n ? res : vector<int>{};
}
```

## 高频追问

1. **字典序最小的拓扑序？** —— 把队列换成小根堆。
2. **为什么结果不唯一？** —— 同时入度为 0 的节点顺序任意。
3. **DFS 版怎么输出？** —— 后序遍历的逆序。

## 易错点

- ❌ 有环时不返回空
- ❌ 用 DFS 后序却忘了反转
- ✅ 说清「出队即合法」
"""},
    {"kw": "克隆图", "diff": 2, "body": """## 题目

**输入**：连通无向图的节点，返回深拷贝。

**问**：DFS 里怎么避免重复克隆和死循环？

## 口述答案

> 用一个哈希表存「原节点 → 克隆节点」。进入一个节点时先查表，
> 已有就直接返回那副本，没有就新建、存表、再递归克隆它的邻居。
> 这个表同时解决了两个问题：**避免重复克隆**和**避免环导致死循环**。

## 讲深一层

```cpp
unordered_map<Node*, Node*> mp;
Node* clone(Node* n) {
    if (!n) return nullptr;
    if (mp.count(n)) return mp[n];
    Node* c = new Node(n->val);
    mp[n] = c;                                   // 先存再递归
    for (Node* nb : n->neighbors) c->neighbors.push_back(clone(nb));
    return c;
}
```

`mp[n] = c` 必须在递归之前——否则环会无限递归。

## 高频追问

1. **BFS 版怎么写？** —— 队列 + 同样的哈希表，先把节点建出来再连边。
2. **图不连通呢？** —— 外层再遍历一遍所有节点。
3. **为什么用节点指针当 key？** —— 值可能重复，指针唯一。

## 易错点

- ❌ 先递归再存表 —— 环上死循环
- ❌ 只克隆节点不克隆边
- ✅ 记住「先建节点存表，再连边」
"""},
    {"kw": "单词搜索", "diff": 3, "body": """## 题目

**输入**：`board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`, `word = "ABCCED"`
**输出**：`true`

**问**：回溯的剪枝和状态恢复怎么做？

## 口述答案

> 从每个格子出发尝试匹配第一个字符，匹配就递归四个方向匹配下一个字符。
> 剪枝：越界、字符不匹配**立刻返回 false**，不回退尝试。
> 状态恢复：匹配后**临时把该格改成特殊字符**标记已访问，四个方向递归完再改回来——
> 不恢复会污染其他分支。

## 讲深一层

```cpp
bool dfs(vector<vector<char>>& b, string& w, int i, int j, int k) {
    if (k == (int)w.size()) return true;
    if (i<0||i>=(int)b.size()||j<0||j>=(int)b[0].size()||b[i][j]!=w[k]) return false;
    char tmp = b[i][j];
    b[i][j] = '#';                                  // 标记
    bool ok = dfs(b,w,i+1,j,k+1) || dfs(b,w,i-1,j,k+1)
           || dfs(b,w,i,j+1,k+1) || dfs(b,w,i,j-1,k+1);
    b[i][j] = tmp;                                  // 恢复
    return ok;
}
```

## 高频追问

1. **为什么要恢复？** —— 同一条路径不能重复用同一格，但不同起点可以。
2. **能提前剪枝吗？** —— 统计字符频次，若 word 里某字符比 board 多，直接 false。
3. **复杂度？** —— O(mn × 4^L)，L 为单词长度。

## 易错点

- ❌ 不恢复状态 —— 后续路径被堵死
- ❌ 先判 k 还是先判边界，顺序错会越界
- ✅ 说清「标记—递归—恢复」三步
"""},
    {"kw": "二叉树的最大深度", "diff": 1, "body": """## 题目

**输入**：二叉树根节点，返回最大深度。

**问**：递归和层序各自怎么算？

## 口述答案

> 递归：`maxDepth(root) = 1 + max(左, 右)`，空节点返回 0。
> 层序：用队列按层遍历，每处理完一层层数加一。
> 前者代码最短；后者能顺带拿到宽度、某层节点等信息。

## 讲深一层

```cpp
int maxDepth(TreeNode* r) {
    if (!r) return 0;
    return 1 + max(maxDepth(r->left), maxDepth(r->right));
}
```

层序版：

```cpp
int maxDepth(TreeNode* r) {
    if (!r) return 0;
    queue<TreeNode*> q{{r}};
    int d = 0;
    while (!q.empty()) {
        for (int i = q.size(); i > 0; --i) {
            auto* n = q.front(); q.pop();
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        ++d;
    }
    return d;
}
```

## 高频追问

1. **最小深度呢？** —— 注意只有单侧子树时不能直接取 min（那是 0）。
2. **会爆栈吗？** —— 深度大时会，改迭代。
3. **平衡二叉树判断？** —— 后序遍历，返回高度并检查左右差。

## 易错点

- ❌ 空节点返回 1
- ❌ 最小深度直接取 min 忽略单侧
- ✅ 说清两种方法的取舍
"""},
    {"kw": "二叉树的层序遍历", "diff": 1, "body": """## 题目

**输入**：二叉树根节点
**输出**：`[[3],[9,20],[15,7]]`

**问**：为什么必须用队列？

## 口述答案

> 队列先进先出，保证**同一层的节点按顺序被处理、下一层的节点排在后面**。
> 用栈会变成深度优先，就不是按层了。
> 实现上每轮先记下**当前层的节点数 `q.size()`**，只处理这么多个，
> 就能自然分层。

## 讲深一层

```cpp
vector<vector<int>> levelOrder(TreeNode* r) {
    vector<vector<int>> res;
    if (!r) return res;
    queue<TreeNode*> q{{r}};
    while (!q.empty()) {
        int sz = q.size();
        vector<int> lv;
        for (int i = 0; i < sz; ++i) {
            auto* n = q.front(); q.pop();
            lv.push_back(n->val);
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        res.push_back(lv);
    }
    return res;
}
```

`sz` 必须在循环**之前**取——循环中 size 会变。

## 高频追问

1. **锯齿形层序？** —— 偶数层反转。
2. **右视图？** —— 每层取最后一个。
3. **不用 sz 行不行？** —— 用两个队列或加层标记。

## 易错点

- ❌ 循环里用 `q.size()` 当条件 —— 会处理到新入队的
- ❌ 忘了判空树
- ✅ 记住「先取 size 再循环」
"""},
    {"kw": "验证二叉搜索树", "diff": 2, "body": """## 题目

**输入**：二叉树，判断是否为 BST。

**问**：为什么只比较父子不够？

## 口述答案

> 因为 BST 要求**整棵左子树都小于根**，不只是左孩子。
> 反例：根 5，左孩子 4，4 的右孩子 6 —— 局部 4<5 成立，但 6 在左子树里却大于根。
> 正确做法有两种：**传上下界**（递归时带 `[min, max]`），
> 或者**中序遍历检查严格递增**。

## 讲深一层

```cpp
bool check(TreeNode* r, long lo, long hi) {
    if (!r) return true;
    if (r->val <= lo || r->val >= hi) return false;
    return check(r->left, lo, r->val) && check(r->right, r->val, hi);
}
bool isValidBST(TreeNode* r) { return check(r, LONG_MIN, LONG_MAX); }
```

用 `long` 是因为节点值可能就是 `INT_MIN`/`INT_MAX`。

中序版：记录前一个节点，要求严格递增。

## 高频追问

1. **等于算不算 BST？** —— 标准定义不允许重复，用严格不等。
2. **中序版怎么写？** —— 递归左、比较 pre、递归右。
3. **为什么用 long？** —— 避免边界值被误判。

## 易错点

- ❌ 只比较父子 —— 漏判深层
- ❌ 用 int 当界的初值
- ✅ 记住「传上下界」或「中序递增」
"""},
    {"kw": "二叉树的中序遍历", "diff": 2, "body": """## 题目

**要求**：用迭代写法实现中序遍历。

**问**：为什么必须显式用栈？

## 口述答案

> 因为中序是「左 → 根 → 右」，必须先把左链一路压到底才能访问根，
> 而递归的调用栈会自动帮你记住「回来之后该访问谁」。
> 迭代就要手动模拟这个栈：**一路向左压栈**，弹出访问，再转向右子树。

## 讲深一层

```cpp
vector<int> inorderTraversal(TreeNode* r) {
    vector<int> res;
    stack<TreeNode*> st;
    while (r || !st.empty()) {
        while (r) { st.push(r); r = r->left; }   // 一路向左
        r = st.top(); st.pop();
        res.push_back(r->val);                    // 访问
        r = r->right;                             // 转向右
    }
    return res;
}
```

前序：访问提前到入栈时；后序：用双栈或标记法。

## 高频追问

1. **前序迭代怎么写？** —— 压栈时先访问，然后压右再压左。
2. **后序迭代？** —— 前序改成「根右左」，最后反转。
3. **Morris 遍历？** —— 利用叶子节点的空右指针，O(1) 空间。

## 易错点

- ❌ 外层条件只写 `!st.empty()` —— 根还没压入时直接退出
- ❌ 忘了 `r = r->right`
- ✅ 说清「一路向左压栈」
"""},
    {"kw": "路径总和 II", "diff": 2, "body": """## 题目

**输入**：二叉树 + 目标和，找出所有「根到叶子」路径和等于目标。

**问**：回溯时怎么恢复路径？

## 口述答案

> 进入节点先 `push`，递归左右，**返回前 `pop`**。
> 少一次 pop 就会把别的分支的节点留在路径里，结果串成一堆错路径。
> 判断时机在叶子节点：左右都空时检查当前和是否等于目标。

## 讲深一层

```cpp
void dfs(TreeNode* r, int need, vector<int>& path, vector<vector<int>>& res) {
    if (!r) return;
    path.push_back(r->val);
    need -= r->val;
    if (!r->left && !r->right && need == 0) res.push_back(path);
    dfs(r->left, need, path, res);
    dfs(r->right, need, path, res);
    path.pop_back();                             // 关键
}
```

## 高频追问

1. **为什么要判叶子？** —— 不判的话中途满足也会被收，但那不是完整路径。
2. **有负数节点要注意什么？** —— 不能提前剪枝（后面可能变回来）。
3. **只求是否存在？** —— 那就不用记录路径，直接返回 bool。

## 易错点

- ❌ 忘了 pop
- ❌ 不判叶子
- ✅ 说清「进 push、出 pop」
"""},
    {"kw": "N 皇后", "diff": 3, "body": """## 题目

**输入**：`n = 4`
**输出**：所有解的布局，共 2 个。

**问**：怎么用三个数组做到 O(1) 冲突判断？

## 口述答案

> 逐行放置，每行一个皇后。冲突只有三种：同列、同主对角线、同副对角线。
> 用三个布尔数组：`col[j]`、`diag1[row-j+n]`、`diag2[row+j]`。
> 放之前查三个，放完标记三个，回溯时撤销三个。
> 这样判断冲突是 O(1)，不用每次扫棋盘。

## 讲深一层

```cpp
void solve(int row, int n, vector<int>& pos,
           vector<bool>& col, vector<bool>& d1, vector<bool>& d2,
           vector<vector<string>>& res) {
    if (row == n) { /* 生成答案 */ return; }
    for (int j = 0; j < n; ++j) {
        if (col[j] || d1[row-j+n] || d2[row+j]) continue;
        col[j] = d1[row-j+n] = d2[row+j] = true;
        pos[row] = j;
        solve(row+1, n, pos, col, d1, d2, res);
        col[j] = d1[row-j+n] = d2[row+j] = false;
    }
}
```

对角线下标的推导：主对角线满足 `row - j` 为常数（加 n 避免负下标），副对角线满足 `row + j` 为常数。

## 高频追问

1. **为什么按行放？** —— 每行一个，天然排除行冲突。
2. **位运算优化？** —— 用整数位表示列和对角线占用，更快。
3. **N=8 有多少解？** —— 92 个。

## 易错点

- ❌ 对角线下标不加偏移 —— 负下标越界
- ❌ 回溯时忘撤销
- ✅ 记住 `row-j+n` 和 `row+j`
"""},

    # ==================== DP ====================
    {"kw": "爬楼梯", "diff": 1, "body": """## 题目

**输入**：`n = 5`（每次走 1 或 2 阶）
**输出**：`8`

**问**：为什么它和斐波那契是同一道题？

## 口述答案

> 到第 n 阶，最后一步只能是从 n-1 走 1 阶，或从 n-2 走 2 阶。
> 所以 `dp[n] = dp[n-1] + dp[n-2]`，和斐波那契完全一样，只是初值不同（dp[1]=1, dp[2]=2）。
> 只要两个变量滚动就能 O(1) 空间。

## 讲深一层

```cpp
int climbStairs(int n) {
    if (n <= 2) return n;
    int a = 1, b = 2;
    for (int i = 3; i <= n; ++i) { int c = a + b; a = b; b = c; }
    return b;
}
```

| 方法 | 空间 | 说明 |
|---|---|---|
| 数组 DP | O(n) | 直观 |
| **滚动变量** | **O(1)** | 最优 |
| 矩阵快速幂 | O(log n) | n 极大时用 |

## 高频追问

1. **每次可走 1..k 阶？** —— 前缀和优化或完全背包。
2. **不能连续走 2 阶？** —— 加状态维度。
3. **n 到 1e18？** —— 矩阵快速幂 + 取模。

## 易错点

- ❌ 初值搞错（dp[0]=1 还是 0）
- ❌ 忘了取模（题目要求时）
- ✅ 说清「最后一步的来源」
"""},
    {"kw": "打家劫舍", "diff": 1, "body": """## 题目

**输入**：`nums = [2,7,9,3,1]`
**输出**：`12`（偷 2 + 9 + 1）
**限制**：不能偷相邻两家。

**问**：状态转移里「选或不选」怎么表达？

## 口述答案

> `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`。
> 意思是：不偷第 i 家，就等于前 i-1 家的最优；偷第 i 家，就得跳过 i-1，取前 i-2 家的最优再加。
> 两个选择取大。
> 同样可以滚动成两个变量。

## 讲深一层

```cpp
int rob(vector<int>& a) {
    int prev = 0, cur = 0;               // dp[i-2], dp[i-1]
    for (int x : a) {
        int t = max(cur, prev + x);
        prev = cur; cur = t;
    }
    return cur;
}
```

| 状态定义 | 转移 |
|---|---|
| dp[i] = 前 i 家最大 | max(dp[i-1], dp[i-2]+a[i]) |
| 滚动 | prev/cur 两变量 |

## 高频追问

1. **环形房屋？** —— 拆成「不含首」和「不含尾」两次（见打家劫舍 II）。
2. **树形房屋？** —— 树形 DP，返回「偷/不偷」两个值。
3. **能连续偷两家呢？** —— 状态扩展成「最近一次偷的是距离 k」。

## 易错点

- ❌ `dp[i-1]` 和 `dp[i-2]` 混
- ❌ 滚动时更新顺序错
- ✅ 说清「偷当前就必须跳过前一个」
"""},
    {"kw": "最长递增子序列", "diff": 3, "body": """## 题目

**输入**：`nums = [10,9,2,5,3,7,101,18]`
**输出**：`4`（`[2,3,7,101]`）

**问**：O(n²) 和 O(n log n) 两种解法差在哪？

## 口述答案

> O(n²)：`dp[i]` 表示「以 i 结尾的 LIS 长度」，转移是 `dp[i] = max(dp[j]) + 1, j<i 且 a[j]<a[i]`。
> O(n log n)：维护一个 `tails` 数组，`tails[k]` 表示长度为 k+1 的递增子序列的**最小结尾**。
> 遍历每个数，用二分找到它该放的位置并替换，数组长度就是答案。
> 关键洞察：结尾越小，后面越容易接上，所以只留最小结尾。

## 讲深一层

```cpp
int lengthOfLIS(vector<int>& a) {
    vector<int> tails;
    for (int x : a) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;                    // 替换成更小的结尾
    }
    return tails.size();
}
```

注意 `tails` **不是 LIS 本身**，只是长度正确。

## 高频追问

1. **要还原 LIS 怎么做？** —— 额外记录每个元素的前驱下标。
2. **严格递增 vs 非递减？** —— 用 `lower_bound`（严格）或 `upper_bound`（允许相等）。
3. **为什么替换是对的？** —— 替换不改变已有长度的可达性，只让后续更容易接。

## 易错点

- ❌ 把 `tails` 当答案输出
- ❌ `lower_bound` 和 `upper_bound` 用混
- ✅ 说清「结尾越小越容易接」
"""},
    {"kw": "零钱兑换", "diff": 2, "body": """## 题目

**输入**：`coins = [1,2,5], amount = 11`
**输出**：`3`（5+5+1）

**问**：为什么贪心不行，必须 DP？

## 口述答案

> 贪心每次取最大面额，在某些面额组合下会错过更优解。
> 例如面额 `[1,3,4]`、金额 6：贪心得 4+1+1=3 枚，最优是 3+3=2 枚。
> 所以必须 DP：`dp[j] = min(dp[j], dp[j-coin]+1)`，枚举所有面额，取最小枚数。

## 讲深一层

```cpp
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);      // 用 amount+1 表示无穷
    dp[0] = 0;
    for (int j = 1; j <= amount; ++j)
        for (int c : coins)
            if (c <= j) dp[j] = min(dp[j], dp[j - c] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
}
```

这是**完全背包**：每种硬币可用无限次，所以内层正序、外层是金额或硬币都可以。

## 高频追问

1. **为什么用 `amount+1` 当无穷？** —— 最大枚数不会超过 amount（全用 1 元），安全且不会溢出。
2. **求方案数呢？** —— `dp[j] += dp[j-c]`，且必须外层枚举硬币、内层正序（避免重复计数）。
3. **0-1 背包和完全背包在代码上差什么？** —— 内层循环方向（倒序 vs 正序）。

## 易错点

- ❌ 用贪心
- ❌ 无穷大用 INT_MAX 导致 +1 溢出
- ✅ 说清「完全背包的正序」
"""},
    {"kw": "0-1 背包", "diff": 3, "body": """## 题目

**输入**：`n` 个物品（重量 w、价值 v），背包容量 `W`，每件最多取一次。
**输出**：最大价值。

**问**：为什么内层循环必须倒序？

## 口述答案

> 因为一维数组压缩时，`dp[j]` 依赖的是「上一轮」的 `dp[j-w]`。
> 正序遍历时，`dp[j-w]` 可能已经被**本轮**更新过，相当于同一件物品被选了多次，变成完全背包。
> 倒序保证 `dp[j-w]` 还是上一轮的值，才是真正的「每件最多一次」。

## 讲深一层

```cpp
int knapsack(vector<int>& w, vector<int>& v, int W) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < (int)w.size(); ++i)
        for (int j = W; j >= w[i]; --j)          // 倒序
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    return dp[W];
}
```

| 背包类型 | 内层方向 | 含义 |
|---|---|---|
| 0-1 | **倒序** | 每件一次 |
| 完全 | 正序 | 每件无限 |

## 高频追问

1. **二维数组版要倒序吗？** —— 不用，因为 `dp[i][j]` 依赖 `dp[i-1][...]`，天然隔离。
2. **要求恰好装满？** —— 初始化为 -inf，`dp[0]=0`。
3. **求方案数？** —— `dp[j] += dp[j-w[i]]`。

## 易错点

- ❌ 内层正序 —— 变成完全背包
- ❌ 内层起点写 0 而不是 `w[i]`（虽不出错但浪费）
- ✅ 能解释「倒序 = 用上一轮的值」
"""},
    {"kw": "分割等和子集", "diff": 2, "body": """## 题目

**输入**：`nums = [1,5,11,5]`
**输出**：`true`（`[1,5,5]` 和 `[11]`）

**问**：怎么转化成 0-1 背包？

## 口述答案

> 分成两个和相等的子集，等价于「能否从数组里挑出若干个数，和恰好为总和的一半」。
> 所以目标和 `target = sum/2`，`sum` 为奇数直接 false。
> 然后就是 0-1 背包：`dp[j]` 表示能否凑出和 j，内层倒序。

## 讲深一层

```cpp
bool canPartition(vector<int>& a) {
    int sum = accumulate(a.begin(), a.end(), 0);
    if (sum & 1) return false;
    int t = sum / 2;
    vector<bool> dp(t + 1, false);
    dp[0] = true;
    for (int x : a)
        for (int j = t; j >= x; --j)          // 倒序
            dp[j] = dp[j] || dp[j - x];
    return dp[t];
}
```

## 高频追问

1. **为什么奇数直接 false？** —— 两个相等的整数和必然是偶数。
2. **能优化吗？** —— 可以用 bitset 加速，或先做「最大数 > target 直接 false」的剪枝。
3. **求具体方案？** —— 记录选择路径。

## 易错点

- ❌ 内层正序
- ❌ 忘了判奇数
- ✅ 说清「目标和 = 总和/2」
"""},
    {"kw": "编辑距离", "diff": 3, "body": """## 题目

**输入**：`word1 = "horse", word2 = "ros"`
**输出**：`3`

**问**：三种操作对应 DP 表的哪三个方向？

## 口述答案

> `dp[i][j]` 表示 word1 前 i 个字符变成 word2 前 j 个字符的最少操作数。
> 三种操作对应三个方向：**插入**看左边 `dp[i][j-1]`、**删除**看上边 `dp[i-1][j]`、
> **替换**看左上 `dp[i-1][j-1]`。
> 三者取最小再加 1；如果当前字符相等，直接取左上不加一。

## 讲深一层

```cpp
int minDistance(string a, string b) {
    int m = a.size(), n = b.size();
    vector<vector<int>> dp(m+1, vector<int>(n+1));
    for (int i = 0; i <= m; ++i) dp[i][0] = i;   // 全删
    for (int j = 0; j <= n; ++j) dp[0][j] = j;   // 全插
    for (int i = 1; i <= m; ++i)
        for (int j = 1; j <= n; ++j) {
            if (a[i-1] == b[j-1]) dp[i][j] = dp[i-1][j-1];
            else dp[i][j] = 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
        }
    return dp[m][n];
}
```

## 高频追问

1. **为什么插入看左、删除看上？** —— 因为 `dp[i][j-1]` 表示 word1 前 i 个已经变成 word2 前 j-1 个，差一个字符要插入。
2. **只能替换/删除呢？** —— 去掉对应方向。
3. **空间能压缩吗？** —— 能压成两行，但要保存上一行。

## 易错点

- ❌ 边界初始化漏（第 0 行/列）
- ❌ 字符相等时也加 1
- ✅ 记住「左=插入、上=删除、左上=替换」
"""},
    {"kw": "最长公共子序列", "diff": 2, "body": """## 题目

**输入**：`text1 = "abcde", text2 = "ace"`
**输出**：`3`（`"ace"`）

**问**：二维 DP 的边界怎么设？

## 口述答案

> `dp` 开 `(m+1) × (n+1)`，第 0 行和第 0 列全为 0，表示「其中一个串为空」。
> 这样不用特判 i-1/j-1。
> 转移：字符相等取左上 + 1；不等取上、左的较大值。

## 讲深一层

```cpp
int longestCommonSubsequence(string a, string b) {
    int m = a.size(), n = b.size();
    vector<vector<int>> dp(m+1, vector<int>(n+1, 0));
    for (int i = 1; i <= m; ++i)
        for (int j = 1; j <= n; ++j)
            dp[i][j] = (a[i-1] == b[j-1])
                     ? dp[i-1][j-1] + 1
                     : max(dp[i-1][j], dp[i][j-1]);
    return dp[m][n];
}
```

## 高频追问

1. **和「最长公共子串」什么区别？** —— 子串要求连续，不等时直接置 0。
2. **空间压缩？** —— 用两行或一维倒序。
3. **要输出具体 LCS？** —— 从右下角回溯。

## 易错点

- ❌ 下标从 0 开始却用 `dp[i-1][j-1]` —— 越界
- ❌ 不等时忘了取 max
- ✅ 记住「多开一行一列当边界」
"""},
    {"kw": "不同路径", "diff": 2, "body": """## 题目

**输入**：`m = 3, n = 7`
**输出**：`28`

**问**：为什么组合数也能解？

## 口述答案

> 从左上到右下，一共走 `m+n-2` 步，其中 `m-1` 步向下、`n-1` 步向右。
> 所以答案就是「从 m+n-2 步里选 m-1 步向下」的组合数 `C(m+n-2, m-1)`。
> DP 的转移 `dp[i][j] = dp[i-1][j] + dp[i][j-1]` 本质上就是在算这个。

## 讲深一层

```cpp
int uniquePaths(int m, int n) {
    vector<int> dp(n, 1);
    for (int i = 1; i < m; ++i)
        for (int j = 1; j < n; ++j)
            dp[j] += dp[j-1];
    return dp[n-1];
}
```

一维 DP：`dp[j]` 是「上方来的」，`dp[j-1]` 是「左方来的」。

## 高频追问

1. **有障碍物呢？** —— 障碍处置 0。
2. **组合数会溢出吗？** —— 会，m、n 大时要用高精度或取模。
3. **能走三个方向吗？** —— 那 DP 就不适用了（有环），要另想。

## 易错点

- ❌ 一维 DP 初始化全 1 但第一列处理错
- ❌ 组合数直接算阶乘溢出
- ✅ 说清「向下 m-1 步、向右 n-1 步」
"""},
    {"kw": "最小路径和", "diff": 2, "body": """## 题目

**输入**：`grid = [[1,3,1],[1,5,1],[4,2,1]]`
**输出**：`7`（1→3→1→1→1）

**问**：二维 DP 怎么压缩成一维？

## 口述答案

> `dp[j]` 存「到当前行第 j 列的最小和」。按行原地更新：
> `dp[j] = min(dp[j], dp[j-1]) + grid[i][j]`。
> 其中 `dp[j]`（更新前）是「从上方来的」，`dp[j-1]`（已更新）是「从左方来的」。
> 一行就够，因为每个格子只依赖上和左。

## 讲深一层

```cpp
int minPathSum(vector<vector<int>>& g) {
    int R = g.size(), C = g[0].size();
    vector<int> dp(C);
    dp[0] = g[0][0];
    for (int j = 1; j < C; ++j) dp[j] = dp[j-1] + g[0][j];   // 第一行
    for (int i = 1; i < R; ++i) {
        dp[0] += g[i][0];                                     // 第一列
        for (int j = 1; j < C; ++j)
            dp[j] = min(dp[j], dp[j-1]) + g[i][j];
    }
    return dp[C-1];
}
```

## 高频追问

1. **第一行/第一列为什么要单独处理？** —— 它们只有一个方向可来。
2. **空间还能更省吗？** —— 原地修改 grid，O(1) 额外空间。
3. **求最大路径和呢？** —— 把 min 换 max。

## 易错点

- ❌ 第一行/第一列没单独初始化
- ❌ `dp[j]` 和 `dp[j-1]` 的更新顺序错
- ✅ 说清「上 = 更新前、左 = 已更新」
"""},
    {"kw": "单词拆分", "diff": 2, "body": """## 题目

**输入**：`s = "leetcode", wordDict = ["leet","code"]`
**输出**：`true`

**问**：为什么用 DP 而不是 DFS 暴搜？

## 口述答案

> 暴搜会**重复计算同一个后缀**——比如 "aaab" 从不同起点切，会反复判断 "ab" 能不能拆。
> DP 把「前 i 个字符能否拆分」记下来：`dp[i] = OR over j<i (dp[j] && s[j:i] in dict)`。
> 每个位置只算一次，复杂度 O(n²·L)。

## 讲深一层

```cpp
bool wordBreak(string s, vector<string>& dict) {
    unordered_set<string> st(dict.begin(), dict.end());
    int n = s.size();
    vector<bool> dp(n + 1, false);
    dp[0] = true;
    for (int i = 1; i <= n; ++i)
        for (int j = 0; j < i; ++j)
            if (dp[j] && st.count(s.substr(j, i - j))) { dp[i] = true; break; }
    return dp[n];
}
```

## 高频追问

1. **要返回所有拆法？** —— 那就得 DFS + 剪枝或记忆化。
2. **字典很大怎么优化？** —— 用 Trie 或按最大词长限制 j 的范围。
3. **字符串匹配开销？** —— `substr` 每次 O(L)，可换哈希。

## 易错点

- ❌ `dp[0]` 忘了设 true
- ❌ j 的范围写错
- ✅ 说清「dp[i] 表示前缀可拆」
"""},
    {"kw": "乘积最大子数组", "diff": 3, "body": """## 题目

**输入**：`nums = [2,3,-2,4]`
**输出**：`6`（`[2,3]`）

**问**：为什么要同时维护最大和最小？

## 口述答案

> 因为**负数会让最小值翻成最大值**。
> 比如当前最小值是 -8，乘以下一个 -1 就变成 +8，可能是全局最大。
> 所以同时记 `maxEnd` 和 `minEnd`，遇到负数时先交换两者再更新。

## 讲深一层

```cpp
int maxProduct(vector<int>& a) {
    int mx = a[0], mn = a[0], best = a[0];
    for (int i = 1; i < (int)a.size(); ++i) {
        if (a[i] < 0) swap(mx, mn);        // 负数翻转
        mx = max(a[i], mx * a[i]);
        mn = min(a[i], mn * a[i]);
        best = max(best, mx);
    }
    return best;
}
```

不交换也可以，写成三者取 max/min：

```cpp
int t1 = mx * a[i], t2 = mn * a[i];
mx = max({a[i], t1, t2});
mn = min({a[i], t1, t2});
```

## 高频追问

1. **和最大子数组和的区别？** —— 加法有单调性（负前缀丢弃），乘法没有（负负得正）。
2. **有 0 怎么办？** —— 乘 0 后归零，上面的转移自然处理。
3. **能滚动吗？** —— 已经是 O(1)。

## 易错点

- ❌ 只维护最大值 —— 遇到负数就错
- ❌ 先更新 mx 再算 mn，用到了新值
- ✅ 说清「负数翻转」
"""},
    {"kw": "打家劫舍 II", "diff": 2, "body": """## 题目

**输入**：`nums = [2,3,2]`（房屋围成环）
**输出**：`3`（不能同时偷首尾）

**问**：环形怎么拆成两个线性？

## 口述答案

> 首尾不能同时偷，所以分两种情况：
> **不偷第一个**（考虑 1..n-1）和**不偷最后一个**（考虑 0..n-2），取两者较大值。
> 两种情况都退化成线性的打家劫舍 I。
> 这样就把环拆成了两条链，每条都保证首尾不同时选。

## 讲深一层

```cpp
int robRange(vector<int>& a, int l, int r) {
    int prev = 0, cur = 0;
    for (int i = l; i <= r; ++i) {
        int t = max(cur, prev + a[i]);
        prev = cur; cur = t;
    }
    return cur;
}
int rob(vector<int>& a) {
    int n = a.size();
    if (n == 1) return a[0];
    return max(robRange(a, 0, n-2), robRange(a, 1, n-1));
}
```

## 高频追问

1. **n=1/2 要特判吗？** —— n=1 要（否则区间为空）。
2. **为什么是「不偷首」和「不偷尾」两种？** —— 覆盖了「首尾最多选一个」的所有合法情况。
3. **树形版本？** —— 树 DP，返回偷/不偷两个值。

## 易错点

- ❌ n=1 时越界
- ❌ 区间端点写错（应该是 0..n-2 和 1..n-1）
- ✅ 说清「首尾最多选一个」
"""},
    {"kw": "股票买卖含冷冻期", "diff": 3, "body": """## 题目

**规则**：卖出后第二天不能买（冷冻一天），可交易多次。
**问**：状态机 DP 有哪几个状态？

## 口述答案

> 三个状态：**持有股票**、**不持有且在冷冻期**、**不持有且可买**。
> 转移：
> 持有 = max(昨天持有, 昨天可买 - 今天价格)；
> 冷冻 = 昨天持有 + 今天价格（今天卖出）；
> 可买 = max(昨天可买, 昨天冷冻)。
> 答案取「冷冻」和「可买」的较大值。

## 讲深一层

```cpp
int maxProfit(vector<int>& p) {
    int hold = INT_MIN, freeze = 0, free_ = 0;
    for (int x : p) {
        int nh = max(hold, free_ - x);
        int nf = hold + x;
        int nfree = max(free_, freeze);
        hold = nh; freeze = nf; free_ = nfree;
    }
    return max(freeze, free_);
}
```

## 高频追问

1. **为什么 `hold` 初始化成 `INT_MIN`？** —— 表示「还没买」，非法状态，不能被选中。
2. **冷冻期两天呢？** —— 加一个状态或用队列记历史。
3. **含手续费？** —— 卖出时减手续费。

## 易错点

- ❌ 状态定义不清就直接写转移
- ❌ 用新值算旧状态（要先存临时变量）
- ✅ 先把三个状态和转移写清楚
"""},
    {"kw": "正则表达式匹配", "diff": 3, "body": """## 题目

**输入**：`s = "aab", p = "c*a*b"`
**输出**：`true`
**规则**：`.` 匹配任意单字符，`*` 匹配前一个字符 0 次或多次。

**问**：DP 状态怎么定义？

## 口述答案

> `dp[i][j]` 表示「s 的前 i 个字符」能否被「p 的前 j 个字符」匹配。
> 关键在 `*`：它要和前一个字符一起看。
> 如果 `p[j-1]` 是 `*`，有两种选择：
> **用 0 次**（`dp[i][j-2]`），或**用一次以上**（`s[i-1]` 与 `p[j-2]` 匹配且 `dp[i-1][j]`）。

## 讲深一层

```cpp
bool isMatch(string s, string p) {
    int m = s.size(), n = p.size();
    vector<vector<bool>> dp(m+1, vector<bool>(n+1, false));
    dp[0][0] = true;
    for (int j = 2; j <= n; ++j)
        if (p[j-1] == '*') dp[0][j] = dp[0][j-2];   // 空串匹配 a*b*
    for (int i = 1; i <= m; ++i)
        for (int j = 1; j <= n; ++j) {
            if (p[j-1] == '*') {
                dp[i][j] = dp[i][j-2];                                  // 0 次
                if (p[j-2] == '.' || p[j-2] == s[i-1])
                    dp[i][j] = dp[i][j] || dp[i-1][j];                  // 多次
            } else {
                if (p[j-1] == '.' || p[j-1] == s[i-1])
                    dp[i][j] = dp[i-1][j-1];
            }
        }
    return dp[m][n];
}
```

## 高频追问

1. **为什么 `dp[0][j]` 要单独初始化？** —— 空串也能被 `a*b*c*` 匹配。
2. **`dp[i-1][j]` 为什么不是 `dp[i-1][j-2]`？** —— 用多次时 `*` 还在，要继续匹配剩余。
3. **回溯写法？** —— 可以，但会有重复子问题。

## 易错点

- ❌ `*` 当成独立字符处理
- ❌ 空串的初始化漏掉
- ✅ 说清「0 次 vs 多次」两种转移
"""},
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    hits = 0
    for f in CONTENT.glob("Q-*.md"):
        txt = f.read_text(encoding="utf-8")
        m = re.search(r"^title:\s*(.+)$", txt, re.M)
        if not m or "status: answered" in txt:
            continue
        title = m.group(1)
        for it in ITEMS:
            if it["kw"] not in title:
                continue
            fm = txt[:txt.index("\n---", 3) + 4]
            fm = re.sub(r"^status: .*$", "status: answered", fm, count=1, flags=re.M)
            fm = re.sub(r"^difficulty: .*$", f"difficulty: {it['diff']}", fm, count=1, flags=re.M)
            if not args.dry:
                f.write_text(fm + "\n\n" + it["body"] + TAIL, encoding="utf-8")
            hits += 1
            print(f"  ✓ {title[:30]}")
            break

    print(f"\n{'预览' if args.dry else '已补答案'} {hits} 道")
    return 0


if __name__ == "__main__":
    sys.exit(main())
