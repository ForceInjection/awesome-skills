#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# OpenCode Skill E2E Evaluator (unit-test)
# 说明：
# - 以最小依赖执行指定 SKILL 的端到端评估：生成 JSONL 事件、拆分评审报告、解析用量、执行行为断言
# - 支持多技能：通过 skills/<skill>/config.sh 注入技能特定的 Prompt、目标文档与行为断言
# - 静态单测：可选，按 SKILL 调度对应的静态校验（文档资产与约束、SKILL.md 结构完整性等）
# 使用：
#   SKILL=doc-reviewer bash unit-test/opencode-skill-eval.sh all
#   SKILL=md-translator bash unit-test/opencode-skill-eval.sh all
# 约定变量（主控脚本提供给各技能 config.sh 使用）：
#   - REPO：仓库根目录
#   - UT：unit-test 目录
#   - SKILL：技能名称
#   - MODE：运行模式（content/all/自定义字符串）
#   - ARTIFACT：JSONL 事件产物路径
#   - REPORTS_DIR：评审报告输出目录
#   - TARGET_DOC：技能所需的目标文档路径（由 config.sh 的 build_target_doc 定义）
#   - PROJECT_DIR：行为断言可能需用到的项目目录
#   - AGENT_CMD：Agent CLI 命令（默认 opencode run --format json --print-logs）
# 输出：
#   - JSONL 事件：$UT/evals/artifacts/test-01.jsonl
#   - 评审报告（拆分后）：$UT/evals/reports/*.md
#   - 用量与成本报告：$UT/evals/reports/usage.md
#   - 行为断言结果：标准输出 JSON（overall_pass/score/逐项布尔）
# -----------------------------------------------------------------------------
set -euo pipefail
REPO="/Users/wangtianqing/Project/study/awesome-skills"
UT="$REPO/unit-test"
SKILL="${SKILL:-doc-reviewer}"
MODE=${1:-all}

# 如果 MODE 是某个技能的名称，大概率是用户用错了命令（把技能名当成了 MODE 参数）
if [[ -d "$UT/skills/$MODE" ]]; then
  echo "Error: 错误的用法。你传入的 '$MODE' 是一个技能名称。"
  echo "正确的用法应该是: SKILL=$MODE bash unit-test/opencode-skill-eval.sh all"
  exit 1
fi

# 加载 Skill 配置（每个技能一个 config.sh），用于注入技能特定的 Prompt、目标文档与行为断言
CONFIG_DIR="$UT/skills/$SKILL"
CONFIG_FILE="$CONFIG_DIR/config.sh"

# 默认目标文档（doc-reviewer 的示例；若技能提供 build_target_doc 会覆盖）
TARGET_DOC_DEFAULT="$UT/fixtures/doc-reviewer/review-target.md"
TARGET_DOC="$TARGET_DOC_DEFAULT"

if [[ -f "$CONFIG_FILE" ]]; then
  # shellcheck source=/dev/null
  source "$CONFIG_FILE"
  # 优先加载目录覆盖，以便清理和隔离
  if type build_reports_dir >/dev/null 2>&1; then
    REPORTS_DIR="$(build_reports_dir "$UT")"
  fi
  if type build_artifact_path >/dev/null 2>&1; then
    ARTIFACT="$(build_artifact_path "$UT")"
  fi
fi

# 若技能未设置 Prompt，回退到 doc-reviewer 的默认描述
if [[ -z "${PROMPT:-}" ]]; then
  if [[ "$MODE" == "content" ]]; then
    PROMPT="请使用 doc-reviewer 技能，执行“内容评审”。\n\n目标文档：$TARGET_DOC\n\n要求：\n- 按 2.2 内容评审规则分章节/子小节逐块审查\n- 仅输出一个独立报告\n- 严格使用结构：## 评审结果 - [内容评审] / ### 发现的问题 / ### 总结\n- 不要修改原文件，仅给出审查结论与建议"
  elif [[ "$MODE" == "all" ]]; then
    PROMPT="请使用 doc-reviewer 技能，对以下文档分别执行“四类评审”：大纲评审、内容评审、资产与链接评审、格式评审。\n\n目标文档：$TARGET_DOC\n\n要求：\n- 为每一种评审输出一个独立报告\n- 每个报告严格使用结构：## 评审结果 - [评审类型名称] / ### 发现的问题 / ### 总结\n- 不要修改原文件，仅给出审查结论与建议"
  else
    PROMPT="$MODE"
  fi
fi

# 产物与执行环境约定（可被技能配置覆盖）
ARTIFACT="${ARTIFACT:-"$UT/evals/artifacts/${SKILL}.jsonl"}"
REPORTS_DIR="${REPORTS_DIR:-"$UT/evals/reports/$SKILL"}"

# 在每次执行 Agent 前，清理该技能专属的 reports 目录，防止遗留脏数据（如之前测试的翻译产物）
rm -rf "$REPORTS_DIR"
mkdir -p "$REPORTS_DIR"

if [[ -f "$CONFIG_FILE" ]]; then
  # 技能可选：提供目标文档路径（放在清理目录之后，确保拷贝不会被清理掉）
  if type build_target_doc >/dev/null 2>&1; then
    TARGET_DOC="$(build_target_doc "$UT")"
  fi
  # 技能可选：生成 Prompt（放在获取最新 TARGET_DOC 之后）
  if type build_prompt >/dev/null 2>&1; then
    PROMPT="$(build_prompt "$MODE" "$TARGET_DOC")"
  fi
fi

USAGE_REPORT="${USAGE_REPORT:-"$REPORTS_DIR/usage.md"}"
AGENT_CMD_DEFAULT='opencode run --format json --print-logs'
AGENT_CMD="${AGENT_CMD:-$AGENT_CMD_DEFAULT}"
export AGENT_CMD
command -v opencode >/dev/null 2>&1 || { echo "error: opencode not found in PATH"; exit 1; }
# 执行 Agent：生成 JSONL 事件产物
bash "$UT/evals/agent/run.sh" "$PROMPT" "$ARTIFACT" "$TARGET_DOC"
# 追加用量统计文本（若 Agent 支持）
opencode stats >> "$ARTIFACT" || true
# 拆分评审报告（从 JSONL/文本中提取并按类型写入 Markdown）
node "$UT/evals/agent/split-reports.js" "$ARTIFACT" "$REPORTS_DIR"
# 解析 LLM 用量与成本，生成 usage.md
node "$UT/evals/agent/parse-usage.js" "$ARTIFACT" "$USAGE_REPORT"
# 行为断言：优先调用技能自定义钩子（skill_after_artifact_checks），否则回退到通用断言
if grep -q '"type"' "$ARTIFACT"; then
  if type skill_after_artifact_checks >/dev/null 2>&1; then
    skill_after_artifact_checks "$ARTIFACT" "$REPORTS_DIR" "$TARGET_DOC"
  else
    node "$UT/evals/agent/checks.js" "$ARTIFACT" "$REPORTS_DIR"
  fi
else
  echo "{\"warning\":\"artifact-not-json\",\"path\":\"$ARTIFACT\"}"
fi

if type skill_postprocess >/dev/null 2>&1; then
  skill_postprocess "$ARTIFACT" "$REPORTS_DIR" "$TARGET_DOC"
fi
# 静态单测调度：按 SKILL 分发（若无分发入口则回退到 doc-reviewer）
if [[ -f "$UT/tests/run_static.py" ]]; then
  python3 "$UT/tests/run_static.py" "$SKILL"
fi
