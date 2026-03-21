---
name: web-summarizer
description: Analyze and summarize text-content websites. Use when the user provides a URL and asks to summarize, analyze, review, or extract information from a web page. Supports single or multiple URLs with structured analysis output in Chinese. Not for code repositories or API docs.
---

# Web Summarizer

Analyze and summarize text-content web pages, outputting structured analysis in Chinese.

## Workflow

### Step 1: Fetch Content

When multiple URLs are provided, fetch them **in parallel** (multiple tool calls in one message) to save time.

For each URL, choose the fetching method:

#### Method 1: Jina Reader (Primary)

For standard web pages, blogs, and articles:

1. Fetch `https://r.jina.ai/<URL>` using the `WebFetch` tool or equivalent HTTP client.
2. If the result contains meaningful text content, proceed to Step 2.
3. If Jina Reader returns empty, times out, or returns garbled content, fall back to Method 2.

#### Method 2: Direct Fetch / MCP Browser Fallback

If Jina Reader fails, or for the following domains known to block scrapers or rely heavily on dynamic rendering, skip Jina and use this method directly:

- `mp.weixin.qq.com` (WeChat articles)
- `weibo.com`
- `zhihu.com`
- `xiaohongshu.com`
- `douyin.com`
- `x.com` / `twitter.com`

**Fallback Steps:**

1. Attempt to fetch using `mcp_DuckDuckGo_Search_Server_fetch_content` if available in your tools.
2. Alternatively, if a browser-use MCP is available:
   - Use `new_page` with the target URL.
   - Wait a few seconds for dynamic content to render.
   - Use `take_snapshot` to get the accessibility tree text.
   - Scroll and snapshot again if content is truncated.

### Step 2: Analyze Content

For each page, produce a structured analysis in Chinese with these sections. The output must be professional, objective, and insightful.

```markdown
## [Page Title](URL)

### 1. 核心概要 (Executive Summary)

One-paragraph summary capturing the core message and purpose of the page.

### 2. 关键要点 (Key Takeaways)

- Bullet list of the most important points, facts, or arguments. Keep it concise.

### 3. 深度解析 (Deep Analysis)

Longer discussion of the content's significance, context, and nuance.

- Highlight the underlying logic or mechanism described in the text.
- Include any critical data, statistics, or evidence presented.
- Identify the author's primary stance or bias (if applicable).

### 4. 值得关注的细节 (Notable Highlights)

Notable quotes, unique perspectives, surprising information, or edge cases mentioned.

### 5. 结论与行动建议 (Conclusion & Actionable Advice)

Actionable takeaways, recommendations, or next steps derived from the content.
If not applicable, summarize the final verdict.
```

### Step 3: Multi-URL Comparison (when multiple URLs are provided)

After analyzing each page individually, add a comprehensive comparison section:

```markdown
## 综合对比分析 (Cross-Reference Analysis)

### 共同主题 (Common Themes)

Identify shared concepts, points of agreement, or industry trends across all sources.

### 差异与冲突 (Differences & Contradictions)

Highlight conflicting data, varying perspectives, or different methodologies proposed by the sources.

### 综合结论 (Synthesis)

An overarching conclusion that merges the insights from all provided URLs into a unified takeaway.
```

## Rules

- **Output Language**: ALWAYS output the final analysis in Chinese (中文), regardless of the source language.
- **Accuracy**: Preserve factual accuracy. Do not hallucinate or fabricate information not present in the source text.
- **Handling Paywalls**: If a page is paywalled, login-gated, or otherwise inaccessible, report this clearly: "⚠️ 无法访问：该页面受登录或付费墙限制" and skip analysis for that URL.
- **Handling Long Content**: For exceptionally long pages where content is truncated, focus on the most substantive content already obtained. Add a disclaimer: "> _注意：原文内容过长，以下分析基于已获取的部分核心内容。_"
- **Adaptive Output**:
  - If the user provides URLs without explicit instructions, default to the full structured analysis.
  - If the user explicitly asks for a "quick summary" (简单总结), provide only the `核心概要` and `关键要点` sections.
