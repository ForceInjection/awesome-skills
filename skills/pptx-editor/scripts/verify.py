#!/usr/bin/env python3
"""PPTX 渲染验证：LibreOffice → PDF → pdftotext -bbox → 全页出界扫描。

超出幻灯片边缘的文本会被裁切（PPT 不会自动换行收窄），必须逐页检查。

用法：
  python3 verify.py 文件.pptx                 # 全部页
  python3 verify.py 文件.pptx --pages 2,20    # 指定页
  python3 verify.py 文件.pptx --margin 3      # 边缘容差(pt)，默认 0

退出码：0 全部通过；1 有出界文本；2 环境缺依赖。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile


def find_soffice():
    cands = [
        shutil.which("soffice"),
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--pages", help="逗号分隔页码，如 2,20；缺省全部")
    ap.add_argument("--margin", type=float, default=0.0, help="边缘容差(pt)，默认 0")
    args = ap.parse_args()

    soffice = find_soffice()
    if not soffice:
        print("错误：找不到 LibreOffice（soffice）", file=sys.stderr)
        sys.exit(2)
    for tool in ("pdftotext", "pdfinfo"):
        if not shutil.which(tool):
            print(f"错误：找不到 {tool}（poppler）", file=sys.stderr)
            sys.exit(2)

    sel = None
    if args.pages:
        sel = {int(s) for s in args.pages.split(",") if s.strip()}

    with tempfile.TemporaryDirectory() as td:
        pdf = os.path.join(td, "deck.pdf")
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", td, os.path.abspath(args.pptx)],
            check=True, capture_output=True,
        )

        total = 0
        info = subprocess.run([shutil.which("pdfinfo"), pdf], capture_output=True, text=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", info, re.M)
        if m:
            total = int(m.group(1))

        bad_count = 0
        for page in range(1, total + 1):
            if sel and page not in sel:
                continue
            out = os.path.join(td, f"p{page}.html")
            subprocess.run(
                ["pdftotext", "-f", str(page), "-l", str(page), "-bbox", pdf, out],
                check=True, capture_output=True,
            )
            html = open(out, encoding="utf-8").read()
            pm = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', html)
            words = re.findall(
                r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)</word>',
                html,
            )
            w, h = (float(pm.group(1)), float(pm.group(2))) if pm else (960.0, 540.0)
            bad = [
                x for x in words
                if float(x[2]) > w - args.margin or float(x[3]) > h - args.margin
            ]
            status = "OK" if not bad else f"{len(bad)} 个词出界"
            print(f"P{page:>2}: {len(words):>3} 词 | {status} (页面 {w:.0f}x{h:.0f}pt)")
            for x in bad:
                print(f"    出界: yMin={float(x[1]):.1f} xMax={float(x[2]):.1f}  {x[4]}")
            bad_count += len(bad)

        print(f"\n共 {bad_count} 个词出界" + ("，全部通过 ✓" if bad_count == 0 else "，需修复 ✗"))
        sys.exit(0 if bad_count == 0 else 1)


if __name__ == "__main__":
    main()
