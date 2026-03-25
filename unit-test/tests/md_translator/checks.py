import re
from pathlib import Path
from typing import Dict, Any, Tuple


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if not m:
        return {}
    fm = m.group(1)
    out = {}
    for line in fm.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def _check_exists_skill_md(root: Path) -> Tuple[bool, str]:
    p = root / "md-translator" / "SKILL.md"
    ok = p.exists()
    return ok, "SKILL.md 存在" if ok else "缺少 md-translator/SKILL.md"


def _check_frontmatter(root: Path) -> Tuple[bool, str]:
    p = root / "md-translator" / "SKILL.md"
    text = _read_text(p)
    fm = _parse_frontmatter(text)
    ok = (fm.get("name") == "md-translator") and bool(fm.get("description"))
    return ok, "Frontmatter 完整（name/description）" if ok else "Frontmatter 缺少或不正确"


def _check_core_sections(root: Path) -> Tuple[bool, str]:
    p = root / "md-translator" / "SKILL.md"
    text = _read_text(p)
    required = [
        r"^#\s*Markdown Translator\s*$",
        r"^##\s*Workflow\s*$",
        r"^###\s*1\.\s*Read the Original Document\s*$",
        r"^###\s*2\.\s*Translate the Content\s*$",
        r"^###\s*3\.\s*Save the Translation Result\s*$",
    ]
    ok = all(re.search(r, text, flags=re.M) for r in required)
    return ok, "核心章节齐备（Workflow/1–3 步）" if ok else "缺少必要章节"


def _check_suffix_guidance(root: Path) -> Tuple[bool, str]:
    p = root / "md-translator" / "SKILL.md"
    text = _read_text(p)
    ok = ("_zh.md" in text) or ("-zh.md" in text) or (" .zh.md" in text) or (".zh.md" in text)
    return ok, "包含语言后缀命名示例" if ok else "缺少语言后缀命名说明（如 _zh.md）"


def _check_format_rules(root: Path) -> Tuple[bool, str]:
    p = root / "md-translator" / "SKILL.md"
    text = _read_text(p)
    ok = ("spaces between Chinese and English" in text) or ("中文" in text and "English" in text)
    ok = ok and ("code blocks" in text or "代码块" in text)
    ok = ok and ("Markdown table" in text or "Markdown 表格" in text)
    return ok, "包含必要格式与表格规范" if ok else "缺少格式规范说明"


def run_skill_checks(base_dir: str) -> Dict[str, Any]:
    root = Path(base_dir)
    checks = []
    for cid, fn in [
        ("exists_skill_md", _check_exists_skill_md),
        ("frontmatter", _check_frontmatter),
        ("core_sections", _check_core_sections),
        ("suffix_guidance", _check_suffix_guidance),
        ("format_rules", _check_format_rules),
    ]:
        ok, note = fn(root)
        checks.append({"id": cid, "pass": ok, "notes": note})
    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)
    score = round(passed / (total or 1), 2)
    return {"score": score, "details": f"{passed}/{total} checks passed", "checks": checks}
