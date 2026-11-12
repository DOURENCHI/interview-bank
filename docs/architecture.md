# 架构说明 · CareerOS 求职功能台

> 单一真源：题目正文只在 `content/**/*.md`，结构化数据只在 `companies/` 与 `sources/*.json`，
> 网页 `dist/bank.html` 一律由 `tools/build.py` 生成。禁止手改成品 HTML。

## 一、分层与职责

| 层 | 位置 | 职责 | 产出 / 消费者 |
|---|---|---|---|
| 内容层 | `content/`（11 模块） | 一题一 `.md` + YAML frontmatter，口述稿体答案、手写 SVG 插图 | `tools/build.py` 读取 |
| 写卡层 | `tools/cards/*.cards`、`tools/apply_cards.py` | 纯文本写答案，避开 Python 中文引号转义 | 回灌到 `content/` |
| 校验层 | `tools/validate.py`、`tools/audit.py` | 字段/号段/小节/ID 唯一；重复与来源审计 | CI 门禁 |
| 数据层 | `companies/*.json`、`sources/*.json` | 目标公司池、雷达公司池、岗位模板、种子岗位、雷达快照 | 构建时注入 HTML |
| 采集层 | `tools/job_radar.py`、`tools/nc_collect.py` | 官方招聘门户低频增量扫描；牛客面经/真题增量 | `sources/jobs_radar.json` 等 |
| 构建层 | `tools/build.py` | 把 913 题卡 + 数据对象注入 `PAGE` 模板，产出单文件离线页 | `dist/bank.html`（约 5.3 MB） |
| 表现层 | `dist/bank.html` | 6 个视图、筛选、复习、训练、岗位匹配、公司总览；状态存 localStorage | 双击即开，无需服务端 |
| 自动化层 | `.github/workflows/radar.yml` / `ci.yml` | 每日 09:30 扫描；push 时校验+构建+审计+雷达逻辑回归 | 有 diff 才提交 |
| 测试层 | `tools/ui_test.py`、`tools/radar_test.py`、`tools/rep_test.py` | Edge/Playwright 冒烟、纯逻辑回归、报告回归 | 本机验收 |

## 二、数据流

```mermaid
flowchart LR
    A[content/*.md<br/>1033 题卡] --> B[tools/build.py]
    C[companies/*.json<br/>targets / radar_companies / jobs / profiles] --> B
    D[sources/jobs_radar.json<br/>岗位快照 667+ 岗] --> B
    N[sources/nowcoder_*<br/>面经索引 + 真题卷元数据] --> B
    T[sources/tutorial_map.json<br/>牛客宝典 16 章 40 节 + 映射规则] --> B
    PJ[companies/projects.json<br/>6 个项目 × 技能栈 × 证据四态] --> B
    B --> H2[HEALTH<br/>数据质量 13 项]
    B --> E[dist/bank.html<br/>单文件离线页]
    F[companies/radar_companies.json<br/>公司池 51 条] --> G[tools/job_radar.py --scan]
    G --> D
    G2[zhiye·feishu·moka·hotjob<br/>4 种 ATS 适配器] --> G
    H[.github/workflows/radar.yml<br/>每日 09:30] --> G
    NC[tools/nc_collect.py<br/>每周增量采集] --> N
    I[.github/workflows/ci.yml] --> J[validate / build / audit / radar_test]
    J --> E
```

用户浏览器里的自评、错题、收藏、忽略全部写 localStorage，**不回写仓库**；换设备用题库页「备份↓」导出 JSON。

## 二之一、采集适配器（4 种 ATS）

| ATS | 公司样例 | 方式 | 要点 |
|---|---|---|---|
| zhiye 智业云 | 宇树/优必选/联影/埃斯顿/黑芝麻/柏楚/普渡 | requests POST 直连 | portalId 缺失时逐候选探测 |
| feishu 飞书招聘 | 智元/启元/Momenta/小鹏/轻舟/小马/蔚来/禾赛/拓竹 | Playwright 监听 `search/job/posts` | 405-csrf 重试流程；/s/ 分享页需点「查看全部职位/校招内推」；渲染慢，failed 自动重试 1 次 |
| moka Moka | 元戎/文远知行/大疆/燧原/银河通用 | Playwright 抓 `a[href*="#/job/"]` DOM | jobs 接口响应加密，只能走 DOM；卡片文本含标题/城市/简介 |
| hotjob 大易 | 地平线（wecruit.hotjob.cn） | requests 表单 POST 分页 | 接口公开明文；`recruitType=1&currentPage=N`；详情链 `/mc/position/detail/{postId}` |

## 三、三个「池」必须分开理解

| 对象 | 文件 | 数量（2026-11-10） | 含义 |
|---|---|---|---|
| 目标公司池 | `companies/targets.json` | 130 家 | 题库公司/岗位族索引口径，按 JD 推导，**不是真实考题** |
| 雷达公司池 | `companies/radar_companies.json` | 52 条 / 启用 24 源 | 招聘入口登记表；`enabled=true` 且带 `source` 的 23 条才实际扫描 |
| 岗位快照 | `sources/jobs_radar.json` | 775 岗 | 官方门户扫到的岗位，带状态机与招聘性质分类 |
| 牛客同步 | `sources/nowcoder_experiences.jsonl` + `nowcoder_papers.csv` | 面经 80 篇 / 真题卷 124 套 | 每周增量；真题卷只存元数据 |
| 宝典考点地图 | `sources/tutorial_map.json` | 2 套宝典 / 16 章 / 40 节 | 牛客公开目录 + 章节→题库映射规则；构建期算命中题号 |
| 项目证据档案 | `companies/projects.json` | 6 个项目 | 技能栈（对齐 SKILLS 名字）+ 代码/指标/测试/文档证据 + 缺口；仓库未填=证据不完整 |

「公司」视图把前两者按名称合并（别名表 `NAME_ALIAS` 处理「小鹏集团 → 小鹏」），
同名去重后 152 家，并把第三者的岗位按公司聚合展示。

## 四、前端视图（hash 路由）

| hash | 视图 | 主要职责 |
|---|---|---|
| `#home` | 首页 | 数据卡、快速入口、今日任务、岗位进度、雷达可信行、公司/岗位总览入口 |
| `#bank` | 题库 | 全文搜索、chips/pills 筛选、答案折叠、自评 1~4、错题、备份 |
| `#train` | 训练 | 模拟面试、项目连环问、专项训练入口 |
| `#jobs` | 岗位 | **投递决策中心（四类）+ 五大岗位族** + 五维适配度 + JD 原文依据 + 技术岗过滤 + 雷达分页（18/页） |
| `#comp` | 公司（V1.8） | **全部公司 + 全部岗位**，按校招/实习/社招分组，含已收藏/已忽略 |
| `#rep` | 分析 | 牛客宝典考点地图、**训练闭环（7 天变化/复测/连续低分）**、项目证据链、系统健康、模块掌握度 |

localStorage 键：`ib_review_v1`（自评→间隔复习）、`ib_wrong_v1`、`ib_hist_v1`（训练历史）、
`ib_jobs_v1`（人工登记 + 雷达收藏转正）、`ib_jobs_dismiss_v1`（忽略，按 job_key）。

## 五、关键不变量

0. **适配度不合成单一百分比**：相关度/覆盖/掌握/证据/资格五维独立展示，任何一维都不能代表「能不能投」。
   抽不到的招聘条件一律 `未说明`，禁止默认符合；无自评一律 `数据不足`，禁止 50 分兜底。
1. `job_key = 公司 : 来源岗位ID : 归一化城市 : 批次`；收藏/忽略/下线判定全部按 key 隔离。
2. 采集失败 ≠ 岗位下线；连续 2 次成功扫描未见才标 `suspect`。
3. 招聘性质分类的证据优先级不可颠倒：岗位标题 > 来源批次标签 > 校园招聘入口推定。
4. 届别三态独立展示：覆盖（题库有没有）/ 掌握（自评）/ 资格（届别硬性条件）不互相抵消。
5. 合规：不登录、不绕验证码、不提交 Cookie/Token/简历，只读公开职位列表页。

## 六、版本轴

`CHANGELOG.md` 的 `v1.x` 是**题库内容版本**；代码注释里的 `CareerOS V1.5~V1.8` 是**功能台版本**，
两套编号独立，不要互相套用。本轮为功能台 V1.8（全部公司总览 + 招聘性质分类）。
