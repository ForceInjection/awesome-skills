#!/bin/bash
# mech-gates.sh —— self-review 第 3 步的机械门（**只读**：不改文件、不落 pyc）
#
# 用法（<SKILL_DIR> 指本技能的安装目录）：
#   bash <SKILL_DIR>/scripts/mech-gates.sh
#       默认取「工作区改动 + 未跟踪」：
#         git diff --name-only HEAD  ∪  git ls-files -o --exclude-standard
#   bash <SKILL_DIR>/scripts/mech-gates.sh <path>...
#
# 检查项：
#   *.sh / *.bash   bash -n            —— 语法
#   *.py            ast.parse          —— 语法（用 ast 而非 py_compile：**不落 __pycache__**）
#   所有文本文件    冲突标记            —— 判负（<<<<<<< / >>>>>>> / ======= 行首）
#   所有文本文件    行尾空白            —— 仅报告条数（不判负，只看是否突然变多）
#
# 退出码：0 = 无 FAIL；1 = 有 FAIL（语法错 / 冲突标记）；2 = 坐标问题（不在仓内 / 零待检文件）
# ⚠️ 它只是**机械门**：过了不等于评审通过——判据/失败方向/口径一致那几族要人（见 SKILL.md 第 4 步）。
set -uo pipefail

REPO="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "${REPO}" ]; then
    echo "✗ 不在 git 仓库内（cwd=$(pwd)）——先到目标仓/worktree 再跑。" >&2
    exit 2
fi
echo "== 受检仓：${REPO}（HEAD $(git rev-parse --short HEAD 2>/dev/null || echo '?')）=="

FILES=()
if [ "$#" -gt 0 ]; then
    for _p in "$@"; do FILES+=("$_p"); done
else
    while IFS= read -r _f; do
        [ -n "$_f" ] && FILES+=("$_f")
    done < <({ git diff --name-only HEAD; git ls-files -o --exclude-standard; } 2>/dev/null)
fi

if [ "${#FILES[@]}" -eq 0 ]; then
    # ⚠️ 零文件**不等于干净**（2026-09-29 实证：在 A 仓跑、改动全在 B worktree，
    # 旧版打"无待检文件"读起来像绿 ⇒ 整场机械门形同没跑）。宁可报错。
    echo "✗ 零待检文件——先确认这是**改动所在的**仓/worktree。" >&2
    echo "   （下面只列**同仓**的 worktree；改动若在**另一个仓**，这里看不到——去那边跑一遍。）" >&2
    while IFS= read -r _wt; do
        [ -z "${_wt}" ] && continue
        [ "${_wt}" = "${REPO}" ] && continue
        _n=$(git -C "${_wt}" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        if [ "${_n:-0}" -gt 0 ]; then
            echo "   ⚠️ 另一 worktree 有 ${_n} 处改动：${_wt}" >&2
        fi
    done < <(git worktree list --porcelain 2>/dev/null | awk '/^worktree /{print $2}')
    exit 2
fi

FAIL=0
N=0
WS_TOTAL=0
for f in "${FILES[@]}"; do
    [ -f "$f" ] || continue          # 删除/不存在的路径跳过
    N=$((N + 1))
    # 冲突标记：判负只认**无歧义**的两个——真标记后面必跟 ref 名（`<<<<<<< HEAD`），
    # 故**不能锚 `$`**（旧写法 `^(…|=======)$` 要求标记独占一行 ⇒ 真标记全漏）。
    if grep -IqE '^(<<<<<<<|>>>>>>>)( |$)' "$f" 2>/dev/null; then
        echo "  ✗ 冲突标记   $f"
        grep -InE '^(<<<<<<<|>>>>>>>)( |$)' "$f" | head -5 | sed 's/^/      /'
        FAIL=1
    elif grep -IqE '^=======$' "$f" 2>/dev/null; then
        # 裸分隔线：**也可能是**合法 markdown setext 下划线 ⇒ 只提示，不判负
        echo "  ⚠️ 疑似冲突分隔线（也可能是 markdown setext 下划线，人工看一眼） $f"
    fi
    case "$f" in
        *.sh|*.bash)
            if bash -n "$f" 2>/tmp/.mech_gates_err; then
                echo "  ✓ bash -n    $f"
            else
                echo "  ✗ bash -n    $f"
                sed 's/^/      /' /tmp/.mech_gates_err
                FAIL=1
            fi
            ;;
        *.py)
            if python3 -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8",errors="replace").read())' "$f" 2>/tmp/.mech_gates_err; then
                echo "  ✓ py-parse   $f"
            else
                echo "  ✗ py-parse   $f"
                sed 's/^/      /' /tmp/.mech_gates_err
                FAIL=1
            fi
            ;;
        *)
            echo "  · 跳过语法检查 $f（非 .sh/.py）"
            ;;
    esac
    # 行尾空白（只统计）
    _ws=$(grep -Icn '[ 	]$' "$f" 2>/dev/null | head -1)
    [ -n "${_ws:-}" ] && [ "${_ws}" != "0" ] && WS_TOTAL=$((WS_TOTAL + _ws))
done

rm -f /tmp/.mech_gates_err
echo
if [ "${N}" -eq 0 ] && [ "${#FILES[@]}" -gt 0 ]; then
    # ⚠️ FILES 非空但一条都没检 ⇒ 待检路径全是删除 / 不存在。
    #    **这不是"全过"**（本 skill 的 A2 族：计数为 0 就 PASS = 恒真判据，只是没有语法面可检）。
    echo "机械门：**无语法面可检**——待检 ${#FILES[@]} 条路径全是删除 / 不存在（N=0）。"
    echo "       删除类改动没有语法门可过；行为面靠单测 / 自证套件，别把本条读成「全过」。"
    exit 0
fi
echo "机械门：检了 ${N} 个文件；行尾空白合计 ${WS_TOTAL} 行（仅供参考）。"
if [ "${FAIL}" -eq 0 ]; then
    echo "结果：**全过**（语法 / 冲突标记）——判据与口径那几族仍要人工逐族查。"
    exit 0
fi
echo "结果：**有 FAIL**——先修再往下。"
exit 1
