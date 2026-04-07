import re
from pathlib import Path
from typing import Dict, Any, List, Tuple


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _find_markdown_links(text: str) -> List[Tuple[str, str]]:
    pattern = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)")
    return pattern.findall(text)


def _find_markdown_images(text: str) -> List[str]:
    pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    return pattern.findall(text)


def check_no_secrets(text: str) -> bool:
    patterns = [
        r"\bsk-[A-Za-z0-9]{20,}\b",
        r"\bAKIA[0-9A-Z]{16}\b",
        r"\bghp_[A-Za-z0-9]{20,}\b",
        r"(?i:\bapi[_-]?key\s*[:=]\s*[A-Za-z0-9\-_=]{12,}\b)",
        r"(?i:\bsecret\s*[:=]\s*[A-Za-z0-9\-_=]{12,}\b)",
    ]
    return not any(re.search(p, text) for p in patterns)


def check_links_format(text: str) -> bool:
    links = _find_markdown_links(text)
    if not links:
        return True
    def ok(url: str) -> bool:
        if url.startswith("#"):
            return True
        return url.startswith("http://") or url.startswith("https://")
    return all(ok(url) for _, url in links)


def check_images_relative(text: str) -> bool:
    images = _find_markdown_images(text)
    if not images:
        return True
    def is_relative(p: str) -> bool:
        return not (p.startswith("http://") or p.startswith("https://") or p.startswith("/"))
    return all(is_relative(p) for p in images)


def check_filename_convention(path: Path) -> bool:
    name = path.name
    return name == name.lower() and "-" in name and " " not in name and "_" not in name


def run_checks(file_path: str) -> Dict[str, Any]:
    p = Path(file_path)
    text = _read_text(p)
    results = {
        "no_secrets": check_no_secrets(text),
        "links_format": check_links_format(text),
        "images_relative": check_images_relative(text),
        "filename_convention": check_filename_convention(p),
    }
    score = sum(1 for v in results.values() if v)
    total = len(results)
    return {"checks": results, "overall_pass": score == total, "score": round(score / total, 2)}


def _read_text2(p: Path) -> str:
    return p.read_text(encoding="utf-8")


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
            out[k.strip()] = v.strip()
    return out


def _check_exists_skill_md(base_dir: Path) -> tuple[bool, str]:
    p = base_dir / "skills" / "doc-reviewer" / "SKILL.md"
    ok = p.exists()
    return ok, "SKILL.md 存在" if ok else "缺少 skills/doc-reviewer/SKILL.md"


def _check_frontmatter(base_dir: Path) -> tuple[bool, str]:
    p = base_dir / "skills" / "doc-reviewer" / "SKILL.md"
    text = _read_text2(p)
    fm = _parse_frontmatter(text)
    ok = bool(fm.get("name")) and bool(fm.get("description"))
    return ok, "YAML Frontmatter 包含 name 与 description" if ok else "Frontmatter 缺少 name 或 description"


def _check_core_sections(base_dir: Path) -> tuple[bool, str]:
    p = base_dir / "skills" / "doc-reviewer" / "SKILL.md"
    text = _read_text2(p)
    required = [
        r"^#\s*文档评审\s*$",
        r"^##\s*1\.\s*评审类型",
        r"^##\s*2\.\s*评审规则",
        r"^##\s*3\.\s*评审输出格式",
        r"^##\s*4\.\s*示例",
    ]
    ok = all(re.search(pattern, text, flags=re.M) for pattern in required)
    return ok, "核心章节齐备" if ok else "缺少核心章节（文档评审/1-4节）"


def _check_four_types(base_dir: Path) -> tuple[bool, str]:
    p = base_dir / "skills" / "doc-reviewer" / "SKILL.md"
    text = _read_text2(p)
    required_types = [
        "大纲评审",
        "内容评审",
        "资产与链接评审",
        "格式评审",
    ]
    ok = all(t in text for t in required_types)
    return ok, "四类评审类型完整" if ok else "评审类型不完整"


def _check_output_format_block(base_dir: Path) -> tuple[bool, str]:
    p = base_dir / "skills" / "doc-reviewer" / "SKILL.md"
    text = _read_text2(p)
    ok = "## 评审结果 - [评审类型名称]" in text and "### 发现的问题" in text and "### 总结" in text
    return ok, "输出格式模板存在" if ok else "缺少评审输出格式模板"


def _check_no_bilingual_titles(base_dir: Path) -> tuple[bool, str]:
    p = base_dir / "skills" / "doc-reviewer" / "SKILL.md"
    text = _read_text2(p)
    bad = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("#"):
            if re.search(r"\([A-Za-z].*\)", line):
                bad.append(line.strip())
    ok = len(bad) == 0
    return ok, "标题仅使用一种语言" if ok else f"发现双语标题：{'; '.join(bad[:3])}"


def _check_numbering_headers(base_dir: Path) -> tuple[bool, str]:
    p = base_dir / "skills" / "doc-reviewer" / "SKILL.md"
    text = _read_text2(p)
    h2_lines = []
    h3_lines = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("## "):
            h2_lines.append(line)
        elif line.startswith("### "):
            h3_lines.append(line)
    h2_ok = all(re.match(r"^##\s+\d+\.\s+", line) for line in h2_lines)
    h3_ok = all(re.match(r"^###\s+\d+\.\d+\s+", line) for line in h3_lines)
    ok = h2_ok and h3_ok
    return ok, "标题编号格式符合规范" if ok else "标题编号格式不符合规范（期望：## n. … / ### n.m …）"


def run_skill_md_checks(base_dir: str) -> Dict[str, Any]:
    root = Path(base_dir)
    checks = []
    for cid, fn in [
        ("exists_skill_md", _check_exists_skill_md),
        ("frontmatter", _check_frontmatter),
        ("core_sections", _check_core_sections),
        ("four_types", _check_four_types),
        ("output_format", _check_output_format_block),
        ("no_bilingual_titles", _check_no_bilingual_titles),
        ("numbering_headers", _check_numbering_headers),
    ]:
        ok, note = fn(root)
        checks.append({"id": cid, "pass": ok, "notes": note})
    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)
    score = round(passed / (total or 1), 2)
    return {"score": score, "details": f"{passed}/{total} checks passed", "checks": checks}
