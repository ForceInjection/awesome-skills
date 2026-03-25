#!/usr/bin/env bash
set -euo pipefail

build_target_doc() {
  local ut_dir="$1"
  # 我们不直接使用原文档作为目标，而是每次测试前将原文档拷贝到 reports 目录进行隔离测试
  local reports_dir="$ut_dir/evals/reports/md-translator"
  mkdir -p "$reports_dir"
  cp "$ut_dir/fixtures/md-translator/input.md" "$reports_dir/input.md"
  echo "$reports_dir/input.md"
}

build_prompt() {
  local mode="${1:-all}"
  local target_doc="${2:-}"
  if [[ -z "$target_doc" ]]; then
    target_doc="$(build_target_doc "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)")"
  fi
  # md-translator 为行为型技能，这里统一引导翻译为中文并添加 _zh 标识
  cat <<PROMPT
请使用 md-translator 技能，将附带的 Markdown 文档完整翻译为中文，并保持 Markdown 格式与结构不变。

目标文档：$target_doc

要求：
- 翻译后新文件名需添加语言后缀，并且严格使用下划线（示例：article_zh.md）
- 保留所有标题、列表、代码块、链接与图片引用的原有结构
- 表格使用标准 Markdown 表格语法，避免使用 <br> 等 HTML 标签
PROMPT
}

skill_after_artifact_checks() {
  local artifact="$1"
  local reports_dir="$2"
  local target_doc="$3"
  node "$UT/evals/agent/checks.js" "$artifact" "$target_doc"
}

build_artifact_path() {
  local ut_dir="$1"
  echo "$ut_dir/evals/artifacts/md-translator.jsonl"
}

build_reports_dir() {
  local ut_dir="$1"
  echo "$ut_dir/evals/reports/md-translator"
}

skill_postprocess() {
  local artifact="$1"
  local reports_dir="$2"
  local target_doc="$3"
  # 这里不再需要拷贝了，因为测试本身就是针对 reports 目录下的隔离文件进行的
  # 我们可以清理掉作为测试输入的临时原文档，只保留生成的翻译结果
  if [[ -f "$target_doc" && "$target_doc" == *"/evals/reports/"* ]]; then
    rm -f "$target_doc"
  fi
}
