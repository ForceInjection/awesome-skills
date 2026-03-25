# Skill 测试：从“凭感觉”到“有证据”的质量体系

本文说明如何在仓库内以最小依赖完成 Skill 的“静态单元测试”与“端到端评估”。结合系统化的测试原则，我们的目标是以确定性信号（行为与产物）构建可复现、可比较、可在 CI 守门的质量闭环，兼容任意 CLI 型开源 Code Agent（如 `OpenCode`），使团队从“凭感觉的手动验证”走向“结构化、可复现、可对比”的工程化治理。

---

## 1 背景与目标

Skill 创作门槛低、数量爆发，但高质量（稳定、可复用、可维护） Skill 的生产仍缺乏系统方法。常见问题包括：触发不稳定（漏触/误触）、步骤偏离、环境污染（如翻译结果污染代码库）、风格约定无法保证。
当缺乏度量时，改动难以判断是改进还是回归。因此，我们遵循软件工程的 TDD 原则，为 Skill 建立测试闭环：“只评结果、不评路径”。

我们通过以下两个层面生成可复现的度量信号：

- **静态层（无大模型依赖）**：校验文档资产与约束（链接格式、图片相对路径、命名规范、敏感信息脱敏），作为 CI 必过项。
- **行为层（端到端沙盒）**：让 Agent 实际执行 Skill，记录 JSONL 事件流并断言工具、顺序与关键产物。

评估时主要关注以下**成功维度**：

1. **结果**：产出是否可用（报告是否生成、格式是否保留）。
2. **过程**：是否遵循预期步骤（如：先拷贝文件到沙盒，再修改，防止主干污染）。
3. **效率与消耗**：Token 消耗是否在合理范围，有无不必要的“折腾”（通过解析 `usage.md` 对比）。

---

## 2 目录与文件定位

测试框架通过目录约定实现多技能的隔离与调度，核心由统一的主控脚本、各技能独立的配置沙盒以及静态规则集组成。

- 代码参考
  - 主控脚本与入口：`./unit-test/opencode-skill-eval.sh`
  - 端到端执行器：`./unit-test/evals/agent/run.sh`
  - 通用行为断言器：`./unit-test/evals/agent/checks.js`
  - 用量与成本解析器：`./unit-test/evals/agent/parse-usage.js`
  - 技能配置与隔离环境：`./unit-test/skills/<skill>/config.sh`
  - 静态单测实现与入口：
    - 分发调度器：`./unit-test/tests/run_static.py`
    - 规则检查模块：`./unit-test/tests/<skill>/checks.py`
  - 示例夹具（测试输入样本）：`./unit-test/fixtures/<skill>/input.md`

---

## 3 静态单元测试（文档资产与约束）

静态测试不依赖 Agent 与大模型的推理，通过 Python 脚本前置拦截格式错误、死链接与敏感信息，从而阻断低级错误流入端到端环节，有效降低评估成本与噪音。

- 适用范围
  - 链接格式（仅允许 `http://` 或 `https://`，锚点 `#` 例外）
  - 图片相对路径（禁止绝对与 `http(s)` 外链）
  - 文件命名（小写 + 中划线，不含空格与下划线）
  - 敏感信息（API Key/Secret 等）脱敏
- 运行示例

```bash
# 说明：运行静态单测，自动按 SKILL 分发，输出结构化 JSON（overall_pass/score/逐项布尔）
python3 ./unit-test/tests/run_static.py doc-reviewer
```

- 结果解读
  - `overall_pass`：所有检查通过为 true
  - `score`：通过项比例（0–1）
  - 逐项布尔：快速定位失败原因（如命名不合规）

---

## 4 端到端评估（`OpenCode` 等 CLI Agent）

端到端评估将 Agent 视为黑盒，通过捕获其 CLI 运行时的标准输出（JSONL 事件流）来重构行为轨迹，进而对工具调用顺序、Token 消耗及最终生成产物执行严格的代码级断言。

### 4.1 环境准备

评估框架依赖全局环境变量来注入必要的 API 凭证与基础的 Agent 启动指令。

```bash
# 说明：如果 Agent 需要 LLM 提供方，按需设置，例如：
export OPENAI_API_KEY=your-key

# 说明：设置 CLI Agent 命令为环境变量，并开启 JSON 事件输出
export AGENT_CMD='opencode run --format json --print-logs'
```

### 4.2 运行与生成轨迹

主控脚本通过读取 `SKILL` 环境变量进行执行路由，拉起 Agent 并将标准输出重定向为 JSONL 轨迹文件，同时自动挂载对应技能的临时沙盒工作区。

```bash
# 说明：执行端到端评估，需通过环境变量指定技能（如 doc-reviewer, md-translator）
# 注意：不要将技能名称作为脚本的位置参数传入，否则会触发防呆报错
SKILL=doc-reviewer bash ./unit-test/opencode-skill-eval.sh all

# 产出文件默认位于：
# - 轨迹：./unit-test/evals/artifacts/doc-reviewer.jsonl
# - 报告与产物：./unit-test/evals/reports/doc-reviewer/
```

### 4.3 行为与产物断言

我们将“是否成功”的主观判断固化为 Node.js 脚本或 Bash 钩子断言。通过解析 JSONL 轨迹中的 `command_execution` 与文件操作记录，不仅能校验产物，还能精准捕获 Agent 是否陷入循环重试（“折腾”），并将其作为 CI 拦截红线。

```bash
# 说明：解析轨迹并断言关键产物。主控脚本默认会优先执行 config.sh 的 skill_after_artifact_checks 钩子，
# 若未定义则回退使用通用的 checks.js 断言器。
SKILL=doc-reviewer node ./unit-test/evals/agent/checks.js \
  ./unit-test/evals/artifacts/doc-reviewer.jsonl \
  ./unit-test/evals/reports/doc-reviewer
```

- 结果解读（示例：`doc-reviewer`）
  - `hasOutline`/`hasContent`：各类报告是否生成
  - `structureOk`：报告结构是否符合要求
  - `score`/`overall_pass`：确定性行为评分与总判定

### 4.4 运行结果与产物说明

单次评估运行后将生成不可变的行为轨迹、沙盒隔离的临时产物以及多维度的资源消耗报告。这些确定的物理文件构成了故障排查与 CI 自动化守门的数据基础。

- 事件轨迹文件（JSONL）
  - 路径：`./evals/artifacts/${SKILL}.jsonl`（可被技能配置覆盖）
  - 作用：记录 `OpenCode` 执行 Skill 的全过程事件；末尾追加 `opencode stats` 的统计信息。
- 报告与产物隔离目录
  - 路径：`./unit-test/evals/reports/${SKILL}`（可被技能配置覆盖）
  - 作用：每次运行前会被自动清空，用于存放该技能拆分出的报告，或作为“沙盒隔离区”存放临时文件（如拷贝的源文档），防止运行过程污染主干代码库的 `fixtures` 目录。
- 使用统计报告
  - 路径：`./unit-test/evals/reports/${SKILL}/usage.md`
  - 作用：提取并汇总模型使用的 Token 数据（支持提取现代大模型的 **Prompt Caching 缓存**和**推理思考 Tokens**）与费用，辅助评估稳定性与资源使用情况。
- 行为断言结果（标准输出）
  - 来源：优先调用 `config.sh` 中的 `skill_after_artifact_checks` 钩子（按技能定制），若未定义则回退调用通用的 `node ./unit-test/evals/agent/checks.js`。
  - 形态：以 JSON 打印关键断言字段

```json
# 说明：示例输出（不同 Agent 版本可能存在增删字段）
# 你可以将该 JSON 直接采集到 CI 日志中用于守门判断
{
  "hasOutline": true,
  "hasContent": true,
  "hasAssets": true,
  "hasFormat": true,
  "structureOk": true,
  "score": 1,
  "overall_pass": true
}
```

### 4.5 运行模式与参数

主控脚本的第一个位置参数 (`MODE`) 决定了 Agent 的系统提示词 (Prompt) 注入策略，支持内置的全量测试与针对特定功能模块的子集测试。

- `content`：仅执行“内容评审”，生成 1 个报告；JSONL 中只包含该评审类型的相关事件。
- `all`（默认）：执行四类评审，生成 4 个报告；JSONL 覆盖所有类型事件；适合完整端到端评估。
- 自定义字符串：直接作为自定义 Prompt 传入，适配个性化测试需求。

---

## 5 CI 建议与阈值守门

在流水线中结合静态校验与行为断言，可建立拦截 Skill 能力退化的自动化屏障。对于存在非确定性输出的模型，建议引入 `pass@k` 多次采样策略以平衡通过率与稳定性。

- **策略配置**
  - 静态层：将 `run_static.py` 的 `overall_pass` 设为必过。
  - 行为层：将 `checks.js`（或技能自定义钩子）的 `overall_pass` 设为必过。
  - 进阶（pass@k）：如果单次成功率不足 100%，可在 CI 中运行多次试验（例如 trials=5），统计 pass@k（至少一次成功，衡量能力）与 pass^k（次次成功，衡量稳定性），依据业务容忍度设置阈值。
- **故障排查**
  - 静态失败：直接根据 Python 脚本报错修复文档资产与约束。
  - 行为失败：优先查看 JSONL 事件中的命令顺序、重复执行与错误信息，定位断言失败根因。

---

## 6 如何新增一个 Skill 测试

为了确保框架的可扩展性，新增一个技能的测试只需遵循基于目录的约定，实现配置注入与断言钩子即可，无需修改主控核心脚本。

- **第一步：准备测试数据 (Fixtures)**
  在 `./unit-test/fixtures/<skill-name>/` 目录下准备输入样本（如 `input.md`）。这是 Agent 执行任务的源数据，框架运行时会自动将它们拷贝到沙盒目录，以防止原始数据被污染。
- **第二步：编写静态检查**
  在 `./unit-test/tests/<skill-name>/` 下创建静态规则。主调度器 `run_static.py` 会自动扫描该目录，执行无依赖的快速验证（如检查 `SKILL.md` 的 Frontmatter 完整性）。
- **第三步：创建技能专属配置 (`config.sh`)**
  在 `./unit-test/skills/<skill-name>/` 下创建 `config.sh`，利用 Bash 钩子覆盖默认行为：
  - `build_target_doc`：定义输入文档的拷贝与沙盒路径。
  - `build_prompt`：定义注入给 Agent 的测试指令。
  - `skill_after_artifact_checks`：定义专属的 Node.js/Bash 行为断言（检查文件是否存在、格式是否合规等）。
- **第四步：运行与调试**
  使用 `SKILL=<skill-name> bash ./unit-test/opencode-skill-eval.sh all` 触发端到端运行，并通过 `usage.md` 和 JSONL 日志验证 Token 消耗与重试行为是否符合预期。

---
