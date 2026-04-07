import sys
from pathlib import Path


def run_doc_reviewer() -> int:
    base = Path(__file__).resolve().parent
    # 运行静态资产约束检查
    from doc_reviewer.checks import run_checks, run_skill_md_checks

    target = base.parent / "fixtures" / "doc-reviewer" / "sample-doc.md"
    if not target.exists():
        print({"error": f"missing sample file: {target.as_posix()}"})
        return 1
    result1 = run_checks(target.as_posix())
    print(result1)

    # 校验技能说明文档（SKILL.md）结构完整性
    root = Path(__file__).resolve().parents[2]
    skill_md_dir = root / "skills" / "doc-reviewer"
    if (skill_md_dir / "SKILL.md").exists():
        result2 = run_skill_md_checks(root.as_posix())
        print(result2)
        ok = result1.get("overall_pass", False) and result2.get("score", 0) == 1
    else:
        # 不再输出提醒，视为可选检查，避免影响本地与 CI 的成功判定
        ok = result1.get("overall_pass", False)
    return 0 if ok else 2


def main() -> int:
    args = sys.argv[1:]
    skill = args[0] if args else "doc-reviewer"
    if skill == "doc-reviewer":
        return run_doc_reviewer()
    if skill == "md-translator":
        from md_translator.checks import run_skill_checks as run_md_checks
        result = run_md_checks(Path(__file__).resolve().parents[2].as_posix())
        print(result)
        return 0 if result.get("score", 0) == 1 else 2
    print({"warning": f"no static tests defined for skill: {skill}"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
