---
name: doc-reviewer
description: Review technical documents. Supports four independent review types: outline review (checks the table of contents and structural logic), content review (checks text accuracy and code quality), assets & links review (validates link and reference compliance), and format review (proofreads purely visual typography and punctuation). Use when the user requests a review or revision of a Markdown document.
---

# Document Review

This document defines the standard operating procedures and checklists for technical document review. To improve review efficiency and reduce attention dilution in large language models, document review is split into four **independent review types**. Based on the user's needs, the Agent can assume a dedicated role and perform a single review using the corresponding dedicated ruleset.

---

## 1. Review Types

When performing a review, the Agent should select one or more of the following types and execute them independently, based on the user's instructions or the document's actual state. Each review type should be handled as an independent Prompt task and produce an independent review report.

1. **Outline Review**
   - **Role**: Structure Architect
   - **Action**: Extract only all headings (TOC) of the document and examine the document skeleton from a global perspective. Identify structural issues and provide refactoring suggestions.
2. **Content Review**
   - **Role**: Technical Editor
   - **Action**: Split the document into chunks by section (or subsection) and read each chunk in depth. Focus on text quality, technical accuracy, and code logic.
3. **Assets & Links Review**
   - **Role**: Compliance & Asset Inspector
   - **Action**: Extract all hyperlinks, image paths, file references, and bibliography entries and check them in batch. Ensure external dependencies are valid and compliant.
4. **Format Review**
   - **Role**: Typography Proofreader
   - **Action**: Quickly scan the text, focusing on purely visual typography and punctuation standards. These issues typically support silent/automatic one-click fixes.

---

## 2. Review Rules

When executing a specific review type, the Agent loads the corresponding detailed rules file on demand:

- **Outline Review**: Load `references/outline-review-rules-en.md`; focus on the logic and reasonableness of the section arrangement.
- **Content Review**: Load `references/content-review-rules-en.md`; focus on text quality, technical accuracy, and code logic.
- **Assets & Links Review**: Load `references/assets-review-rules-en.md`; validate the validity and compliance of links, images, and references.
- **Format Review**: Load `references/format-review-rules-en.md`; focus on purely visual typography and Markdown syntax standards.

---

---

## 3. Review Output Format

For any review type, the review report must be output in the following standard format:

```text
## Review Result - [Review Type Name]

### Issues Found

1. **[Category] Line XX / Section N**: Issue description.
   - Suggestion: Specific fix suggestion or refactoring example.

### Summary

A total of X issues were found.
```

---

## 4. Example

**User**: "Help me run a content review on section 2 of `architecture.md`."

**Agent**:
(Trigger the content review rules and load the Technical Editor role)

> **[Content Review]**
>
> ### Issues Found
>
> 1. **[Text Quality] Under the Section 2 heading**: Missing overview paragraph; the document goes straight into subsections.
>    - Suggestion: Add an introduction covering the core architectural goals of this section.
> 2. **[Consistency] Line 32**: Inconsistent terminology; the preceding text uses "KV Cache", while "键值缓存" appears here.
>    - Suggestion: Unify to "KV Cache".
>
> ### Summary
>
> A total of 2 issues were found. Would you like me to apply these changes directly?
