# mattpocock/skills 深度解析：把工程纪律封装成可组合的 Agent 技能

## 目录

- [1. 项目简介](#1-项目简介)
- [2. 设计哲学：组合压倒内容](#2-设计哲学组合压倒内容)
- [3. 核心模式深度解析](#3-核心模式深度解析)
  - [3.1 grilling：设计树与前沿轮次访谈](#31-grilling设计树与前沿轮次访谈)
  - [3.2 wayfinder：决策票地图与战争迷雾](#32-wayfinder决策票地图与战争迷雾)
  - [3.3 tdd：seam 治理下的红绿循环](#33-tddseam-治理下的红绿循环)
  - [3.4 diagnosing-bugs：回路即技能](#34-diagnosing-bugs回路即技能)
  - [3.5 writing-for-agents：自我指涉的元技能](#35-writing-for-agents自我指涉的元技能)
  - [3.6 codebase-design：深模块词汇底座](#36-codebase-design深模块词汇底座)
- [4. 技能架构分析：分层组合系统](#4-技能架构分析分层组合系统)
  - [4.1 用户调用与模型调用：原则化的切分](#41-用户调用与模型调用原则化的切分)
  - [4.2 CONTEXT.md：共享词汇层](#42-contextmd共享词汇层)
  - [4.3 进程闸门与完成标准：普遍语法](#43-进程闸门与完成标准普遍语法)
  - [4.4 sub-agent 派发：上下文经济观](#44-sub-agent-派发上下文经济观)
- [5. 元工程实践：把仓库当产品管理](#5-元工程实践把仓库当产品管理)
  - [5.1 双轨分发：插件订阅与可编辑复制](#51-双轨分发插件订阅与可编辑复制)
  - [5.2 仓库治理：CLAUDE.md、ADR 与版本管理](#52-仓库治理claudemdadr-与版本管理)
- [6. 与 awesome-skills 的对比](#6-与-awesome-skills-的对比)
- [7. 可借鉴的结论](#7-可借鉴的结论)
- [8. 快速开始：5 分钟上手](#8-快速开始5-分钟上手)

---

## 1. 项目简介

[mattpocock/skills](https://github.com/mattpocock/skills) 是知名 TypeScript 教育家、Total TypeScript 创始人 Matt Pocock 的个人 Agent 技能库，2026 年开源后迅速成为 GitHub 上关注度最高的技能集合之一（22 万 + stars）。仓库副标题为 "Skills for Real Engineers. Straight from my `.agents` directory." —— 它直接来自作者的日常开发环境，是作者真实使用的技能，而非演示性质的教学样本。

> **读者指南**：本文第 1-5 章讲设计（所有人可读），第 6 章是与本仓库的对比（作者视角，普通用户可跳过），第 7 章给出可操作的借鉴结论（每条配落地第一步），第 8 章是 5 分钟快速开始。想直接上手的读者可以从第 8 章开始。

项目收录 35 个 `SKILL.md`，按用途分为五个桶（bucket）：

| 目录            | 定位                                 |
| --------------- | ------------------------------------ |
| `engineering/`  | 日常代码工作（18 个，推荐发布）      |
| `productivity/` | 非代码类工作流工具（7 个，推荐发布） |
| `misc/`         | 保留但不推广（4 个）                 |
| `in-progress/`  | 公开的 beta 技能，收集反馈（6 个）   |
| `deprecated/`   | 已废弃                               |

仓库的核心理念在 README 中直言不讳：

> Developing real applications is hard. Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve. These skills are designed to be small, easy to adapt, and composable. They work with any model. They're based on decades of engineering experience.

与市面上"拥有流程"的框架（GSD、BMAD、Spec-Kit——均为试图接管整个开发流程的方法论体系，如 GSD 是 GitHub 的 spec 驱动工作流）不同，该仓库把技能设计为**小、可适配、可组合**的纪律单元：作者明确鼓励用户 "Hack around with them. Make them your own."。针对的四个真实失败模式：**对齐失败**（agent 没做用户想做的事）、**过度冗长**（agent 用 20 个词说 1 个词能说的话）、**代码不工作**（缺乏反馈回路）、**代码库变成大泥球**（软件熵加速）。

---

## 2. 设计哲学：组合压倒内容

如果只用一个词概括这个仓库，"组合"（composition）是最恰当的。与绝大多数"一个技能 = 一份完整手册"的仓库不同，这里的技能形成一座金字塔：

- **底层**：模型可调用的**原语技能**（primitives）——`grilling`（访谈）、`domain-modeling`（领域建模）、`codebase-design`（深模块设计）、`tdd`（测试驱动开发）、`research`（研究）、`prototype`（原型）、`code-review`（评审）、`diagnosing-bugs`（诊断）。它们承载全部方法论，任何时候都可以被触发。
- **上层**：用户主动调用的**薄路由技能**（routers）——`grill-with-docs`、`grill-me`、`wait-what`、`handoff`、`implement` 等（SKILL.md 仅 7-16 行）。路由技能的正文经常只有一句话，例如 `grill-with-docs` 的完整 SKILL.md：

```markdown
---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Call the Skill tool twice, for "grilling" and "domain-modeling".
```

`grilling` 是复用度最高的原语：`grill-me`、`grill-with-docs`、`triage`、`wayfinder`、`improve-codebase-architecture` 五个技能都在驱动它。`ask-matt` 则是整个组合系统的显式地图——一个"技能路由"技能，负责回答"现在这种情况该用哪个技能"。

这种架构的收益：方法论只写一遍，出现在一个地方（原语），修 bug 是一处编辑；路由技能几乎不消耗上下文，只在用户真正需要时把原语拉进来。代价是组合依赖字符串约定（"Call the Skill tool with X"），用户经 skills.sh 只安装子集时，路由技能的调用会静默失效——这是该组合架构的一个固有风险。仓库未内置探测机制（唯一做安装探测的是 `setup-matt-pocock-skills`），新用户需要注意。

`ask-matt` 不只是技能地图，它编码了整个仓库的组合骨架：**"idea → ship" 主流程**——`grill-with-docs`（对齐）→ `to-spec`（综合成规范）→ `to-tickets`（拆成票）→ `implement`（按票实现，内部驱动 tdd，收尾 code-review），两条 on-ramp（`triage` 分诊、`diagnosing-bugs` 诊断），以及 `prototype` 经 `handoff` 的绕行桥。

---

## 3. 核心模式深度解析

### 3.1 grilling：设计树与前沿轮次访谈

`grilling` 是仓库最受欢迎的模式（README 自述 `grill-me` / `grill-with-docs` 为 "These are my most popular skills"），也是对齐失败（failure mode #1）的解法。它把"让 agent 向用户提问"这件事从随意的对话改造成有结构的纪律：

**设计树（design tree）**：每一次决策都会分支成挂在它下面的子决策。访谈的目标是遍历整棵树，直到每个分支都被访问过、没有留下任何静默假设。

**前沿轮次（frontier rounds）**：把"所有前提已经满足、现在就能问的问题"（前沿，frontier）作为一整轮一次性抛出。每个问题编号，并**附上模型的推荐答案**，然后停下来等用户回答，再计算下一轮前沿。这种批处理是注意力经济学的精巧设计——一次等待换来一整片问题的答案，而不是一问一答的低效往返。

**职责切分**：_"Finding facts is your job, never the user's."_（找事实是 agent 的活，永远不是用户的活）。前沿问题需要查文件、查环境时，派 sub-agent 去找，不阻塞其余问题；但**决策永远是用户的**——每个决策都交给用户拍板。

**终止条件**：前沿为空——设计树的每个分支都已访问，没有剩余静默假设。在用户确认达成共识之前，不得开始行动。

一次 `grilling` 对话长这样（问题编号 + 推荐答案，一轮抛出一整片前沿）：

```
❓ **Q1** - **目标范围**：这个改动要覆盖哪些功能，明确排除哪些？

➡️ 建议先只做核心流程，边缘场景留到第二期

❓ **Q2** - **数据模型**：现有 schema 需要迁移吗？

➡️ 建议不需要，增量加字段即可
```

（注：grill-with-docs 的描述中提到的 ADR 即 Architecture Decision Record，架构决策记录——记录"为什么这么设计"的短文档，防止无上下文的未来维护者误改。）

### 3.2 wayfinder：决策票地图与战争迷雾

`wayfinder` 是对"一个 agent 会话装不下的大型工作"最严肃的结构化回答之一。核心洞见：**多会话的规划必须是一个共享物，而不是会话内的状态**。

- **目的地（destination）**：地图的锚点。命名目的地是绘图的第一个动作，它决定每个票的形状——可能是一份待移交的 spec、一个待锁定的决策、或一个原地变更。
- **决策票 vs 执行票**：地图上的票是**决策票**——解决的是一个决策，不是一段待执行的构建。`wayfinder` 默认是规划模式（plan, don't do）：地图完成的标准是"路已清晰、没有待决事项"，而不是交付物。
- **战争迷雾（fog of war）**：地图刻意不完整。能看清但还无法精确定义的决策存在于"迷雾"中，记在地图的 **Not yet specified** 区。判据是"你现在能否精确陈述这个问题"，而不是"你现在能否回答它"。迷雾只向目的地聚集；明确排除在外的范围进入 **Out of scope** 区，永不毕业。
- **原生阻塞依赖**：票之间的依赖用 tracker 的原生 blocking 关系表达，让前沿（frontier）直接可视化在 tracker 的 UI 上——人类不需要打开地图就能看到当前可取的票。
- **claim-by-assignment**：一个会话**先把自己分配为票的 assignee 再干活**，这样并发的其他会话会跳过已认领的票——并发会话协作成为一等公民。
- **硬规则**：_"Never resolve more than one ticket per session"_（一次会话最多解决一张票，research 票除外）。每张票被约束为一个 100K token 会话能装下的大小。
- **四种票型**：Research（AFK——agent 独自查资料）、Prototype（HITL——做出粗糙实物供讨论）、Grilling（HITL——访谈，默认型）、Task（HITL 或 AFK——必须先完成的体力活，如注册服务、迁移数据）。HITL 即 human-in-the-loop（人机协同），AFK 即 away-from-keyboard（agent 独立完成）。票型决定一张票由谁解决、以什么方式解决。

### 3.3 tdd：seam 治理下的红绿循环

`tdd` 把"红→绿循环"重构为 **seam 治理**。它的目标不是教 agent 跑 TDD，而是让循环"产出值得留的测试"：

- **测试只写在预同意的 seam 上**：seam（接缝）指"不深入内部就能观察行为"的公共边界——测试在此进行，而不是对着内部实现。写任何测试之前，先写下要测试的 seam 并征得用户确认——_"No test is written at an unconfirmed seam."_。你不可能测试一切，预先同意 seam 是让测试投入落在关键路径和复杂逻辑上，而不是每个边角。
- **三个反模式**，每个带判定信号：
  - **Implementation-coupled**（实现耦合）：mock 内部协作者、测私有方法、或通过旁路验证（查数据库而不是走接口）。判定信号：重构后行为未变但测试碎了。
  - **Tautological**（同义反复）：期望值用与代码相同的方式重算（`expect(add(a, b)).toBe(a + b)`）。期望值必须来自独立的事实源。
  - **Horizontal slicing**（水平切片）：先写完所有测试再写实现。批量测试验证的是*想象中*的行为——你测试了事物的形状而不是面向用户的行为。要用**垂直切片**：一个测试 → 一个实现 → 重复，每个测试都是回应上一轮反馈的**曳光弹**（tracer bullet）。
- **重构不属于循环**：重构被显式划给 `code-review` 阶段，防止红绿循环被稀释。
- **跨技能组合**：接口形状本身存疑时（模块该多深、seam 该在哪），调用 `codebase-design` 获取词汇——"a reference to consult, not a session to run"（是供查阅的参考，不是要跑一遍的会话）。

### 3.4 diagnosing-bugs：回路即技能

`diagnosing-bugs` 的宣言是：**"Phase 1: Build a feedback loop. This is the skill. Everything else is mechanical."**（构建反馈回路。这才是技能本身，其余全是机械动作）。

- **回路优先于假设**：_"No red-capable command, no Phase 2."_（没有能让测试变红（失败）的命令，就不许进入第二阶段）。发现自己在读代码构建理论之前还没有这个命令——立刻停下："直接跳到假设正是这个技能要防止的失败"。
- **10 种构造回路的手段**，按优先级排列：
  1. 失败测试（在能触达 bug 的 seam 上写测试）
  2. curl/HTTP 脚本（对着运行中的 dev server）
  3. CLI 调用 + 夹具输入，与已知正确的输出比对
  4. 无头浏览器脚本（Playwright/Puppeteer 驱动 UI 并断言）
  5. 重放捕获的 trace（把真实请求/事件日志存盘，隔离重放）
  6. 一次性 harness（最小化系统子集 + mock 依赖，单函数调用触发 bug 路径）
  7. 属性/fuzz 循环（"有时输出错误"类 bug 跑 1000 个随机输入）
  8. 二分 harness（bug 出现在两个已知状态之间时，自动化 `git bisect run`）
  9. 差分循环（同一输入跑旧版 vs 新版，diff 输出）
  10. **HITL bash 脚本**（最后手段——human-in-the-loop，人机协同：必须人类点击时，用模板驱动人类操作，输出回传 agent）
- **回路完成标准是可勾选清单**：Red-capable（能捕获这个具体 bug 的确切症状）/ Deterministic（确定性）/ Fast（秒级）/ Agent-runnable（agent 可无人值守运行）。
- **收紧回路**：把回路当产品对待——能更快吗？信号更尖锐吗？更确定吗？"30 秒的 flaky 回路比没有回路好不了多少；2 秒的确定性回路是调试超能力。"
- **非确定性 bug**：目标不是干净的复现而是**更高的复现率**——触发 100 次、并行化、加压力、注入 sleep。"50% 概率的 flaky bug 可以调试；1% 的不行。"
- **假设必须可证伪**，按固定格式陈述："If <X> is the cause, then <changing Y> will make the bug disappear." 无法陈述预测的假设是 vibe（感觉），丢弃或锐化。排序后的假设列表**先展示给用户**再测试——用户往往一句话就重排优先级。
- **脱敏纪律**：展示的一切先 REDACTED；调试日志带唯一前缀 `[DEBUG-a4f2]`，清理是一个 grep。
- **"没有正确的 seam 本身就是发现"**：如果找不到合适的回归测试 seam，那就是发现——代码库架构阻止了 bug 被锁死，显式标记并桥接到 `improve-codebase-architecture`。

### 3.5 writing-for-agents：自我指涉的元技能

`writing-for-agents` 是"**关于怎么写 agent 文档的文档**"——本仓库所有 SKILL.md 的质量来源，也是少数把技能写作理论化的公开案例。它的工具箱：

- **Context pointer（上下文指针）**：上下文中的引用，命名某些上下文外的材料并编码到达它的条件。技能 description 是一个指针，AGENTS.md 里的一行也是同一个对象。**指针的措辞，而不是目标，决定 agent 何时以及多可靠地到达材料**。"弱措辞的指针指向必达目标"是方差 bug（variance bug——同一输入在不同运行间输出不一致导致的不可靠）——先锐化措辞，锐化失败才内联材料。
- **两种载荷**：Context load（常驻材料的 token 成本）与 Cognitive load（人类的认知负担——人是索引）。指针逃掉 context load，代价是指针自己的一行；没有指针的材料完全骑在 cognitive load 上。
- **信息层级阶梯**：in-file step（主要层，agent 按顺序执行的动作）→ in-file reference（按需查阅的定义/规则）→ disclosed reference（推到独立文件、由指针到达）。渐进式披露是**走下阶梯**：分支是衡量披露的最干净测试——所有分支都需要的留在正文，只有部分分支到达的推给指针。
- **Leading words（引导词）**：模型预训练中已存在的紧凑概念（_tight_、_red_、_fog of war_、_tracer bullets_），以 token 而非句子重复，招募模型已有的先验来锚定行为。"fast, deterministic, low-overhead" → _tight_；"a loop you believe in" → _red_（一个模糊的闸门变成二值的可观察状态）。造新词要付定义 token，先找现成的词。
- **否定是失败模式**："别想大象"，大象就是全部——禁令把被禁行为拖进上下文，使它*更*可用。正面陈述目标行为；禁令只保留在无法正面表述的硬护栏上，且必须配正面目标。
- **完成标准（completion criteria）**：Clarity（agent 能否区分完成与未完成——模糊的界限邀请"过早完成"）与 Demand（要求多高——"every modified model accounted for" 强制彻底的工作）。
- **修剪纪律**：单一事实源（去重复）、环境是事实源（`package.json`、`--help` 是 lookup，重述它们的是缓存）、相关性检查（防 sediment——"添加感觉安全、删除感觉冒险"的默认命运）、**no-op 测试**（"这条指令相对默认行为改变行为吗？不改变就整句删除，而不是删词"）。

### 3.6 codebase-design：深模块词汇底座

`codebase-design` 是仓库的**共享词汇底座**，把 Ousterhout 的深模块哲学（"最好的模块是深的：大量功能通过小接口暴露"）封装成一组强制术语：module / interface / depth / seam / adapter / leverage / locality。它被 `tdd`、`improve-codebase-architecture` 引用。

写作上值得注意的手法：

- **强制术语表**："Use these terms exactly... Consistent language is the whole point." 并带 `_Avoid_` 列表。
- **原则以"测试"形式给出**：deletion test（复杂度守恒检验——想象删除这个模块：如果复杂度随之消失，它是过路模块 pass-through；如果复杂度分散到 N 个调用方重新出现，它是在发挥价值）、"one adapter = hypothetical seam, two = real"（一个适配器是假设的 seam，出现两个才是真的）。
- **Rejected framings 章节**：主动记录被否定的定义——防止模型回退到"行数比"这类通俗说法。
- **DESIGN-IT-TWICE.md**：**并行设计竞赛**模式——3 个及以上 sub-agent 各拿不同的偏置约束（最小接口 / 最大灵活 / 常见调用方优先 / 端口适配器）独立设计，然后按 depth / locality / seam 对比，给立场鲜明的推荐。这是 sub-agent 派发最有创意的用法之一。

---

## 4. 技能架构分析：分层组合系统

### 4.1 用户调用与模型调用：原则化的切分

每个技能都在两个调用模式中选一个：

- **User-invoked**（用户调用）：`disable-model-invocation: true`（OpenAI 生态对应 `policy.allow_implicit_invocation: false`），只有人类输入斜杠命令才能到达。它们的职责是**编排**——承载有状态的会话流程。
- **Model-invoked**（模型调用）：模型或用户都可以触发，持有可复用的纪律——agent 在任务匹配时自动拉取。

判据本身被自我文档化在 `writing-for-agents/SKILL-MECHANICS.md` 里：用户调用技能零上下文载荷但只能靠人触发；模型调用技能靠 description 的措辞承担触发分支。README 用一句话总结："User-invoked skills orchestrate; model-invoked skills hold the reusable discipline. A user-invoked skill may invoke model-invoked skills, but never another user-invoked one."（用户调用技能编排，模型调用技能持有可复用纪律。用户调用技能可以调用模型调用技能，但绝不调用另一个用户调用技能。）

### 4.2 CONTEXT.md：共享词汇层

`CONTEXT.md` 是项目共享语言的单一事实源——一个**纯词汇表**，严格遵循 "totally devoid of implementation details"（完全不含实现细节），不是 spec、不是草稿本。它定义领域术语（Issue tracker / Issue / Decision ticket / Triage role），每条带 `_Avoid_`（避免使用的词），还有 "Flagged ambiguities"（记录曾经产生歧义、现已解决的术语）。

多个工程技能（如 `tdd`、`diagnosing-bugs`）开篇就带同一条指令："read `CONTEXT.md` (if it exists)... respect ADRs in the area you're touching"（阅读 CONTEXT.md（若存在）……遵守你改动区域的 ADR）。词汇是跨技能组合的胶水：`tdd` 用 `codebase-design` 的 seam 词汇，`code-review` 的 Spec 轴（见 4.4）查 spec。`domain-modeling` 技能负责主动构建与打磨这个词汇表，配 ADR 三条件门（难反转 + 无上下文会惊讶 + 真权衡——满足三者才写 ADR）。

值得注意的是：**仓库在元层面实践自己的方法论**——它自己的 CONTEXT.md 就是这个词汇表系统的产物，`.out-of-scope/` 目录记录被拒绝的请求防止重复建议，ADR 记录"为什么发 Claude Code 插件而不是 Codex 插件"这种真实权衡。

### 4.3 进程闸门与完成标准：普遍语法

几乎所有技能都使用同一种语法：**显式进程闸门 + 可勾选完成标准**。

- "No red-capable command, no Phase 2."（diagnosing-bugs）
- "Never resolve more than one ticket per session."（wayfinder）
- "Do NOT interview the user."（to-spec——把已讨论的内容综合成 spec 时禁止再访谈）
- "No test is written at an unconfirmed seam."（tdd）
- "Always resolve; never --abort."（resolving-merge-conflicts——按意图解决冲突，追两侧的 primary source，绝不放弃合并）
- 完成标准写成勾选清单（diagnosing-bugs 的四个勾选项、wizard 的 "Done when…"）

这是 `writing-for-agents` 的 completion criteria 理论（Clarity + Demand）的直接产物——仓库在实践它讲授的理论。

### 4.4 sub-agent 派发：上下文经济观

sub-agent 派发是仓库的标准操作，对"什么该进 sub-agent 窗口"有清晰的经济观：

- **code-review**：双轴（Standards / Spec）并行 sub-agent，防止两个评审视角互相污染上下文——这是隔离要防的 reranking（重排）现象。
- **grilling**：前沿问题需要查事实时派 sub-agent，不阻塞其余问题。
- **research**：整个技能就是"把阅读腿活委托给后台代理，只信一手来源，产出带引用的 Markdown"。
- **wayfinder**：research 票并行派发 sub-agent 解决。
- **improve-codebase-architecture**：代码库探索派 sub-agent。
- **DESIGN-IT-TWICE**：并行设计竞赛。

上下文经济的另一半是**会话卫生规则**，定义在 `ask-matt/PHASE-BOUNDARIES.md`：五个选项的决策树（Continue / `/clear` / `/handoff` / sub-agent / `/compact`），按 primary vs secondary source 的损耗经济学排序——Continue 最先排除，`/clear` 最便宜，`/handoff` 只在换 harness、换目录、换人或中途分叉时用，`/compact` 垫底。配套的 **smart zone**（约 150k token）指模型仍能清晰推理的窗口：`ask-matt` 建议对齐到 `to-tickets` 保持一个不中断的窗口，超窗即做交接或压缩。

---

## 5. 元工程实践：把仓库当产品管理

### 5.1 双轨分发：插件订阅与可编辑复制

仓库提供两种安装路径，对应两种哲学：

- **Claude Code 插件**（`.claude-plugin/`）：`claude plugins install mattpocock-skills`，作为官方市场中的托管、只读、自动更新的捆绑包——**订阅而非 fork**。插件只发布 `engineering/` 和 `productivity/` 两个推广桶里的 25 个技能，misc / in-progress / deprecated 不出现。
- **skills.sh**（`npx skills add mattpocock/skills`）：把技能文件**复制**进项目成为普通文件，用户拥有并可以编辑——"Nothing updates behind your back"。适用于 Codex 等所有 Agent-Skills 标准 harness。

配套的安装引导：`/setup-matt-pocock-skills` 在每个仓库跑一次，询问 issue tracker 选择（GitHub / Linear / 本地文件）、triage 标签约定、文档保存位置。工程技能通过 setup 生成的 issue-tracker 配置文件（`issue-tracker-github.md` / `issue-tracker-gitlab.md` / `issue-tracker-local.md`，每个 tracker 一种）获得 tracker 抽象，统一的措辞是"应该已提供给你，否则让用户跑 /setup-matt-pocock-skills"。

**两条路径怎么选**：想零维护、跟随作者更新，选插件订阅；想改造成自己的技能、或使用 Codex 等非 Claude 的 harness，选 skills.sh 复制。注意 README 的警告：**不要两条都装**——"installing both leaves you with every skill twice"（两条都装会得到每个技能的两份）。

### 5.2 仓库治理：CLAUDE.md、ADR 与版本管理

仓库的治理密度在同类项目中罕见：

- **CLAUDE.md / AGENTS.md** 是给 AI 维护者的完整操作手册：bucket 约定、plugin.json 同步规则、docs 镜像页同步规则、`ask-matt` 路由图必须保持准确（"a router that lies" 是明确的失败模式）、`scripts/link-skills.sh` symlink 分发。
- **ADR**（`.agents/adr/`）：记录真实架构决策——`0002-ship-as-a-claude-code-plugin.md` 详细分析为何发 Claude Code 插件而非 Codex 插件（Codex manifest 只接受单一路径、symlink 安装即断），以及"为什么 setup 指针只放在硬依赖技能里"（软依赖技能保持 token 精简，避免 cargo-cult）。
- **版本发布**：`.changeset/` 管理每个技能微调（连"grilling 问题间加分隔线"都有 changeset），`sync-plugin-version.mjs` 同步 plugin 与 package 版本。
- **文档镜像**：每个推荐技能在 `docs/<bucket>/<skill>.md` 有人类可读的文档页，统一四段结构：What it does / When to reach for it / Common questions / It's working if。
- **文风规则**：全仓库禁止 em-dash（破折号）——用逗号、冒号、括号或连词改写。

## 6. 与 awesome-skills 的对比

| 维度     | awesome-skills（本仓库）                           | mattpocock/skills                                                                   |
| -------- | -------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 技能形态 | 大而全的独立 SKILL 包（30-224 行，自成体系）       | 小而组合：底层原语 + 薄路由（7-140 行，方法论只写一遍）                             |
| 组合机制 | 技能之间基本独立，靠 description 触发              | 路由技能显式调用原语（"Call the Skill tool twice"），`ask-matt` 是显式地图          |
| 共享词汇 | 无仓库级词汇文件；双语约定（中英分层）是主要规范   | CONTEXT.md 领域词汇单一事实源 + ADR，几乎所有技能都读                               |
| 调用切分 | 未区分用户/模型调用                                | `disable-model-invocation` 原则化切分，判据自我文档化                               |
| 测试体系 | unit-test/ 测试金字塔（静态 + 端到端 JSONL 断言）  | 几乎没有测试体系（被本仓库深扫确认的弱点）                                          |
| 分发     | `sync.sh` 复制到本地三个 harness                   | Claude Code 官方插件市场 + skills.sh 双轨，changeset 版本管理                       |
| 深度解析 | 三篇深度解析文章（gstack / google / superpowers）  | 无（以实战技能为主）                                                                |
| 独特资产 | 双语文档体系、测试金字塔、四类评审（doc-reviewer） | grilling 设计树、wayfinder 决策票地图、writing-for-agents、diagnosing-bugs 回路纪律 |

重叠区域：本仓库的 `openspec-assistant`（规范驱动开发）与其 `to-spec → to-tickets → implement → tdd → code-review` 流水线同属 SDD 阵营，但思路互补——我们的重在角色协同（架构师 / 开发 / QA）与 `/opsx` 指令体系，他们的重在纪律化的小步流水线。本仓库的 `doc-reviewer` 四类评审与其 `code-review` 双轴（Standards + Spec）也可互相参照。

## 7. 可借鉴的结论

每条结论附**落地第一步**——下一条读完就可以动手，具体机制回看对应小节。

1. **组合式技能架构值得试验**（详见 §2）：把方法论收敛到少数原语（grilling、domain-modeling、codebase-design），用户入口做成薄路由，可以让修复和演进成为一处编辑。代价是需要 `ask-matt` 这类路由地图防止"技能太多找不到"。
   - **第一步**：挑一个你现有的厚技能，把其中一个可复用流程（如"先提问再动手"）抽成独立原语，主技能改成一句路由调用它——先做这一个实验，不必全量重构。
2. **CONTEXT.md 词汇层是最被低估的设计**（详见 §4.2）：多个技能读同一个词汇文件，让术语、变量、文件名保持一致，agent 导航成本与 token 消耗同时下降。`grill-with-docs` 把"对齐访谈"和"词汇沉淀"绑定，一次会话同时产出共享语言与 ADR——"it might be the single coolest technique in this repo"。
   - **第一步**：为你当前项目写一个 20 行的词汇表（10 个领域术语 + 每个的 `_Avoid_` 避免用词），放到 `CONTEXT.md`，然后在技能里加一行"读 CONTEXT.md 再动手"。
3. **进程闸门比冗长指令更可靠**（详见 §4.3）："No red-capable command, no Phase 2" 这类显式闸门把纪律变成硬约束，配合可勾选完成标准，远比"请务必先建立反馈回路"有效。这是 completion criteria 的 Clarity 原则的直接应用。
   - **第一步**：打开你一个 SKILL.md，找到最含糊的"请务必/确保"指令，改写成"没有 X 就不许进入下一步"的闸门 + 一句完成标准。
4. **写技能时要意识到"否定是失败模式"**（详见 §3.5）：正面陈述目标行为；禁令只在无法正面表述时使用且必须配正面目标。这一条可以直接改进我们所有 SKILL.md 的编写。
   - **第一步**：grep 你的技能目录里的"不要/禁止/切勿"，逐条改写为正面表述。示例——原："不要修改用户提供的标题"，改："用户提供的标题作为主标题原样保留，提炼与概括放副标题"。这条示例正来自本仓库 `editorial-card-designer` 的现有规则。
5. **元工程自举**（详见 §4.2、§5.2）：用自己教的纪律管理自己的仓库（CONTEXT.md 管自己的词汇、ADR 记录自己的架构决策、`.out-of-scope/` 防重复建议）——这让仓库的每一项方法论都经过了真实使用的检验。
   - **第一步**：为自己仓库写一个 `CONTEXT.md`（哪怕 5 个术语），并在下一次做出难反转的决策时写一条 ADR——先做这两件事，其余机制随用随加。
6. **组合架构的代价要提前买单**（详见 §2）：过于依赖作者个人约定（CONTEXT.md / triage 标签 / smart zone 约 150k token 的推理清晰度窗口假设）会提高新用户认知负担；跨技能组合无 fallback，安装子集时路由静默失效。
   - **第一步**：若你只想要其中 2-3 个技能，用 skills.sh 选择安装，并手动核对所选技能的跨技能调用是否齐全（见 §5.1）。
7. **技能质量需要测试保证**：该仓库几乎没有测试体系，是其最大短板——这反向确认了"技能质量需要测试保证"的判断，也正是我们 unit-test 金字塔（静态 + 端到端 JSONL 断言）的价值所在。
   - **第一步**：无需外部动作——它是对我们现有测试投入的背书，继续按 `unit-test/` 体系为新技能补测试即可。

## 8. 快速开始：5 分钟上手

想直接体验这个仓库，不需要先读完上文：

1. **装插件**（Claude Code 用户，30 秒）：
   ```bash
   claude plugins install mattpocock-skills
   ```
   或想拥有可编辑副本（适用于 Codex 等任意 harness）：
   ```bash
   npx skills add mattpocock/skills
   ```
   **两条路径二选一，不要都装**（会得到每个技能的两份）。
2. **跑一次安装引导**（每个仓库一次）：`/setup-matt-pocock-skills`——回答 issue tracker、triage 标签、文档目录三个问题。只用 productivity 技能可跳过。
3. **5 分钟实验**：对你手头一个模糊的想法（新功能、重构、一篇文章）跑 `/grill-me`——体会"设计树前沿轮次"的对齐访谈（§3.1）。这是作者的招牌技能。
4. **推荐试用的技能**，按场景：
   - 团队写代码：`/grill-with-docs`（对齐 + 词汇沉淀）、`/tdd`（seam 治理）
   - 大型工作规划：`/wayfinder`（决策票地图，§3.2）
   - 修难缠的 bug：`/diagnosing-bugs`（回路纪律，§3.4）
   - 想看懂它的技能怎么写：读 `skills/productivity/writing-for-agents/SKILL.md`——本仓库全部技能的质量来源（§3.5）
5. **还拿不准用哪个**：直接问 `/ask-matt`，它会按主流程给你路由（§2）。
