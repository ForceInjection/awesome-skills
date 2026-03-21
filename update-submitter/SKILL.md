---
name: "update-submitter"
description: "Analyzes git status, groups related file changes, and generates standardized Conventional Commits. Invoke when the user wants to commit changes, submit updates, or create a PR."
---

# Update Submitter

This skill automates the process of reviewing local repository changes, grouping related file modifications, and generating standardized commit messages following the Conventional Commits specification.

## 1. Core Workflow

The workflow outlines the exact steps to collect changes, group them, and generate commits.

### 1.1 Target Initialization

Accept the target directory and gather the current state of the repository.

1. Accept a target directory path from the user. If no path is provided, default to the current project directory.
2. Execute `git status` to retrieve the list of modified, added, deleted, and untracked files.
3. If necessary, execute `git diff` or `git diff --staged` to understand the context of the changes.

### 1.2 Change Analysis and Grouping

Analyze the changed files and group them into logical units that belong in the same commit.

1. Review the list of changed files.
2. Group files based on their relationships (e.g., UI components together, database schemas together, documentation updates together).
3. Ensure that unrelated changes are kept in separate commit groups to maintain a clean git history.

### 1.3 Commit Message Generation

Generate a standardized commit message for each logical group of changes.

1. Follow the Conventional Commits specification format: `<type>[optional scope]: <description>`.
2. Use the appropriate `type` based on the following standards:
   - `feat`: A new feature.
   - `fix`: A bug fix.
   - `docs`: Documentation only changes.
   - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc.).
   - `refactor`: A code change that neither fixes a bug nor adds a feature.
   - `perf`: A code change that improves performance.
   - `test`: Adding missing tests or correcting existing tests.
   - `chore`: Changes to the build process or auxiliary tools and libraries.
3. Provide a clear and concise `description` of the changes.

### 1.4 Execution and Confirmation

Present the proposed commit plan to the user and execute upon confirmation.

1. Output the proposed commit groups and their corresponding commit messages to the user for review.
2. Wait for the user's explicit confirmation.
3. Once confirmed, execute the appropriate `git add <files>` and `git commit -m "<message>"` commands for each group.

## 2. Usage Examples

These examples demonstrate how to invoke and use the skill in the terminal.

```bash
# Invoke the update-submitter skill on the current directory
/update-submitter

# Invoke the update-submitter skill on a specific directory
/update-submitter /path/to/project
```
