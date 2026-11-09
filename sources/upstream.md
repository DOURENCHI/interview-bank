# 开源复用台账

数据实测于 2026-11-09，来源 GitHub REST API `/repos/{owner}/{repo}`。**star 数和最后推送时间会变，引用前重新核。**

## 一、可安全复用（许可证明确、内容可用）

| 仓库 | ★ | 最后推送 | 许可证 | 复用方式 |
|---|---|---|---|---|
| `WinstonJQ/embodied-interview-qa` | 325 | 2026-10-19 | **MIT** | 唯一"活跃 + MIT + 内容厚"的仓库（3.9MB）。具身智能/RL/机器人控制/系统设计可整段借鉴结构，题目可摘录改写 |
| `pallavi-shekhar/ai-engineering-interview-questions-company-wise` | 2038 | 2026-11-09 | **Apache-2.0** | 借"按公司 + 轮次"的组织方式；题目可摘录 |

Apache-2.0 复用要求：保留版权声明与 NOTICE（如有）、标注修改。

## 二、只能用索引，不能抄正文

| 仓库 | ★ | 最后推送 | 许可证 | 限制 |
|---|---|---|---|---|
| `huihut/interview` | 38293 | 2026-09-17 | **CC BY-NC-SA 4.0** | 非商业 + 相同方式共享，**会传染**。只存题目标题 + 原链接 + 自己写的答案 |

CC BY-NC-SA 的实际影响：若直接摘录正文，整个题库需以同协议开放且不得商用。将来若把题库作为求职作品集展示、或接私活复用，会构成违约。**规避成本很低：只抄题目、不抄答案。**

## 三、不建议复用（实测不达预期）

| 仓库 | ★ | 最后推送 | 问题 |
|---|---|---|---|
| `SoulVen/interview-linux-cpp` | **0** | 2021-03-31 | 0 star 0 fork，5 年未更新。此前被推荐为"优先复用"，实测名不副实 |
| `ShanghaiTechAIClub/DLInterview` | 1112 | **2018-05-03** | 停更 8 年，仅 35KB。深度学习部分已明显过时（无 Transformer/VLA 相关） |
| `zouxiaobo/interview_back_end` | 276 | 2019-10-08 | 停更 7 年 |
| `JuWaiRen147/Awesome-CPP-Autonomous-Driving` | 21 | 2025-12-02 | fork(22) > star(21)，无 LICENSE |
| `autodriving-heart/Awesome-interview-questions-on-Autonomous-Driving` | 22 | 2024-04-13 | 无 LICENSE，社区问答性质，非面试原题 |
| `Yicen-y/Autonomous-Driving-Cpp` | 4 | 2025-12-08 | LICENSE 署名 `0voice`，本身系转抄，来源链不清 |

## 四、许可证速查

| 协议 | 能否抄正文进私有库 | 能否公开 | 备注 |
|---|---|---|---|
| MIT | ✅ | ✅ 需保留版权声明 | 最宽松 |
| Apache-2.0 | ✅ | ✅ 需保留声明 + 标注修改 | 含专利授权 |
| CC BY-NC-SA 4.0 | ⚠️ 仅个人学习 | ❌ 公开即传染为同协议且禁商用 | 只抄题目最稳 |
| 无 LICENSE | ❌ | ❌ | 默认保留所有权利，法律上不能复制 |

## 五、结论

真正值得复用的只有 2 个仓库（MIT + Apache），其余靠自己的文档产出。题库约 **85% 的题目应来自本地教学/项目文档**，开源部分只补齐通用八股（C++/Linux/算法）的表述方式。
