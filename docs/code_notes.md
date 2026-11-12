# 代码备注 · 关键函数 / 参数 / 数据结构

## 一、tools/build.py（单文件页面生成器）

`PAGE = r"""..."""` 是 **raw 字符串**，JS 里的 `\n` 不会被 Python 提前解释；
占位符 `__DATA__ / __TARGETS__ / __PROFILES__ / __JOBS__ / __RADAR__ / __POOL__ / __*OPTS__ / __COUNT__`
由 `main()` 逐个 `str.replace` 注入。不要在非 raw 字符串里写模板。

| 函数 / 常量 | 作用 |
|---|---|
| `load_questions()` | 扫描 `content/`，解析 YAML frontmatter + 正文小节，按模块/优先级排序 |
| `render()` | 题库主渲染，填充 `LASTHIT` 供模拟面试抽题 |
| `showView(v)` | 切 6 个视图并 `history.replaceState('#'+v)`；`comp` 分支调 `renderCompanies()` |
| `renderHome()` | 首页仪表盘；V1.8 追加招聘性质统计行与 `#h_allco` 跳转按钮 |
| `renderJobs()` / `jobMatch()` | 收藏岗位卡；匹配三维度 `cover / mastery / eli` + 技能四态 |
| `renderRadar()` | 只渲染 `pending.slice(0, 40)`；`pending = 非忽略 且 非收藏` |
| `renderCompanies()` | V1.8 全量公司 + 全量岗位，按性质分组 |
| `jobScore(job)` | → 命中数组 | 只产出事实：技能、层级、JD 片段、题库储备、自测均值（无自测=`avg:null`，**不再有 score=50**） |
| `jdSnippet(jd, kws)` | → 字符串 | 取 JD 里第一处命中词前后 30/42 字，作为「为什么判命中」的证据 |
| `eligibilityOf(job)` | → `{cls,txt,fields,bad,unknown}` | 五字段独立判定；抽不到=`未说明`；只对硬性不符判 `不符合` |
| `jobMatch(job)` | → `{hits,relevance,cover,mastery,evidence,eligibility,gaps}` | 五维各自独立，**不合成百分比** |
| `renderTut()` / `renderProj()` / `renderHealth()` | 无参数 | 考点地图 / 项目证据链 / 系统健康三个面板 |
| `backupPayload()` / `parseBackup()` / `planImport()` | → 对象 | 备份 v2：导出、校验归一化、合并计划（新增/更新/跳过） |
| `REV_DAYS` | SM-2 简化：自评 1/2/3/4 → 1/3/7/21 天 |
| `USER_GRAD = 2029` | 资格判断唯一依据；改届别只改这里 |
| `_rule_hit(q, rule)`（build.py 内） | → bool | 宝典章节映射判据：`modules`/`subs`/`terms` 三者 AND；**terms 只匹配标题+子方向+标签**，不匹配正文 |
| `renderTut()` | 无参数 | 渲染考点地图：tab、章卡片、节 chips、加权准备度、缺口提示 |
| `tutStat(ids)` / `tutScore(t)` / `tutDone(t)` | → `{n,done,avg}` / 0~100 / 已自测题数 | 准备度 = Σ 权重×(0.4×覆盖 + 0.6×均分/4) ÷ Σ 权重，只算 `weight>0` 的技术章 |
| `tutOpen(ids, label)` | 无返回值 | 写入 `tutFilter`（Set），清空其他筛选 → 切题库 → 渲染；题库顶部出提示条 |

V1.8 前端纯函数：

- `allCompanies()`：`POOL`（47 条）+ `TARGETS.companies`（128 家）按 `coKey()` 合并，
  `NAME_ALIAS = {'小鹏集团': '小鹏'}`，按 tier A/B/C 再按名称排序 → 152 家。
- `jobClass(j)`：历史快照兜底（缺 `job_class` 时按标题/批次判一次），正常路径直接读快照字段。
- `handleOf(j, dis, have)`：返回 `[显示文案, CSS 类]`，CSS 类带 `hs-` 前缀。
- `compFilter = {cls, src, st, q}`：`cls/st/q` 作用于岗位表，`src/q` 作用于公司表；
  公司表**不受性质与岗位状态筛选影响**，保证「全部公司」始终可见。
- 点公司行 → 写 `compFilter.q` + 搜索框 → `renderCompanies()` → 滚到岗位表。

## 二、tools/job_radar.py（雷达）

| 函数 | 参数 / 返回 | 原理 |
|---|---|---|
| `make_key(company, source_id, city, batch)` | → `公司:ID:归一化城市:批次` | 同岗多城市、多批次不误合并；收藏/忽略按 key 隔离 |
| `reconcile(old_jobs, scans, today)` | `scans={source_id:{status,jobs,error}}` → `(merged, src_states)` | 成功源才参与 missing 判断；失败源岗位原样保留；连续 `SUSPECT_AFTER=2` 次未见 → `suspect` |
| `classify_change(old, new)` | → 变更种类列表 | 职责/任职要求/届别/批次/地点/名称，保留最近 3 条 |
| `families_of(title, jd)` | → 岗位族列表 | 四层关键词打标，无命中归「其他」 |
| `classify_job(job, site)` | → **浅拷贝**，幂等 | V1.8 招聘性质分类，见下 |
| `class_stats_of(jobs)` | → `{class_stats, class_basis_stats}` | 写入快照供首页与总览显示 |
| `reclassify()` | 无参数，不联网 | 读快照 → 全量重分类 → 写回并重生成报告分类小节 |
| `scan_zhiye(site)` / `scan_feishu(site)` | → 岗位列表 | 北森智业云 POST 直连；飞书必须 Playwright 监听 `search/job/posts` 自然响应 |
| `scan_hotjob(site)` | site 需 `su`（wecruit 的 SUxxx 标识） | 大易公开表单接口：`POST /wecruit/positionInfo/listPosition/{su}`，body `recruitType=1&currentPage=N&pageSize=10`（**form-urlencoded，不是 JSON**）；详情链 `/{su}/mc/position/detail/{postId}` |
| `scan_moka(site)` | site 需 `url`（campus_apply/campus-recruitment 入口） | Moka `website/jobs/v2` 响应**加密**，改为 Playwright 渲染 `{url}#/jobs` + 滚动后抓 `a[href*="#/job/"]` 卡片 DOM；首行可能是「热招」徽标要跳过 |
| `city_from_title(title)` | → 城市串 | zhiye 系 LocNames 常为空，城市写在标题尾部（`- 上海(J19796)`、`（成都）`），两个正则兜底提取；key 里 city 随之变化——**改此逻辑后建议清空快照重扫**，否则旧 key 全部 missing 产生 suspect 垃圾 |
| （build.py）`const NC` | `sources/nowcoder_experiences.jsonl` + `nowcoder_papers.csv` | 面经索引与真题卷元数据注入；前端 `ncOf()` 按公司名宽松匹配（「华为HUAWEI」↔「华为」） |
| （build.py）`citiesOf(s)` / `CITY_PRI` | city 串 → 重点城市数组 | chips 动态生成：苏南五城 + 实习五城固定优先，其余按岗位数降序，保证计数全覆盖 |

### classify_job 的证据优先级（V1.8 核心）

| 优先级 | 证据 | `class_basis` | `class_conf` |
|---|---|---|---|
| 1 | 岗位标题含 实习/校招/社招/20xx届/顶才/探索者 | 岗位标题明确 | `high` |
| 2 | `label` / `batch` / `site.label`（先剥掉括号里的采集说明） | 来源批次标签 | `medium` |
| 3 | zhiye `category=2`、URL 含 `campus`、`type_label=校招` | 校园招聘入口推定 | `low` |
| 4 | 无线索 | 来源未标注 | `none` |

额外修正：判为「实习」时 `type` 改为 `实习`；若 `grad_year` 只来自入口批次推定
（标题里没写届别），置 `None` 并留 `grad_year_raw` / `grad_year_basis`，
避免把「2027 届校招入口里的实习生」误判成「只面向 2027 届」。
函数返回浅拷贝且不修改入参，`scan_all()` 对新岗位与合并后的全部岗位各调一次，保证幂等。

## 三、数据结构

`sources/jobs_radar.json`：

```json
{
  "updated": "2026-11-10T16:13:21+08:00",
  "sources": [{"source_id": "宇树科技·", "status": "success", "jobs_found": 63,
               "checked_at": "...", "error": null}],
  "pool_stats": {"pool_total": 47, "enabled": 9, "scanned_ok": 9, "ats_dist": {...}},
  "family_stats": {...},
  "class_stats": {"校招": 347, "实习": 4},
  "class_basis_stats": {"岗位标题明确": 96, "来源批次标签": 46, "校园招聘入口推定": 209},
  "jobs": [{"key": "...", "company": "...", "title": "...", "city": "...",
            "type": "校招", "batch": "2027届校招", "grad_year": 2027,
            "job_class": "校招", "class_basis": "岗位标题明确",
            "tech_relevant": true, "family_conf": "high",
            "req": {"education": "硕士及以上", "grad_range": [2027, 2027],
                    "student_status": "应届毕业生", "intern_duration": null,
                    "weekly_days": 4},
            "class_conf": "high", "class_evidence": "2027届",
            "jd": "...", "links": ["..."], "src": "feishu", "label": "...",
            "source_id": "...", "families": ["..."],
            "first_seen": "...", "last_seen": "...", "status": "open",
            "consecutive_missing": 0, "jd_hash": "...", "prev_jd_hash": "...",
            "change_log": []}]
}
```

`sources/tutorial_map.json`（V1.9.1 宝典目录 → 题库映射）：

```json
{
  "tutorials": [{
    "id": 93, "short": "C++ 工程师", "title": "【C++工程师面试宝典】",
    "url": "https://www.nowcoder.com/issue/tutorial?tutorialId=93&uuid=...",
    "articles": 30, "learners": "840.5W", "fit": "主线 · C++/嵌入式/机器人/智驾岗直接对口",
    "chapters": [{
      "no": "第2章", "name": "C/C++基础", "weight": 3,
      "emphasis": "原文：必考、且占比非常大",
      "rule": {"modules": ["02_cpp"]},
      "sections": [{"n": "语言基础", "rule": {"modules": ["02_cpp"], "subs": ["语言基础"]}},
                   {"n": "STL", "rule": {"modules": ["02_cpp"], "subs": ["STL 容器"]}},
                   {"n": "面向对象(二)"}]
    }]
  }],
  "practice": [{"label": "算法篇 · 面试高频 TOP 榜", "n": "600+", "url": "..."}]
}
```

构建期在 `build.py` 里为每章/每节补 `ids`（命中题号，`sections[].rule` 缺省时 `ids=null`），
再整体注入 `const TUT = ...`。因此页面上的「N 题」= 点进去实际筛选的题数，不存在估算偏差。
`rule` 三个键是 **AND** 关系：`modules`（模块）→ `subs`（子方向）→ `terms`（标题+子方向+标签关键词）。
改规则后必须重跑 `build.py`；只改 JSON 不会自动生效。

`companies/projects.json`（V2.0 项目证据）：

```json
{"projects": [{
  "id": "yolo_deploy", "name": "YOLO AI 推理部署", "sub": "YOLO 部署", "tier": "核心",
  "stack": ["C++", "Linux", "模型部署", "Python", "深度学习/感知"],
  "evidence": {"code": {"status": "partial", "note": "..."},
               "metric": {"status": "present", "note": "..."},
               "test": {"status": "partial", "note": "..."},
               "doc": {"status": "present", "note": "..."}},
  "repo": "", "gaps": ["CUDA Kernel 自研"]
}]}
```

`stack` 必须与页面 `SKILLS[].name` 完全一致，否则岗位卡的「工程证据」匹配不到；
`evidence.*.status` 只有 `present / partial / missing`，构建期会给每个项目补 `interview_count`（项目深挖题数）。

`companies/radar_companies.json` 的每条：`company_id / company_name / category / directions /
tier(A|B|C) / career_url / ats_type(zhiye|feishu|hotjob|self-built|unknown) /
source{base,portal_id,category 或 url,label,type_label} / enabled / note`。
只有 `enabled=true` **且** 有 `source` 的条目进入 `scan_all()`。

## 四、易踩的设计约束

- `type` 是采集器给的原始招聘类型，**不能**当作分类结论；分类一律读 `job_class`。
- `grad_year` 为 `None` 表示「未标注」，不等于「不限届别」；实习岗是显式清除并留痕。
- 前端 CSS 全局类 `.todo / .done / .lo / .hi` 等已被题卡占用，新组件的类名要加前缀（如 `hs-`）。
- `RADAR.sources[].jobs_found` 是计数，不是岗位数组；岗位只在 `RADAR.jobs` 里。
