# 抖音图文 → 题库 流水线

把「秋招博主」的**图文作品**里每张图上的文字自动读出来，切成面试题，去重后进 `content/`。

三段脚本，各管一段，可以单独跑、单独重跑：

```mermaid
flowchart LR
    A[博主主页链接] --> B[tools/douyin_works.py<br/>枚举作品]
    B --> C[sources/douyin_works.json]
    C --> D[tools/douyin_ocr.py<br/>下载图片 + OCR]
    D --> E[sources/douyin_ocr.jsonl]
    E --> F[tools/douyin_seed.py<br/>切题 + 去重]
    F --> G[sources/douyin_candidates.json]
    G --> H[人工/模型复核 → 写题卡]
```

## 为什么要多写两个脚本

`douyin-scraper` skill 只吃**单个作品链接**（`/note/` `/video/` `/slides/`），能下载图文作品的所有图片，
但**不能列出一个博主的所有作品**。所以补了 `douyin_works.py` 做枚举。

枚举方式不是自己拼接口（抖音的 `a_bogus` 签名会失效），而是**在浏览器里打开主页、听抖音自己发起的
作品列表请求**——我们只在旁边读响应，页面照常正常加载，不伪造请求、不改参数。

## 用法

```bash
PY="/c/Users/DOUDOU/.workbuddy/binaries/python/envs/default/Scripts/python"   # 带 playwright 的解释器

# 1) 枚举作品（公开号一般不需要登录）
"$PY" tools/douyin_works.py "https://www.douyin.com/user/<sec_uid>" --max 200

# 1b) 若页面要求登录：先扫码登录一次，登录态会存到 _cache/douyin_profile/storage.json
"$PY" tools/douyin_works.py "<主页链接>" --login

# 2) 下载图片并 OCR
"$PY" tools/douyin_ocr.py --limit 30            # 先小批量试
"$PY" tools/douyin_ocr.py --engine tesseract    # 指定引擎

# 3) 切题 + 与现有题库去重（只出候选清单，不写题卡）
"$PY" tools/douyin_seed.py --dry
```

## OCR 引擎

| 引擎 | 状态 | 说明 |
|---|---|---|
| **tesseract 5.5 + chi_sim** | ✅ 已装（语言包需手动补） | `D:\msys64\ucrt64\bin\tesseract.EXE`；chi_sim.traineddata 已放到 `D:\msys64\ucrt64\share\tessdata\` |
| RapidOCR（PP-OCR 中文） | ⏳ 可选，装了自动优先 | 逐行置信度更高、艺术字更稳 |

补语言包（换机器时需要）：

```bash
curl -L -o /d/msys64/ucrt64/share/tessdata/chi_sim.traineddata \
  https://github.com/tesseract-ocr/tessdata_fast/raw/main/chi_sim.traineddata
```

## 实测准确率（2026-11-23，真实抖音图）

以「校招博主Alex」公开作品为样本：

| 图片类型 | 例子 | tesseract | RapidOCR |
|---|---|---|---|
| 表格型（大字、留白多） | 「2024 届名企校招信息表」 | **约 95%**，行结构完整（公司/类型/时间一一对应） | 文字更准，但**单元格对应关系丢失**（读成「24届秋招科大讯飞6月19日…」） |
| 纯文字卡 | 「这些公司秋招岗位刚刚放出！」 | 约 90% | 约 95% |
| 营销拼贴 / 密排小图 | 9 张小图拼接 + 装饰字 | **整段乱码**（实测「让 sjpaajia 全微个\| DOD4届ID」） | **可用**（「微博12024届sina新浪校园招聘月20日申请截止！2024秋招\|滴滴2024届校招产研提前批启动…」） |

结论：**题目类图片（单栏、大字）基本可用**；拼贴类必须走人工或换引擎。
每页都会记 `conf` 置信度，低置信页在清单里会标出来，可以只复核这些。

## OCR 后处理（已实现的坑）

- `”` → `？`（中文问号被识别成右引号，实测高频）
- `C+ +` → `C++`（加号被拆开）
- 折行合并：中文直接相接、英文之间补空格；**「问：」「答：」行与项目符号行不参与合并**（否则整页连成一行）
- 水印/营销噪声过滤：关注我、点赞收藏、扫码、第 N 期、#话题 等

## 判重：三层，不靠单一阈值

| 层 | 规则 | 动作 |
|---|---|---|
| ① 包含关系 | 归一化后一方包含另一方（≥6 字） | 直接判重 |
| ② Dice 相似度 | ≥ 0.62 | 直接判重 |
| ③ 主题交集 | 剥疑问词后的技术术语与题库标题求交集（含子串） | **只标记「疑似同主题」，不丢弃**，留给人工判断 |

为什么要有第 ③ 层：短题干用 Dice 会漏判——
「进程和线程的核心区别是什么？」vs 题库「进程和线程有什么区别？」只有 0.57，擦着 0.62 过去了；
术语交集能抓住（进程 / 线程）。
术语表是从**题库自身标题**里长出来的（剥掉疑问词、剪掉首尾虚词），不依赖人工维护词库。

## 实测：三层判重在真实题卡上的表现

用一张仿抖音题卡（8 道操作系统题）跑全链路：

```
⛔ 判重(相似 0.89) 协程和线程有什么区别？        → Q-1501
⚠️ 疑似同主题 进程和线程的核心区别是什么？      → Q-0754[线程] / Q-1207[进程]
⚠️ 疑似同主题 什么是虚拟内存？为什么需要它？    → Q-1532[虚拟内存]
⚠️ 疑似同主题 死锁的四个必要条件是什么？        → Q-1208[死锁]
⚠️ 疑似同主题 什么是零拷贝？有哪些实现方式？    → Q-4586[零拷贝]
⚠️ 疑似同主题 什么是内存屏障？为什么需要它？    → Q-1215[内存屏障]
⚠️ 疑似同主题 线程池的参数怎么设置？            → Q-1510[线程池]
汇总：真新题 0 / 判重 1 / 疑似同主题 6
```

结论：**操作系统这一块题库已经覆盖得很全**，抖音博主发的同题材题目大概率是重复题，
真正能补进来的多半是冷门方向（数据库/设计模式/具体八股细节）——这也是先做三层判重、再谈入库的原因。

另有一组反向验证：拿「校招博主Alex」的 16 张**投递信息图**（不是面试题）跑一遍，
候选 **0 道**——质量筛没让任何营销内容污染题库。

## 切题规则

支持三种版式：编号清单（`1. 题`）、问答配对（`问：… / 答：…`）、每行一题。
质量筛：长度 6~60、必须含疑问词或问号、滤掉营销语。
去重：与现有 1033 道题做 Dice 相似度，≥0.62 直接判重；同批次内 0.85 判重。
候选清单会带上「近似题号 + 相似度」，方便快速扫一眼就知道是新题还是老题。

## 文字笔记路线（2026-11-24 新增，tools/douyin_article.py）

部分博主发的是**文字笔记**（aweme_type=163，正文直接在 detail 接口里），不需要 OCR：

```
python tools/douyin_article.py --enum  <主页URL> --out sources/douyin_works_b4.json   # 枚举并区分 article/video
python tools/douyin_article.py --fetch --works sources/douyin_works_b4.json --out sources/douyin_text_b4.jsonl
```

- `--fetch` 未登录即可拿到 `aweme_detail.article_info.article_content` 全量正文（实测 659~1624 字/篇）；
- 真**视频**作品未登录只能拿到 60s 预览音轨，完整视频需登录（`tools/douyin_login.py` 扫码存 `_cache/douyin_state.json`）+ ASR（faster-whisper，`tools/douyin_video.py --state` 自动注入登录态，模型 Systran/faster-whisper-small 已缓存，HF_ENDPOINT=https://hf-mirror.com 可重下）；
- **视频两分支判定**（2026-11-24 实测 ADC+DMA 视频得出）：ASR 转 0 字且音量正常（mean_volume ≈ -12dB）→ 多半是**图卡动画+BGM 无旁白**，改走抽帧 OCR：`ffmpeg -i x.bin -vf fps=1 frames/f%03d.png` + RapidOCR 逐帧去重；有旁白的教学视频才走 whisper（vad_filter=True）。CUDA 转写报 `cublas64_12.dll is not found` → douyin_video.py 已修（torch/lib 加 DLL 目录）；图卡视频转写结果记 `"model": "frames+rapidocr"`；
- 文字正文转成 `douyin_ocr_*.jsonl` 兼容格式（text 当作单页 OCR 结果，conf=1.0）后，照常走 `douyin_seed.py` 切题判重。

## 视频讲解型博主（video_asr 路线，2026-11-25 实践）

纯视频博主（如 b11 具身智能科普）的转写是**成段讲解**，不是题面清单，`douyin_seed.py` 的切题规则
（6~60 字、必须含疑问词）不适用——**不走 seed，人工/AI 读转写甄别**：

1. `douyin_works.py` 枚举 → 视频列表 → `douyin_video.py --ids <id>...` 批量 ASR（有旁白教学视频直接 whisper；0 字图卡视频走抽帧 OCR，见上节两分支判定）；
2. 读转写全文，人工甄别：**知识密集的长视频**（>2000 字讲解）按主题合并提炼成知识卡（`source_type: douyin`，note 标注「视频转写提炼」，ASR 错别字需人工校正：居身→具身、派零点五→π0.5、访真→仿真 等）；短贴/生活内容/无转写的不入库；
3. 科普知识卡不挂「出现记录」（不是面经），来源节保留视频 URL 与日期。

先例：b11 博主 28 作品 → 25 条有效转写 → 19 条知识作品 → HTML 汇总文档（`D:\工程\具身智能\`）+ 题库 embodied 模块 13 张卡。

## 每周例行（DSH 定时任务，周日 10:00）

配置在 `sources/douyin_watch.json`（博主清单，route=image/article/video_asr）：

1. 逐博主枚举作品，与已存 works 文件 diff 出新作品；
2. 新作品按 route 处理：图文→OCR，文字笔记→article 正文，视频→登录态+ASR；
3. 图文/文字走 `douyin_seed.py` 切题判重；**视频讲解型读转写人工甄别**（见上节）→ 处置（真新题写卡 / 经典八股挂出现记录 / 知识提炼 / HR 题不入库）；
4. `validate.py` → `gen_taxonomy.py` → `build.py` → CHANGELOG → push。

**注意**：未登录枚举可能只拿到部分作品（b4 主页标 30 实测未登录只给 18~26 条），登录态（`_cache/douyin_state.json`）能拿全量；登录态过期时用 `tools/douyin_login.py` 重新扫码。

## 合规边界

- 只读公开页面、低频、**不批量再分发原图**，图片不落仓库（`_cache/` 已在 `.gitignore`）；
- 题卡里只保留**题目文字 + 原作品链接 + 作者署名**，标注 `source_type: douyin`；
- 著作权属原作者，入库仅作个人复习使用；若要公开发布，建议只保留**题目本身**（事实性内容），
  不复制其原创排版、答案长文或图片；
- 抖音用户协议对自动化访问有限制，脚本按「低频访问、不点赞评论、不刷量」的低扰动方式实现；
- 登录态仅用于读取自己账号可见的公开内容，不做任何互动操作。

## 当前状态

- 四个脚本已就位并跑通（枚举 → OCR/正文 → 切题去重 → 登录）+ ASR（douyin_video.py，两分支判定）；
- `source_type: douyin` 已在 `tools/validate.py` 登记；
- 博主清单 `sources/douyin_watch.json`（b1~b10：嵌入式×3/Java 后端/嵌入式·文字笔记/就业指导×2/求职教学/营销号/STM32；b11 具身智能·纯视频）；
- 每周日 10:00 DSH 定时任务自动周检；视频讲解型博主走 ASR+人工甄别（见上节先例）。
