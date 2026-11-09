# 题卡字段规范

一道题 = 一个 Markdown 文件。文件是唯一内容源，网页由脚本从这些文件生成，**不要在网页端直接改内容**。

## 一、文件命名

```
content/<模块号_模块名>/<ID>-<英文短标题>.md
例：content/01_project/Q-0101-yolo-ros2-deploy-pipeline.md
```

- ID 全局唯一，前缀 `Q-`，四位数字。
- **号段按模块划分，每段 500 个**（早期用 100 间距导致 C++ 编号越界撞进 Linux 段，已改）：

| 模块 | 号段 | | 模块 | 号段 |
|---|---|---|---|---|
| `01_project` | 0101–0599 | | `06_ros2` | 2601–3099 |
| `02_cpp` | 0601–1099 | | `07_imaging` | 3101–3599 |
| `03_linux` | 1101–1599 | | `08_robot` | 3601–4099 |
| `04_algo` | 1601–2099 | | `09_hardware` | 4101–4599 |
| `05_deploy` | 2101–2599 | | `10_cv_pytorch` | 4601–5099 |

`python tools/validate.py` 会自动检查编号是否越界或重复。
- 英文短标题只用小写字母、数字、连字符，不超过 6 个词。

## 二、frontmatter 字段

```yaml
---
id: Q-0101
title: 你的 YOLO 模型是怎么部署到 ROS2 上的？
module: 01_project
sub: YOLO部署
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署, 感知]
companies: [华为车BU, 亿嘉和]
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html
verified_at: 2026-11-09
tags: [YOLO, ONNX, ROS2, TensorRT, 部署]
---
```

| 字段 | 取值 | 说明 |
|---|---|---|
| `id` | `Q-0101` | 全局唯一，勿改，网页锚点依赖它 |
| `title` | 面试官会怎么问 | **用第二人称"你"**，是问句，不是知识点标题 |
| `module` | `01_project` … `10_cv_pytorch` | 见 README 模块表 |
| `sub` | 短中文 | 细分方向，用于二级筛选 |
| `priority` | `P0` / `P1` / `P2` | 依据 `实习/华为与亿嘉和_双目标专攻方案.pdf` 的能力优先级 |
| `difficulty` | `1` / `2` / `3` | 1=能直接答 / 2=要组织语言 / 3=要能画图推导 |
| `roles` | 岗位标签数组 | `AI算法` `端侧部署` `感知` `图像算法` `定位导航` `感知规控` `嵌入式` `机器人软件` |
| `companies` | 公司/部门数组 | **通用八股留空**。只有确实只对口某类公司时才填（如影像题填联影/迈瑞）。公司×岗位的归属关系统一在 `companies/README.md` 维护，避免两处不一致 |
| `qtype` | `project` `principle` `coding` `design` `followup` | 题型 |
| `status` | 见下 | **决定网页是否折叠显示"待补充"** |
| `source_type` | 见下 | 可信度标记，不许含糊 |
| `source_ref` | 本地相对路径或 URL | 必须有，能溯源到原文 |
| `verified_at` | `YYYY-MM-DD` | 最近一次技术核验日期 |
| `tags` | 关键词数组 | 搜索用，3–6 个 |
| `hint` | 一句话 | **选填**。索引阶段还没写答案时，用一句套路提示代替空白，比留「待补充」有用 |
| `appearances` | 字符串数组 | **选填**。这道题在哪些公司的哪些岗位出现过，格式 `公司·岗位`，如 `["Momenta·C++ SDK"]`。只给网页筛选和统计用；详细信息写在正文「出现记录」表 |

### appearances 的填写纪律

只有**真实面经**才能填。一个来源都没有就留空，不要因为"这题看起来像这家会问"就填进去——那是预测，不是出现记录。

正文的「出现记录」表才是完整信息，`appearances` 只是它的索引：

```markdown
## 出现记录

| 日期 | 公司 | 岗位 | 轮次 | 来源 | 可信度 |
|---|---|---|---|---|---|
| 2028-03 | Momenta | C++ SDK 实习 | 一面 | 本人面试 | 已核实 |
| 2027-11 | 华为 | 软件开发 | 机考 | 牛客帖 · 链接 | 社区经验 |
```

- **同一家公司不同部门、不同年份考法可能完全不同**，不要用一条记录推出"这家都这么考"。
- 可信度三档：`已核实` / `社区经验` / `预测题`。没有可信度的记录不如不记。
- 面试后**当天**记，隔一天就记不清追问细节了。

### status

| 值 | 含义 |
|---|---|
| `indexed` | 只有题目，答案空着。**第一版允许大量存在** |
| `draft` | 答案在写，不完整 |
| `answered` | 口述答案+追问齐全，可直接用 |
| `verified` | 已对照官方文档/实测核验过技术准确性 |

### source_type

| 值 | 含义 |
|---|---|
| `self_doc` | 出自你自己的教学文档/项目文档，可信度最高 |
| `self_exp` | 出自你自己的项目实践，未成文 |
| `upstream` | 来自开源题库（必须在 `sources/upstream.md` 登记） |
| `official` | 官方文档 |
| `inferred` | 按 JD 推导的预测题，**不是真实面经** |

## 三、正文结构（口述稿体）

固定六节，顺序不变。空着的节保留标题并写 `待补充`，方便后续定位。

**可选追加 `## 出现记录`** 放在最后（「来源」之后），记录这道题真实出现在哪些面试里。格式见上节。

代码题（`qtype: coding`）在最前面多一节 `## 题目`；如果题目需要交代场景和约束，把它写详细——**题述写得越具体，复习时越省时间**：

```markdown
## 题目

**场景**：你在给感知模块写一个对外 SDK，下游有三个团队在用。

**约束**：不能暴露内部数据结构；要支持热更新；跨编译器版本。

**问**：动态库接口层你会怎么设计？

- **A.** ...
```

「读程序写结果」这类题则直接放代码块：

```markdown
## 题目

​```cpp
cout << -7 / 2 << " " << -7 % 3;
​```

- **A.** -3 -1
- **B.** -4 2
```

其余六节照旧。`python tools/validate.py` 对带 `lab_src` 标记的代码片段题强制检查这一节。

```markdown
## 口述答案

> 面试时真说出口的话。200–320 字，口语，别写论文。
> 结构固定：先给结论 → 再说为什么 → 最后落到"我做过"。

## 讲深一层

追问来了往下说。这里才写原理、公式、数据结构、参数。
比上面深一档，允许术语和细节。

## 高频追问

1. **追问问题** —— 一句话答法（30 秒内说完）
2. ...

## 易错点

- ❌ 常见错答 —— 为什么会被扣分
- ✅ 换成这么说

## 关联项目

指向你自己的项目/文档，这是和背题库的人拉开差距的地方。
没有就写「无」，不要硬凑。

## 来源

本地文档路径 / 官方文档链接 / 开源仓库（含许可证）
```

## 四、示例（可直接当模板用）

存为 `content/01_project/Q-0101-yolo-ros2-deploy-pipeline.md`：

```markdown
---
id: Q-0101
title: 你的 YOLO 模型是怎么部署到 ROS2 上的？
module: 01_project
sub: YOLO部署
priority: P0
difficulty: 2
roles: [AI算法, 端侧部署, 感知]
companies: [华为车BU, 亿嘉和]
qtype: project
status: answered
source_type: self_doc
source_ref: 方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html
verified_at: 2026-11-09
tags: [YOLO, ONNX, ROS2, TensorRT, 部署]
---

## 口述答案

> 我的链路是四段：PyTorch 训练导出 ONNX，ONNX 用 TensorRT 生成 engine，
> C++ 推理节点读 engine 出检测框，最后包成 ROS2 节点发自定义 msg。
> 中间最容易出问题的是 ONNX 导出这一步——动态 shape 没设对，
> TensorRT 建 engine 时会直接失败或者性能掉一半。
> 我在部署实施记录里专门记过这个坑：导出时要把 batch 和 h/w 都写成动态维度，
> 建 engine 时再给一组 optimization profile，不然它按固定尺寸优化，
> 换个分辨率就要重建。实测下来 FP16 比 FP32 快 1.7 倍左右，不是理论的两倍。

## 讲深一层

| 环节 | 工具 | 坑 |
|---|---|---|
| 导出 | `torch.onnx.export` | opset 版本、动态维度、后处理算子是否落到图里 |
| 优化 | `trtexec` / TensorRT API | optimization profile 的 min/opt/max |
| 推理 | C++ Runtime | 显存复用、stream 同步 |
| 集成 | ROS2 节点 | QoS 要设成 SensorDataQoS，否则丢帧 |

## 高频追问

1. **为什么不用 ONNX Runtime 直接推？** —— 能用，但 TensorRT 在这块卡上有 FP16/Tensor Core，延迟更低；ORT 胜在跨平台和易调试。
2. **INT8 量化怎么做的？** —— 需要校准集做 KL 散度或 entropy 校准，精度掉了要逐层看敏感度。
3. **推理结果不对怎么定位？** —— 先比对 PyTorch 与 ONNX 的中间层输出，定位到第一个发散的算子。

## 易错点

- ❌ "TensorRT 就是把模型变快" —— 太笼统，会被追问到答不出
- ✅ 说清是"算子融合 + 精度降低 + 针对本卡 kernel 自动调优"三件事

## 关联项目

- `方向与规划/项目/YOLO_Road_Detection/YOLO_部署实施记录.html`
- `方向与规划/项目/YOLO_Road_Detection/YOLO_模型部署教学文档.html`

## 来源

本人项目文档 + TensorRT 官方文档
```
