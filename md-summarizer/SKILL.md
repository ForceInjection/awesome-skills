---
name: "md-summarizer"
description: "分析和总结指定的本地 Markdown 文件，并输出结构化的中文总结。当用户请求总结、分析或提取本地 Markdown 文档信息时调用此技能。"
---

# Markdown Summarizer

Analyze and summarize text content from local Markdown files, outputting structured analysis in Chinese.

## Workflow

### Step 1: Read and Verify Content

Use the appropriate file reading tool to read the contents of the local Markdown file(s) specified by the user. If multiple files are provided, read them in parallel if possible.
**Verification**: After reading, verify the content. If the file is completely empty or lacks substantive text content (e.g., only contains a few image links), notify the user immediately and abort the summarization for that specific file.

### Step 2: Analyze Content

For each file, produce a structured analysis in Chinese with these sections. The output must be professional, objective, and insightful.

```markdown
## [File Name]

### 1. 核心概要 (Executive Summary)

A single paragraph summarizing the core message and main theme of the document.

### 2. 关键要点 (Key Takeaways)

- Use an unordered list to highlight the most important points, facts, or arguments. Keep it concise.

### 3. 深度解析 (Deep Analysis)

A deep dive into the significance, context, and details of the content.

- Highlight the underlying logic or mechanisms described in the text.
- Include any critical data, statistics, or evidence presented.
- Point out the author's primary stance or bias (if applicable).

### 4. 值得关注的细节 (Notable Highlights)

Notable quotes, unique perspectives, surprising information, or edge cases mentioned.

### 5. 结论与行动建议 (Conclusion & Actionable Advice)

Actionable advice, recommendations, or next steps derived from the content. 
If not applicable, summarize the final verdict.
```

### Step 3: Multi-File Comparison (when multiple files are provided)

After analyzing each file individually, add a comprehensive comparison section:

```markdown
## 综合对比分析 (Cross-Reference Analysis)

### 共同主题 (Common Themes)

Identify shared concepts, consistent viewpoints, or industry trends across all documents.

### 差异与冲突 (Differences & Contradictions)

Highlight conflicting data, varying perspectives, or different methodologies proposed across the sources.

### 综合结论 (Synthesis)

Merge the insights from all provided documents into a unified conclusion.
```

## Rules

- **Output Language**: ALWAYS output the final analysis in Chinese (中文), regardless of the source language.
- **Accuracy**: Preserve factual accuracy. Do not hallucinate or fabricate information not present in the source text.
- **Formatting**: Ensure that Chinese and English characters are separated by spaces.
- **Handling Long Content**: For exceptionally long documents where content is truncated, focus on the most substantive content already obtained. Add a disclaimer: "> _注意：原文内容过长，以下分析基于已获取的部分核心内容。_"
- **Adaptive Output**:
  - If the user provides files without explicit instructions, default to the full structured analysis.
  - If the user explicitly asks for a "quick summary" (简单总结), provide only the `核心概要` and `关键要点` sections.
