# 调试日志 · 问题 / 原因 / 解决 / 验证

按时间倒序；每条都写清「怎么验证的」，避免同类问题复发。

## 2026-11-10 · CareerOS V1.8（全部公司总览 + 招聘性质分类）

### 1. 用户看到「其余 81 道已收藏/忽略，不重复显示」，看不到全部公司与岗位

- **现象**：岗位雷达折叠区只列 40 条待处理新发现，其余岗位被隐藏；文案还把「被 40 条截断」与「已收藏/忽略」混为一谈。
- **原因**：`renderRadar()` 用 `jobs.filter(...).slice(0,40)`，`hidden = jobs.length - show.length` 把两类原因合并成一个数字；而公司池 47 条（45 家）从未在页面上完整列出。
- **解决**：新增第 6 个视图 `#comp`（`renderCompanies()`），公司表列两池去重后的全部 152 家，岗位表列全部 351 岗（含已收藏/已忽略），按 `实习 / 校招 / 社招 / 未标明` 分组；雷达区改为精确文案「显示 X / 待处理 Y；已收藏或忽略 N 条、未展开 M 条」并加跳转按钮；首页、岗位页也加入口。
- **验证**：`ui_test.py` 新增 10 项断言（全量行数、分组、分类筛选数量、公司表不受分类影响、已收藏/已忽略仍可查、搜索联动、点公司行联动、首页跳转）→ 47/47 通过；浏览器截图核对统计卡与表格排版。

### 2. 351 岗全部被硬编码成「校招」，实习岗被误标 2027 届

- **现象**：快照 `type` 全是 `校招`；`batch` 245 条为空、`grad_year` 274 条为空；4 个标题带「实习生」的岗位里 3 个带着从批次推来的 `grad_year=2027`。
- **原因**：`scan_zhiye` 用 `site.category=="2"` 兜底、`scan_feishu` 用 `site.type_label` 默认值，都是**入口级**信息；`grad_year` 又允许从 `batch` 回推，实习岗因此被套上届别硬条件。
- **解决**：新增 `classify_job()`，按「标题 > 批次标签 > 入口推定」三级证据产出 `job_class / class_basis / class_conf / class_evidence`；实习岗清掉批次推定的届别并留 `grad_year_raw`；新增 `--reclassify` 离线回填；快照与报告附 `class_stats / class_basis_stats`。
- **结果**：校招 347 / 实习 4；依据分布 标题明确 96 · 批次标签 46 · 入口推定 209。首页「技能参考」从 77 降到 74（3 个实习岗不再被当作 2027 届校招）。
- **验证**：`radar_test.py` 新增 10 项（标题/批次/入口/无线索/社招、实习届别清除、幂等、统计、池映射）→ 22/22 通过；`--reclassify` 实跑输出核对。

### 3. 公司总览全空：`byCo is not defined`

- **现象**：切到「🏢 公司」后统计卡、公司表、岗位表全空，但视图切换本身正常；手动打开单页时却正常。
- **原因**：编辑时把 `const byCo = {};` 那行随旧代码一起替换掉了，只留下 `const jobsByCo = {}`，函数执行到 `byCo[k]` 抛 `ReferenceError`；`showView()` 里 `classList.toggle` 在 `renderCompanies()` 之前，所以视图看起来「切成功了」，错误被掩盖。
- **解决**：补回声明；并在 `ui_test.py` 开头注册 `pageerror` 监听，末尾加「无 JS 运行时错误」断言——以后任何渲染期异常都会被测试直接抓住。
- **验证**：修复前复现得到 `PAGEERROR: byCo is not defined`；修复后 `getComputedStyle`/行数检查与 47 项 UI 全通过。

### 4. 岗位标题全是红色斜体

- **现象**：岗位表里 349 条「待处理」行标题呈红色斜体，像报错/已作废。
- **原因**：行 CSS 类直接用了 `todo / saved / dismissed`，与题卡全局样式 `.todo{color:#a63a2e;font-style:italic}` 撞名，整行继承红色斜体。
- **解决**：处理状态类统一加 `hs-` 前缀（`hs-todo / hs-saved / hs-dismissed`），筛选判断改为 `h !== 'hs-' + st`（`h` 本身已是 `handleOf()[1]` 字符串，**不要再写 `h[1]`**）；约定新组件类名一律加前缀。
- **验证**：`getComputedStyle(.jt).color` 从 `rgb(166,58,46)` 恢复 `rgb(45,42,33)`，`fontStyle` 从 `italic` 恢复 `normal`，截图复核。改前缀时曾误写成 `h[1] !== ...`（对字符串取下标恒为单字符），导致「已收藏 / 已忽略」筛选结果为空，被 `ui_test.py` 的两项断言当场抓到并修正。

### 5. 统计卡第 7 张单独换行、右侧大片空白；雷达卡片「发现 undefined」

- **原因**：7 张卡 `flex:1 1 145px` 在 1060px 容器里放不下一行；`renderRadar()` 读 `j.found`，而快照字段是 `first_seen`。
- **解决**：卡片精简为 6 张（`flex:1 1 140px`），目标池 128 家改在说明行写清；`found` 改为 `j.found || j.first_seen || ''`；公司表/岗位表最后一列设 `min-width:118px`。
- **验证**：截图核对 6 张卡一行、表格列不挤压。

### 6. 重跑体检脚本后，人工复核附录被覆盖丢失

- **现象**：`python tools/audit.py` 之后 `sources/audit_report.md` 少了末尾 18 行「附：相似题复核记录（4 张污染卡修复 + 25 对有意保留）」。
- **原因**：脚本每次都用 `"\n".join(L)` **整份重写**，而这段附录是人工补写的、不在自动生成内容里。
- **解决**：写报告前读旧文件，若含「## 附：」则把该段落原样带回并追加；本次已从 git 版本恢复原文。
- **验证**：再跑一次 `audit.py`，`git diff sources/audit_report.md` 为空（附录仍在），报告主体也保持 913 题 / 24 对可疑重复 / 缺来源 0。

## 历史问题（前几轮已修，保留结论）

| 问题 | 原因 | 解决 |
|---|---|---|
| Python 字符串里中文引号转义炸掉 | 答案正文混在 Python 源码字符串 | 改用 `tools/cards/*.cards` 纯文本写卡器 + `apply_cards.py` 回灌 |
| 正则 `\b` 对中文失效 | CJK 无单词边界 | 改本地子串匹配 |
| 题卡 ID 越界撞号段 | 早期模块间距 100 太小 | 号段改 500，由 `validate.py` 强制检查 |
| 「已答 948」虚计 | `status=draft` 的空壳卡被计入 | 按答案实际内容重判 21 张 answered / 35 张 indexed 删除；真实数 913 |
| 牛客详情链接 404 | URL 结构不是讨论列表 | 改 `/discuss/{contentId}`；过滤参数无效改本地匹配 |
| 飞书招聘 requests 405 / Brotli 乱码 | 岗位数据只在页面渲染后的 XHR 里 | Playwright 监听 `search/job/posts` 自然响应；`networkidle` 超时改 `domcontentloaded` + `expect_response(status 200)` |
| 小鹏营销落地页 405-csrf | 需点「职位」才进列表路由 | 点击兜底 + 列表页 `/campus/position/list` |
| 2027 届 / 2029 届混淆 | 把岗位面向届别当成用户届别 | `USER_GRAD=2029` + `grad_year/batch/type` 字段分离 |
| V1.6 首扫新增岗位误入 changed、旧 key 重复 | `job_key` schema 升级 | `changed` 加 `k not in added`；删旧快照重扫 |
| 学习报告浮层打不开 | `openRep()` 漏 `display='flex'` / `--accent` 未定义 | 补齐；报告改平铺分析视图 |
| 岗位视图 6 列表竖排 | `.trgrid` 240px 窄卡 | `#joblist` 改单列全宽 |
| GitHub HTTPS 推送 502 | 本机代理对 CONNECT 隧道不通 | 一律 SSH（`~/.ssh/id_ed25519`），`git remote set-url origin git@github.com:...` |
