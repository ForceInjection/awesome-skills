---
name: "openspec-assistant"
description: "Execute OpenSpec Spec-Driven Development (SDD). Covers intent alignment, spec generation, code implementation, and automated verification. Supports collaboration among the Architect (writes Spec / reviews), Developer (writes code), and QA (writes tests) roles, plus the /opsx command system."
---

# OpenSpec Spec-Driven Development Assistant Skill

This skill helps users conduct agile, high-determinism software development using the OpenSpec framework. As an AI coding assistant, we strictly follow the "Intent -> Spec -> Code -> Verification" collaboration paradigm to ensure that AI-generated code is controllable, trustworthy, and maintainable.

## 1. Role Responsibilities and Execution Flow Overview

This section provides a global overview of the core roles and the overall execution flow in the OpenSpec collaboration process, guiding how the user and AI collaborate across different stages.

### 1.1 Core Role Definitions

To ensure development standardization, the workflow is split into three core roles, each with distinct duties across the change lifecycle:

- **Architect**: Responsible for "thinking it through" and "final quality gate". Performs intent alignment and spec definition (generating Specs) before development; reviews code against the Spec and archives it after development.
- **QA (Test Engineer)**: Responsible for the "verification standard". Based on the Spec produced by the Architect, extracts business scenarios and designs automated test cases, providing a clear red/green acceptance baseline for development.
- **Developer**: Responsible for "implementation". Strictly follows the models and interfaces defined by the Spec, as well as the test cases provided by QA, to implement the business logic.

### 1.2 Standard Execution Flow

The standard lifecycle of a Change (or Milestone) flows as follows:

1. **Create and Define Spec (Architect)**: Initiate a new change and produce `proposal.md`, `design.md`, and `spec.md`.
2. **Validate Spec (Architect)**: Verify that the output spec document format is 100% correct.
3. **Design Tests (QA)**: Design and write test case skeletons based on the scenarios in `spec.md`.
4. **Implement Code (Developer)**: Write code based on the spec and test cases, establishing a code-to-spec traceability mapping.
5. **Run Tests (QA/Developer)**: Execute the test scripts to ensure all system behaviors match expectations and pass with all green.
6. **Review and Archive Code (Architect)**: Strictly review the code and, once confirmed not to deviate from the spec, merge it into the main baseline.

## 2. Core Philosophy and Architecture

This section outlines the underlying philosophy of OpenSpec and its core dual-state directory structure, serving as the theoretical foundation of the entire development flow.

OpenSpec is not just a document format — it is an engineering practice of Spec-Driven Development. It acts as a context anchor and contract guardian, constraining the boundaries of code generation.

- **Core philosophy**: Flowing rather than rigid, iterative rather than waterfall, simple rather than complex, and accommodating both existing and new projects (Brownfield-first).
- **Dual-state management**:
  - **Source of Truth** (`openspec/specs/`): The current true spec baseline of the system. Every released feature must have a corresponding spec definition here.
  - **Proposed Changes** (`openspec/changes/<name>/`): In-progress changes. Each change is an independent folder containing `proposal.md` (Why & What), `design.md` (How), `specs/` (Deltas), and `tasks.md` (Steps).

## 3. Role Collaboration and Workflow Details

This section outlines the specific responsibilities and core actions of the three core roles across different stages.

To ensure development standardization, the workflow is split into three core roles: Architect, QA, and Developer. For detailed action guides for each role within the Change lifecycle, read the `references/role-workflow-en.md` file.

## 4. Core Command System

This section lists the core commands that drive the OpenSpec flow, including AI collaboration commands and the underlying CLI commands.

### 4.1 AI Collaboration Commands (Slash Commands)

This subsection shows the recommended workflow commands for use in supported AI editors.

Use the following commands to drive the full flow:

- `/opsx:propose <description>`: Propose a change and generate the spec (Architect role).
- `/opsx:apply`: Implement code and tests based on the spec (Developer & QA roles).
- `/opsx:archive`: After development is complete, the code has been reviewed, and tests pass, archive the change and merge it into the main Spec.

### 4.2 CLI Command Quick Reference

This subsection provides operation guidance for the OpenSpec native command-line tool.

When low-level management or a cheat sheet for the OpenSpec native command-line tool is needed, read the `references/cli-commands-en.md` file.

## 5. Interaction and Execution Guidelines

This section summarizes the high-level guiding principles that must be followed when using the OpenSpec skill to ensure optimal AI collaboration.

1. **Context anchor**: In long conversations, always treat OpenSpec documents (Proposal / Design / Spec) as external memory. Extend by referencing existing Specs rather than re-analyzing the context.
2. **Contract guardian**: AI-generated code must strictly follow the interface contracts (Schema) defined by the Spec — never arbitrarily change JSON structures or status codes (e.g., 400, 409).
3. **Spec before code**: Refuse to write business code directly without a Spec definition.
4. **Incremental evolution**: When introducing complex features (e.g., authentication, persistence), extend incrementally based on the existing Spec architecture, avoiding rewrites from scratch.
