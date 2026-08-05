# CLI Command Quick Reference

This file provides a cheat sheet of common operations for the OpenSpec native command-line tool.

When low-level management is needed, run the following native commands (ordered by lifecycle):

- **Install**: `npm install -g @fission-ai/openspec@latest`
- **Initialize**: `openspec init [path]` - Initialize a project.
- **Update instructions**: `openspec update [path]` - Update the OpenSpec AI collaboration instruction files.
- **Create a change**: `openspec new change <name>` - Create a new change proposal.
- **Validate specs**: `openspec validate [item-name]` - Validate the format of changes and spec documents.
- **View status**: `openspec status` - Show the completion status of change artifacts.
- **Show details**: `openspec show [item-name]` - Show detailed information for a change or spec.
- **List items**: `openspec list` - List all changes by default (use `--specs` to list specs).
- **Interactive dashboard**: `openspec view` - Open an interactive dashboard to view specs and changes.
- **Archive a change**: `openspec archive [change-name]` - Archive a completed change and merge it into the main spec.
- **Get instructions**: `openspec instructions [artifact]` - Output enhanced instructions for creating artifacts or applying tasks.
- **Manage config**: `openspec config` - View and modify global configuration.
