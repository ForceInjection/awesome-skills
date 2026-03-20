---
name: deep-project-analysis
description: Generate a comprehensive project documentation (whitepaper) based on deep codebase analysis, covering architecture, modules, testing, and deployment.
---

# Deep Project Analysis

This skill extends the core mechanics of `deep-code-read` to systematically analyze an entire repository and synthesize a comprehensive "Project Whitepaper". It combines deep module-level understanding with high-level architectural synthesis and engineering practices (build, test, deploy).

The final output focuses heavily on Architecture & Module Deep Dives (approx. 60%), supported by practical Engineering & Operations guides.

## 1. The Team Roles

This workflow employs specialized agents to gather distinct types of information before synthesizing the final document:

- **Agent A (Tech Writer)**: The module expert. **This role is directly fulfilled by invoking the `deep-code-read` skill.** It reads source code to extract module-level capabilities, data structures, and state flows, ensuring high accuracy through its built-in ABC verification loop.
- **Agent B (DevOps Engineer)**: The infrastructure expert. Scans configuration files (Makefiles, Dockerfiles, CI/CD pipelines, `package.json`, etc.) to extract build, test, and deployment practices.
- **Agent C (Chief Architect)**: The synthesizer. Reads all outputs from the `deep-code-read` module skills and the DevOps Engineer to author the final Comprehensive Project Documentation, ensuring a coherent narrative and architectural accuracy.

**REQUIRED SUB-SKILL:** You MUST use the `deep-code-read` skill as the engine for Phase 2.

## 2. Usage

```bash
/deep-project-analysis <source> <output-dir>
```

- **source**: local path (e.g., `./path/to/repo`) or GitHub URL
- **output-dir**: where the final whitepaper and intermediate analysis files are written

## 3. Full Flow

You MUST follow these phases in order to generate the final documentation.

### 3.1 Phase 1: Prepare & Scan

This initial phase handles the resolution and preparation of the target source codebase.

1. Resolve the target repository (clone if URL, verify if local).
2. Scan the directory structure to identify:
   - **Code Modules**: Directories containing core business logic (`src/`, `lib/`, etc.).
   - **Infra Files**: Build scripts, Dockerfiles, CI/CD workflows, config files.
3. Generate an initial dependency graph between modules.

### 3.2 Phase 2: Deep Module Reading (via `deep-code-read`)

This phase delegates the heavy lifting of code comprehension to the `deep-code-read` skill.

For each identified core module, **invoke the `deep-code-read` skill** targeting that specific module directory.

- The `deep-code-read` skill will run its Tech Writer -> QA Engineer -> Junior Dev verification loop.
- Collect the generated, fully-verified `SKILL.md` files for each module.
  _Note: This phase focuses purely on code, logic, and data structures._

### 3.3 Phase 3: Infrastructure Analysis (DevOps Engineer)

This phase extracts engineering practices from configuration files.

Dispatch the DevOps Engineer agent (using `devops-engineer-prompt.md`).

- **Input**: All identified Infra Files (e.g., `Makefile`, `Dockerfile`, `.github/workflows/`, `pom.json`).
- **Output**: A structured report covering Build Steps, Testing Strategies, and Deployment Topologies.

### 3.4 Phase 4: Architectural Synthesis (Chief Architect)

This phase generates the final Comprehensive Project Documentation.

Dispatch the Chief Architect agent by **reading and strictly following** `chief-architect-prompt.md`.

- **Input**: The module documents generated in Phase 2, the infrastructure report from Phase 3, and the initial directory scan.
- **Project Name**: You MUST extract the actual project name (e.g., from the repository directory name, `package.json`, or `go.mod`) and use it to replace all `{project-name}` placeholders in the output filename.
- **Instruction constraints**:
  - The Architect MUST allocate approximately 60% of the document's depth and length to System Architecture and Core Modules, and the remaining 40% to Project Overview, Scenarios, and Engineering Practices.
  - **Diagrams**: You MUST output Mermaid syntax for architecture diagrams, flowcharts, and sequence diagrams as explicitly required in the Chief Architect prompt.
- **Output**: `<actual-project-name>-WHITEPAPER.md` written to the `<output-dir>`. The document MUST follow this exact 8-chapter outline:
  1. Project Overview
  2. System Architecture
  3. Core Modules Deep Dive
  4. Key Scenarios & Workflows
  5. Build & Run
  6. Testing & Quality Assurance
  7. Deployment & Operations
  8. Developer Guide

### 3.5 Phase 5: User Acceptance & Review

Present the generated `<actual-project-name>-WHITEPAPER.md` to the user.

> "The Comprehensive Project Documentation has been generated. Please review `<actual-project-name>-WHITEPAPER.md`. Let me know if you want to drill down into any specific architecture details or adjust the weight of any section."

## 4. Key Rules

Strictly adhere to the following rules during execution:

- **Read-Only Source**: Never modify the source repository.
- **Content Weighting**: Ensure the Chief Architect strictly adheres to the 60/40 ratio between Architecture/Modules and Engineering Practices.
- **Document Formatting**: The final output MUST follow professional technical writing standards (hierarchical numbering, no dual-language titles, consistent terminology).
