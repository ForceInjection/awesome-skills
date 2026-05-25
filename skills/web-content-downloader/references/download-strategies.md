# 下载策略与回退机制

## 主要下载方式

1. **Jina Reader API**（首选）：`https://r.jina.ai/http://{url}`
   - 自动提取正文内容，剥离无关 HTML 标签
   - 返回格式良好的 Markdown
   - 支持大部分现代网页

2. **直接 HTTP 请求 + HTML 解析**（回退）：
   - 使用 `curl` 或 Python `requests` 获取原始 HTML
   - 使用 `BeautifulSoup` 或类似库提取正文
   - 适用于 Jina Reader 无法处理的页面

## 图片处理

- 提取文章中的核心配图
- 下载到本地 `img/` 目录
- 根据上下文重命名图片文件
- 替换 Markdown 中的图片链接为本地相对路径

## HTML 表格转 Markdown

- 识别 HTML `<table>` 元素
- 转换为标准 Markdown 表格格式
- 保持列对齐和可读性
