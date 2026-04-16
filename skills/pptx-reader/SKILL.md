---
name: pptx-reader
description: "理解、读取和分析 .pptx 幻灯片文件内容。当用户需要提取 PPT 文本或分析演示文稿时调用此技能。"
---

# PPTX 读取器技能

本文档详细介绍了如何利用本技能读取和解析 .pptx 文件。相关数据和最佳实践来源参考自 GitHub 的 [anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) 仓库。

## 1. 快速参考

通过 markitdown CLI 工具，可以一键提取幻灯片的核心文本内容，适用于快速的数据摄取场景。

| 任务            | 指南                                                                 |
| --------------- | -------------------------------------------------------------------- |
| 读取 / 分析内容 | 执行 `python -m markitdown presentation.pptx > output_dir/output.md` |

## 2. 环境准备

为避免依赖冲突与外部管理环境限制，所有解析脚本均需在独立的 Python 虚拟环境中执行。

在 macOS 等环境中，为避免与系统全局 Python 环境冲突（如遇到 `externally-managed-environment` 错误），强烈建议使用虚拟环境。

```bash
# 进入 scripts 目录
cd scripts

# 创建名为 venv 的虚拟环境
python3 -m venv venv

# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate

# 安装相关依赖
pip install "markitdown[pptx]" Pillow
```

## 3. 读取内容

通过 Python 脚本可直接从 .pptx 文件中提取纯文本流、生成多幻灯片视觉概览，或解包原始 XML 结构以供深度审查。

确保已激活 `scripts` 目录下的虚拟环境，随后可以执行以下命令：

```bash
# 创建统一的输出目录
mkdir -p output_dir

# 提取 PPTX 中的纯文本内容并输出到指定文件
python -m markitdown presentation.pptx > output_dir/output.md

# 生成指定 PPTX 文件的视觉概览图并指定输出前缀 (含目录)
python thumbnail.py presentation.pptx output_dir/thumbnails

# 将 PPTX 文件解包到指定的 unpacked 目录中
python office/unpack.py presentation.pptx output_dir/unpacked/
```

## 4. 转换为图像

利用 LibreOffice 和 Poppler 工具链，可将演示文稿无损渲染为 PDF 并逐页切分为高分辨率 JPEG 图像，为大模型多模态视觉分析提供基础语料。

将演示文稿转换为单张幻灯片图像以供视觉检查：

```bash
# 创建统一的输出目录
mkdir -p output_dir

# 将 PPTX 文件无头模式转换为 PDF，并输出到指定目录
python office/soffice.py --headless --convert-to pdf --outdir output_dir/ presentation.pptx

# 将生成的 PDF 文件转换为 150 DPI 的 JPEG 图像序列，并指定输出前缀 (含目录)
pdftoppm -jpeg -r 150 output_dir/presentation.pdf output_dir/slide
```

这将会生成 `output_dir/slide-01.jpg`、`output_dir/slide-02.jpg` 等文件，便于后续提取并交由大语言模型分析视觉排版。

## 5. 依赖项

文本提取、图像渲染与解包操作依赖以下 Python 包与系统级 CLI 工具链。

- **`markitdown[pptx]`**：用于文本提取。
- **`Pillow`**：用于生成缩略图网格。
- **LibreOffice (`soffice`)**：用于 PDF 转换（通过 `office/soffice.py` 在沙箱环境中自动配置）。
- **Poppler (`pdftoppm`)**：用于将 PDF 转换为图像。
