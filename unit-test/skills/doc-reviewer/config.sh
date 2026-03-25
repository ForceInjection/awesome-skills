#!/usr/bin/env bash
set -euo pipefail

# 目标文档（doc-reviewer）
build_target_doc() {
  local ut_dir="$1"
  echo "$ut_dir/fixtures/doc-reviewer/review-target.md"
}

# 根据模式构建 Prompt
build_prompt() {
  local mode="${1:-all}"
  local target_doc="${2:-}"
  if [[ -z "$target_doc" ]]; then
    target_doc="$(build_target_doc "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)")"
  fi
  if [[ "$mode" == "content" ]]; then
    cat <<EOF
请使用 doc-reviewer 技能，执行“内容评审”。

目标文档：$target_doc

要求：
- 按 2.2 内容评审规则分章节/子小节逐块审查
- 仅输出一个独立报告
- 严格使用结构：## 评审结果 - [内容评审] / ### 发现的问题 / ### 总结
- 不要修改原文件，仅给出审查结论与建议
EOF
  elif [[ "$mode" == "all" ]]; then
    cat <<EOF
请使用 doc-reviewer 技能，对以下文档分别执行“四类评审”：大纲评审、内容评审、资产与链接评审、格式评审。

目标文档：$target_doc

要求：
- 为每一种评审输出一个独立报告
- 每个报告严格使用结构：## 评审结果 - [评审类型名称] / ### 发现的问题 / ### 总结
- 不要修改原文件，仅给出审查结论与建议
EOF
  else
    echo "$mode"
  fi
}

skill_after_artifact_checks() {
  local artifact="$1"
  local reports_dir="$2"
  local target_doc="$3"
  node "$UT/evals/agent/checks.js" "$artifact" "$reports_dir"
}

# 自定义事件产物与报告目录（可选）
build_artifact_path() {
  local ut_dir="$1"
  echo "$ut_dir/evals/artifacts/doc-reviewer.jsonl"
}

build_reports_dir() {
  local ut_dir="$1"
  echo "$ut_dir/evals/reports/doc-reviewer"
}
