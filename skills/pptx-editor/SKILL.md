---
name: pptx-editor
description: 精确修改 PowerPoint (.pptx)——按 shape 名定位做 run 级文本替换、风格化新增元素，并用 LibreOffice + pdftotext 渲染验证无出界、无碰撞。当用户要求修改、编辑或更新现有 .pptx 演示文稿中的文本、布局或元素时使用。
---

> English version: [SKILL-en.md](SKILL-en.md)

# PPTX 编辑器技能

本文档定义对现有 `.pptx` 进行**精确、可验证修改**的标准流程。与 [pptx-reader](../pptx-reader/SKILL.md) 互补：reader 负责读取与提取，本技能负责修改与验证。

核心原则：**改完没渲染 = 没验证**。本技能假设执行环境无法直接查看图片，一切排版结论以渲染后的词级坐标为准。

## 1. 快速参考

| 任务 | 做法 |
| --- | --- |
| 修改前勘察 | `python3 scripts/dump.py 文件.pptx --slides 2,20`（列出每页 shape 的 name / 几何 / 字体 / 文本） |
| 文本替换 / 新增元素 | 写一次性 patch 脚本（模板 `scripts/patch_template.py`），run 级替换 + paragraph 级兜底，逐条输出 OK/MISS |
| 渲染验证 | `python3 scripts/verify.py 文件.pptx`（LibreOffice → PDF → pdftotext -bbox → 全页出界扫描，退出码 0=通过） |
| 碰撞 / 带间距检查 | 用 bbox 词级坐标 + 元素独有词做 marker 定位（见 §4.2） |

## 2. 环境准备

依赖：`python3` + `python-pptx`、LibreOffice（`soffice`）、poppler（`pdftotext` / `pdfinfo`）。

- macOS：`soffice` 位于 `/Applications/LibreOffice.app/Contents/MacOS/soffice`，脚本会自动探测。
- `python-pptx` 缺失时，在技能 `scripts/` 目录下建 venv：`python3 -m venv venv && venv/bin/pip install python-pptx`。
- 渲染时 PDF 中的字体是**替换字体**（如 MiSans → fallback），行高与 PowerPoint/Keynote 略有差异——排版余量按 §5 的经验值留足。

## 3. 修改工作流

1. **勘察**：`dump.py` 列出目标页全部 shape。本仓库 deck 的 shape 都有语义化命名（如 `p20_shift`、`f2_src`）——**按 shape 名定位**，不要按页内文字盲搜替换。
2. **Patch**：按模板写 `/tmp/fix_ppt_*.py`，一次 patch 只做一组相关修改；脚本内逐条输出 `OK xN / MISS`，全部 OK 才算完成。
3. **验证**：`verify.py` 全页出界扫描；涉及新增/移动元素时再做带间距检查（§4.2）。
4. **报告**：向用户报告每处修改的定位方式与验证结果；如发现既有 bug（如文本被裁出幻灯片），如实报告并修复。

## 4. Patch 方法（python-pptx）

### 4.1 文本替换：run 级优先，paragraph 级兜底

- **run 级**：`old in r.text` 时 `r.text = r.text.replace(old, new)`——保留该 run 的字体格式。
- **paragraph 级兜底**：一句话被拆成多个 run 时，拼接全部 run 文本，匹配后整体写回第一个 run、清空其余 run（保留第一 run 的格式）。
- 常用模板函数见 `scripts/patch_template.py` 的 `rep_runs()` / `replace_in_paragraph()`。

### 4.2 新增元素：拷贝邻近元素的风格

新增文本框前，用 `dump.py` 查同页相近元素的实际参数，逐项照抄：

- `font.name`（本 repo deck 为 MiSans）、`font.size`、`font.bold`、`font.color.rgb`
- `tf.margin_* = 0`、`tf.word_wrap`、`tf.vertical_anchor`（MIDDLE/TOP）、`p.line_spacing`
- 位置用英寸小数（如 `Inches(4.36)`），与页面既有网格对齐

模板函数见 `patch_template.py` 的 `add_text()`。

### 4.3 几何与排版调整

- 改位置/尺寸：`shape.top = Inches(x)`、`shape.height = Inches(h)`
- 改换行行为：`shape.text_frame.word_wrap = True/False`
- 改行距：`paragraph.line_spacing = 1.0`（默认 1.2–1.35）

## 5. 验证方法（无图环境）

### 5.1 出界扫描（每次修改后必做）

`verify.py`：LibreOffice headless 转 PDF → `pdftotext -bbox` 取词级坐标 → 检查是否有词超出页面边缘（**超出即被裁切**，PPT 不会自动换行收窄）。

### 5.2 带间距 / 碰撞检查

多个元素垂直相邻时，用**元素独有词**做 marker 定位各元素，检查带间间隙：

```python
import re, subprocess
subprocess.run(["pdftotext","-f",str(pg),"-l",str(pg),"-bbox",pdf,out], check=True)
words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)</word>',
                   open(out, encoding="utf-8").read())
def band(ws): return (min(float(w[1]) for w in ws), max(float(w[3]) for w in ws))
cap = [w for w in words if "拉平" in w[4]]          # marker 用元素独有词
shift = [w for w in words if "价值正在" in w[4]]
gap = band(shift)[0] - band(cap)[1]                 # 负数 = 碰撞
```

marker 选择陷阱：避免同时命中其他元素的词（如 `$150` 会同时出现在标题和图表里）；命中多个时按坐标（y 范围）二次过滤。

## 6. 经验与陷阱（本技能沉淀自真实修改案例）

1. **`wrap="none"` 是定时炸弹**：文本被追加变长后不会换行，直接溢出幻灯片右缘被裁切（曾致整句"…跨境流。"不可见）。追加文本后检查 `word_wrap`，并渲染确认。
2. **行高估算**（LibreOffice fallback 字体）：每行 ≈ 字号 × 1.32（line_spacing 1.0 时 ≈ ×1.21）。预留带间 ≥5pt 间隙，因为 PowerPoint/Keynote 用真实字体渲染会有偏差。
3. **单行宽度估算**：12pt 下 CJK ≈ 12pt/字、拉丁/数字 ≈ 6.4–6.9pt/字。13.33" 宽页面可用 ≈ 832pt，超出必折行。
4. **折行会引发连锁碰撞**：折行后行数 × 行高会侵占下方元素。新增文字前先算行数，再定字号/框高。
5. **字体替换差异**：渲染验证用的是替换字体，行高只增不减——验证通过即可认为真实环境（更紧凑）也通过。
6. **.pptx 常被 gitignore**（如本 repo）：修改前确认文件是本地工作稿，重要版本先备份。
7. **一次 patch 只动一组相关修改**，逐条 OK/MISS；别攒一批一起改，MISS 时无法定位。

## 7. 依赖项

- `python-pptx`：读写 .pptx。
- LibreOffice（`soffice`）：headless 转 PDF，用于渲染验证。
- poppler（`pdftotext`、`pdfinfo`）：提取 PDF 词级坐标。
