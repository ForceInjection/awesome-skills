# Combined Narrative Structure for Technical Writing

High-quality technical articles, especially those concerning system architecture, AI, or low-level engineering, benefit from a dual-layer approach that addresses both the "Why" and the "How".

## 1. Outer Layer: Context-first (Classic Style)

The "Classic Style" aims to be as transparent as a window. It assumes the reader is an equal and seeks to present technical truth without unnecessary ornamentation.

### 1.1 The C-I-S-T Framework

- **Context (背景)**: Why are we here? What is the environment? Define the status quo and the technological landscape.
- **Issue (问题)**: What broke? What is missing? Identify the pain point or the limitation that necessitates a new approach.
- **Solution (方案)**: How do we fix it? Describe the core mechanism, architecture, or algorithm.
- **Trade-off (权衡)**: What did we give up? Engineering is the art of trade-offs. Discuss performance vs. complexity, cost vs. speed, etc.

## 2. Inner Layer: Process Narrative

While the outer layer provides the macro structure, the inner layer handles the micro-flow within technical sections.

### 2.1 Logical Sequences

A technical explanation should feel like a well-edited film. Each concept should naturally "cut" to the next.

- **Sequential**: A → B → C (Time or logic based).
- **Hierarchical**: Whole → Parts (Structural).
- **Comparative**: A vs B (Decision based).

### 2.2 The "Given before New" Principle

This is a linguistic and cognitive tool to ensure organic connectivity.

- **Definition**: Every sentence should start with information that the reader already knows (from the previous sentence or general knowledge) before introducing a new piece of information.
- **Example**:
  - _Bad_: "The Transformer uses Attention. Attention calculates weights." (Repetitive and jumpy).
  - _Good_: "To process sequences efficiently, the Transformer relies on **Attention**. This **Attention mechanism** allows the model to calculate weights..."
  - _Analysis_: The "New" information in the first sentence ("Attention") becomes the "Given" information in the second sentence, creating a bridge.

## 3. Architecture Review Grade Quality

To achieve "Architecture Review Grade" quality, the outline must demonstrate:

- **Macro Logic**: A clear understanding of the business or technical motivation (The "Why").
- **Technical Rigor**: A granular, logical breakdown of the implementation (The "How").
- **Critical Thinking**: A self-aware analysis of the solution's limits (The "Trade-offs").
