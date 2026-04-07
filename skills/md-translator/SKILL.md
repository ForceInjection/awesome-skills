---
name: "md-translator"
description: "将指定的本地 Markdown 文件翻译成指定语言（默认中文），并在文件名中添加语言标识后缀。当用户请求翻译本地 Markdown 文档时调用此技能。"
---

# Markdown Translator

This skill is used to translate the content of a specified local Markdown file into a target language (default is Chinese), and save the translated content as a new file with a language identifier suffix appended to the filename (e.g., `filename_zh.md`).

## Workflow

Strictly follow these steps:

### 1. Read the Original Document

- Use the file reading tool to read the contents of the local Markdown file specified by the user.

### 2. Translate the Content

- Translate the text content professionally and rigorously into the language specified by the user (if not specified, default to Chinese).
- **Chunking for Long Documents**: If the document is extremely long, split it into logical chunks (e.g., by main headers) and translate them sequentially to prevent context truncation or missing content.
- **Format Preservation**: You MUST preserve the original Markdown formatting during translation (including headers, lists, code blocks, bold text, links, image references, etc.).
- **Table Handling**: If the original text contains tables, you MUST accurately maintain the standard Markdown table format. Avoid using HTML line break tags like `<br>` inside Markdown tables.
- **Formatting Rules**: Ensure the typography follows standard rules: insert spaces between Chinese and English characters; ensure code blocks have explanatory comments.

### 3. Save the Translation Result

- Generate a new filename based on the target language. Append a language identifier suffix to the original filename (e.g., if the original file is `article.md`, save it as `article_zh.md` for Chinese, or `article_en.md` for English).
- Write the translated Markdown content into the new file.
