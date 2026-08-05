# Content Review Rules (Technical Editor)

The core of this review type is **deep reading and content quality control**.
**Execution strategy**: Review the document in chunks — **one section at a time, or even one subsection at a time** — never skim the entire document. Ensure the **accuracy, completeness, and readability** of the content, as well as consistency across descriptions and a unified writing style. Defer all purely typographical issues to the "format review".

- **Text Quality**:
  - **Accuracy**: Technical descriptions must be accurate; principle derivations and data metrics must be correct. Avoid vague phrasing and technical errors.
  - **Completeness**: Check whether the current section fully covers the scope promised by its heading; flag missing key information, skipped steps, or absent prerequisite explanations.
  - **Readability**: Assess whether paragraph structure is clear, sentences are not overly long, and the logic is easy for readers to follow. When necessary, suggest splitting complex long sentences into shorter ones, or converting dense text into lists/tables.
  - **Tone & Voice**: The language must be rigorous and professional; avoid colloquial and emotional expressions (avoid meta prefixes such as "Updated:" and "Status:"). Prefer the **active voice**, and trim verbose, dragging sentences or ones overrun with passive voice.
  - **Personal Pronouns**: In Chinese documents, avoid "you" (你). Use "大家" for a general audience, "我们" when addressing developers, or omit the pronoun and use objective phrasing when the context is clear (e.g., "Agent 理解软件能力").
  - **Information Provenance**: Cited data and experimental results must state clear sources; technical terms or abbreviations must be given their full name or a brief explanation at first occurrence.
  - **[Mandatory Deletion] Empty Transition Sentences**: LLMs frequently generate filler such as "This section will introduce..." or "Below we will show...". **Review rule**: If the first sentence after a heading carries no new technical or business information (zero information entropy), **delete it outright** — never attempt to rewrite or keep it.
    - 🔴 **Input**: `## Cache Design\nThis section mainly introduces the design and implementation of the system cache layer. To improve system throughput...`
    - 🟢 **Action**: Identify the first sentence as an information-free transition sentence and delete it.
    - ✅ **Output**: `## Cache Design\nTo improve system throughput...`
  - **Overview Paragraph Requirement**: Content after a section or subsection heading must **directly enter the business or technical context** and provide substantive information. If a parent heading is immediately followed by subheadings (e.g., `## 1.` followed by `### 1.1`), a table, or a list, insert an informative summary paragraph bridging the two. If the following content already provides detailed coverage, do not repeat it.
- **Consistency Control**:
  - **Terminology Consistency**: Proprietary terms and core concepts must remain absolutely consistent throughout the document (e.g., once "KV Cache" is chosen, never mix in "键值缓存").
  - **Logical Coherence**: Settings and descriptions must not contradict each other; ensure smooth logical flow across sections.
- **Code Quality**:
  - **Logic and Style**: Code examples must be logically correct and follow good programming style, balancing **readability**, **performance optimization**, and **maintainability**.
  - **Comments**: Code blocks must include appropriate comments explaining key logic to help readers understand.
- **Visualization Quality**:
  - Evaluate whether diagrams (e.g., architecture diagrams, sequence diagrams) and formulas accurately reflect the intent of the text.
  - Check that visual elements are consistent with the body text; look for logical gaps, missing information, or redundancy (note: rendering and syntax issues are deferred to the "format review").
