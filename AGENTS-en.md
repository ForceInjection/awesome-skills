# Agent Skills Project Panorama

[中文](AGENTS.md)

This document provides a comprehensive introduction to the `awesome-skills` project. The project offers a standardized, modular skill system for LLM-driven agents, covering multiple domains such as code development, document processing, architecture design, and engineering standards, with the goal of significantly enhancing the effectiveness of AI-assisted programming and automated operations.

## 1. Project Overview

Understanding the project's core positioning and key features helps developers quickly grasp its construction goals and overall value.

### 1.1 Core Positioning

The `awesome-skills` project is an open-source repository focused on accumulating Agent Skills and sharing best practices, occupying a core position in AI infrastructure and automation engineering. By encapsulating complex software engineering roles and workflows into independent, reusable agent skills, it enables AI coding assistants such as Trae and Cursor to load specialized capabilities on demand, thereby providing high-determinism assistance in scenarios such as code refactoring, documentation review, and continuous integration. According to the project's documentation, this system not only provides a rich set of built-in skills but also explores LLM-based engineering architecture design in depth.

### 1.2 Key Features

The project stands out in architecture design and ecosystem integration with the following advantages:

- **Modular design**: All skills are centralized under the project's [`skills/`](./skills/) directory. Each skill is managed in its own directory, following the single-responsibility principle for easy extension and maintenance.
- **Strict standards system**: Built-in skill review tools enforce consistency in prompt structure and metadata format.
- **Multi-scenario coverage**: From low-level code commit standards to high-level system architecture diagramming, the project covers the entire software development lifecycle.

## 2. Core Skill Matrix

The project's core built-in agent skills are all stored in the [`skills/`](./skills/) directory, organized by application scenario into three sections: document processing, engineering development, and architecture research.

### 2.1 Document and Content Processing

The skills in this category specialize in processing plain text, Markdown documents, and external web content, aiming to improve the quality and accessibility of technical documentation:

- **Document Reviewer (`doc-reviewer`)**: Splits technical document review into four independent types — outline, content, assets & links, and formatting — with detailed rules for each type loaded on demand, supporting automatic application of fixes with user authorization.
- **Markdown Link Checker (`md-link-checker`)**: Multi-threaded concurrent validation of the reachability of local file paths and external network URLs, with built-in LRU caching and anti-crawler retry mechanisms.
- **Markdown Summarizer (`md-summarizer`)**: Analyzes local Markdown files and outputs structured Chinese reports containing core summaries, deep dives, and key points, with support for multi-file comparative analysis.
- **Web Content Downloader (`web-content-downloader`)**: Fetches external web pages, strips redundant HTML, and converts them into standard Markdown, while also supporting intelligent extraction and localization of images.
- **Markdown Translator (`md-translator`)**: Translates local documents into target languages while strictly preserving the original layout and formatting.
- **Technical Article Outline Planner (`tech-outline-planner`)**: Uses a combined narrative structure (Context-first + Process narrative) to design "architecture-review-grade" outlines for high-quality technical articles.

### 2.2 Code and Engineering Assistance

The following skills directly serve the software development process, version control, and standards enforcement, primarily aimed at reducing developers' cognitive load and ensuring engineering standards are put into practice:

- **Deep Code Reader (`code-reader`)**: Systematically reads unfamiliar codebases and generates reusable cognitive skill files through three-agent collaboration (technical writer, QA engineer, junior developer) and a closed-book examination-style verification loop.
- **Directory Organizer (`dir-organizer`)**: Refactors and optimizes project directory structures in a standardized manner through a process of state collection, plan formulation, and user review, while automatically updating internal reference links.
- **Update Submitter (`update-submitter`)**: Analyzes local code changes, intelligently groups them, and generates commit messages conforming to the Conventional Commits specification.
- **Spec-Driven Development Assistant (`openspec-assistant`)**: Supports agile development based on the OpenSpec framework, enabling collaboration among architects, developers, and testers.
- **Agent Skill Reviewer (`agent-skill-reviewer`)**: Automatically reviews user-authored new skills to ensure their directory structures and prompts conform to best practices.

### 2.3 Architecture and Academic Research

Advanced skills targeting complex system design, presentation parsing, and academic citation management extend the boundaries of agents in multimodal and specialized academic domains:

- **Architecture Diagram Designer (`drawio-designer`)**: Directly manipulates the underlying XML structure to create and edit AWS-compliant architecture diagrams and export them as high-resolution images.
- **Deep Project Analyzer (`project-analyzer`)**: An extension of `code-reader` that performs comprehensive reverse engineering and static analysis on third-party repositories, generating a "Project Architecture Deep Analysis Report" containing 7 standard sections.
- **Knowledge Graph Ontology Management (`ontology`)**: Provides a typed knowledge graph system supporting entity creation, relationship management, and constraint validation, serving as a collaborative foundation for agents' cross-session memory layer and multi-skill state sharing.
- **PPTX Reader (`pptx-reader`)**: Unpacks and analyzes slide files, supporting text extraction and lossless image rendering to provide high-quality visual analysis corpora for LLMs.
- **Reference Organizer (`reference-organizer`)**: Cross-platform harvesting of metadata from academic papers and white papers, automatically generating citations conforming to the GB/T 7714 or IEEE standards.
- **Editorial Card Designer (`editorial-card-designer`)**: Transforms textual information into high-density HTML info cards in a modern editorial magazine style, supporting 8 fixed aspect-ratio presets and rendering to strictly aligned PNG screenshots.

## 3. Architecture Design and Best Practices

When building agent skills, the project adheres to a set of underlying design philosophies and rigorous engineering practice standards.

### 3.1 Audience Isolation Principle

Through a Chinese/English layering strategy, the project strictly distinguishes system files intended for LLMs from deliverables intended for humans, balancing model inference performance with the reading experience of human developers:

- **Agent-facing files**: All `SKILL.md` files and prompt templates serving as external knowledge bases are written entirely in English to maximize the instruction-following capability of LLMs.
- **Human-facing deliverables**: All analysis reports and documents ultimately delivered for developers to read are strictly output in Chinese and must follow professional typography conventions (e.g., spaces preserved between Chinese and English text).

### 3.2 Production-Grade Directory Standard

To improve skill maintainability and decouple instructions from concrete implementations, the project defines a standardized file organization. Taking the skills in this project's [`skills/`](./skills/) directory as an example, the standard skill directory structure is as follows:

```bash
# This is an example of a standard Agent Skill directory structure
# Ensure the SKILL.md filename is uppercase and includes the required subdirectories
my-awesome-skill/
├── SKILL.md       # Core standard operating manual, defining the skill's trigger phrases and system instructions
├── scripts/       # Executable scripts for atomic operations (e.g., Python or Shell)
├── references/    # Supplementary reference documents loaded on demand
└── assets/        # Static resources (e.g., images, icons)
```

## 4. Quality Assurance System

The project introduces an automated testing mechanism to ensure skill stability and execution reliability.

### 4.1 Automated Unit Testing

To prevent capability regression of skills during iteration, the project has built an evaluation framework based on automated execution scripts in the dedicated `unit-test` directory. By running the automated scripts, developers can test trigger precision, functional correctness, and LLM token consumption across multiple dimensions. The framework includes not only test assertion scripts but also a rich set of test fixtures that simulate real engineering scenarios, ensuring that every Agent Skill runs reliably in production environments.
