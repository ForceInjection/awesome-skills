---
name: "web-content-downloader"
description: "下载网页并转换为 Markdown 文件，保留原网页语言（不翻译）。当用户请求下载网页、保存文章并提取图片时调用此技能。"
---

# Web Content Downloader

This skill is used to download specified web page content and convert it into Markdown format while retaining the original language (no translation). It also automatically extracts and downloads images from the web page into a local `img` directory, renames the images meaningfully, and correctly updates their references in the Markdown file.

## Workflow

Strictly follow these steps:

### 1. Fetch and Convert Web Content

- **Primary Method**: Use Jina Reader to fetch the content. Execute the terminal command `curl -s "https://r.jina.ai/<TARGET_URL>"`. This directly returns the main body in well-formatted Markdown.
- **Fallback Method**: If Jina Reader fails or returns empty content, fall back to other tools (such as `mcp_DuckDuckGo_Search_Server_fetch_content`, `curl`, or equivalent tools) to fetch the HTML content of the target URL, then clean and convert the HTML into Markdown.
- **Keep Original Language**: Do NOT translate the content. Retain the original language of the web page.
- **Table Handling**: If the original web page contains tables (HTML `<table>`), they MUST be accurately converted into standard Markdown table format (`|---|---|`). Avoid using HTML line break tags like `<br>` inside Markdown tables to keep them clean.
- **Formatting Rules**: Ensure the typography follows standard rules: insert spaces between Chinese and English characters; ensure code blocks have explanatory comments.

### 2. Extract Image Links

- Parse the original web content or HTML to extract all core image links. Pay attention not only to `<img src="...">` and Markdown image syntax, but also to modern responsive tags like `<source srcset="...">` or `srcset` attributes.
- Filter out meaningless images such as favicons, tracking pixels, or tiny UI icons.

### 3. Create Directory and Download Images

- Check if an `img` directory exists in the current workspace. If not, create it using the terminal command `mkdir -p img`.
- Use terminal commands (e.g., `curl -O`) to batch download the extracted images into the `img` directory.

### 4. Rename Images

- Generate **meaningful English or Pinyin names** for the downloaded images based on the article's context or what the image depicts (e.g., `design-patterns.png`).
- Use terminal commands (e.g., `mv`) to rename the downloaded images.

### 5. Update Markdown References

- Replace the original remote image links in the Markdown document with the local image links (e.g., `![design-patterns](./img/design-patterns.png)`).
- Save the final Markdown text to the file specified by the user, or generate a `.md` file based on the web page title and save it.
