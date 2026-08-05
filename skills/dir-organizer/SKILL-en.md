---
name: "dir-organizer"
description: "Organize and optimize project directory structures. Invoke this skill when the user requests directory organization, file categorization, cleanup of unused files, or refactoring of folder structures."
---

# Directory Organization Skill

This skill helps users normalize and optimize project directory structures to improve project maintainability.

---

## 1. Trigger Scenarios

The following scenarios should trigger this skill to ensure a sound directory structure.

- The user explicitly requests organizing the current or a specified directory;
- The directory contains many uncategorized scattered files;
- The project requires structural refactoring or cleanup of temporary files.

---

## 2. Core Capabilities

This skill supports various basic and advanced operations on directories and files to meet different levels of organization needs.

- **Create directories**: Create new target directories at appropriate locations based on file categorization needs.
- **Rename directories**: Rename a directory to more accurately reflect its contents.
- **Move files**: Move scattered or misplaced files into appropriate archive directories.
- **Rename files**: Rename single or multiple files to ensure consistent and standardized naming conventions.

---

## 3. Execution Principles

When organizing directories, follow these core principles to ensure safe and standardized operations.

- **Structure analysis**: Before performing any operation, first analyze the current file distribution and dependencies.
- **Safety assurance**: For core files or dependencies that may affect project operation (e.g., configuration, source code), confirm with the user before moving.
- **Standardized naming**: New directories and files must follow the project's unified naming conventions (e.g., keep spaces between Chinese and English).
- **Redundancy cleanup**: Identify and clean up common useless cache or log files.

---

## 4. Standard Execution Steps

A standardized execution workflow ensures directory organization proceeds in an orderly manner.

### 4.1 Status Collection

Collect detailed status information about the current directory.

1. Use terminal tools or scripts to read the complete file list of the target directory.
2. Identify file extensions and their potential purposes.

### 4.2 Plan Creation and Review

Based on the collected information, create a detailed restructuring plan, and the user must review it (Review). **【Mandatory requirement】: You must first print the complete restructuring plan in a regular text reply so that the user can actually see it, and only then initiate a confirmation request (e.g., by invoking the AskUserQuestion tool). Never ask a question directly without first outputting the plan content.**

When outputting the restructuring plan, follow the standardized format below:

1. **Directory and file adjustment plan**: In the text reply, use a Markdown tree structure to clearly show the target state, and use tags to explicitly mark the type of change (e.g., `[新建]`, `[不变]`, `[重命名自: xxx]`, `[移动自: xxx]`). **The tree structure must include the specific files in the directories, not just the directory hierarchy.**
2. **Cleanup plan**: Use a separate list to present the list of useless files to be deleted.
3. **Wait for confirmation**: After ensuring that the plan content above has been fully displayed in the user's chat interface, explicitly ask the user, via a tool or in language, whether they agree to execute the restructuring plan.

### 4.3 Execution and Verification

After the user explicitly agrees to the restructuring plan, actually perform the directory adjustment operations.

1. Use terminal commands to move files, rename files, and create directories.
2. Verify the operation results and present the final directory tree structure to the user.

### 4.4 Automatic Reference Link Updates

After completing file moves and structural adjustments, automatically handle the reference relationships between files properly without asking again.

1. Automatically update internal references: After organizing the directory, you must automatically scan and update the reference links between files within the directory to ensure the accuracy of relative or absolute paths.
2. Update external references on demand: For reference links involving external files (files outside the directory), update them only when the user explicitly requests it.
