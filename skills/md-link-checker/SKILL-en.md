---
name: "md-link-checker"
description: "Check the validity of local and external links in Markdown files. Invoke this skill when the user needs to verify or check the accessibility of links in Markdown documents or projects."
---

# Markdown Link Checker (md-link-checker)

The Markdown link checker skill relies on the `scripts/check_links.py` script in this skill directory to verify the connectivity of local file paths and external network URLs in Markdown text. It is compatible with standard Markdown syntax and HTML image tags, and includes an automatic retry mechanism to handle anti-scraping policies.

## Use Cases

Depending on the user's troubleshooting needs, this skill covers single-file targeted checks, directory-level batch scans, and project-wide deep inspections to ensure the accuracy of external links and internal references in documents. Troubleshooting tasks typically include the following dimensions:

- Verify the link connectivity of a specific Markdown file;
- Batch scan the link validity of all Markdown files under a specified directory;
- Globally inspect the external network addresses or local relative paths in all Markdown files in the project.

## Execution Guide

Invoke the Python script directly from the terminal to launch an automated check. The script dynamically adjusts the check scope and target link types based on the arguments passed.

### Parameters

The script provides a flexible parameter interface for precise control over check targets and strategies. The detailed parameters are shown in the table below:

| Parameter | Short | Options                   | Default           | Description                                                        |
| --------- | ----- | ------------------------- | ----------------- | ------------------------------------------------------------------ |
| `--file`  | `-f`  | File path                 | Project `README.md` | Specifies the path of the single Markdown file to check.           |
| `--dir`   | `-d`  | Directory path            | None              | Recursively checks all Markdown files in the specified directory and its subdirectories. |
| `--all`   | `-a`  | None                      | No                | Checks all Markdown files in the project.                          |
| `--type`  | `-t`  | `local`, `external`, `all` | `local`           | Specifies the link types to check.                                 |

### Common Command Examples

For common troubleshooting tasks, use the following standard command combinations to quickly start the check:

```bash
# Note: Before executing commands, the LLM must first confirm the absolute path of this skill directory using a file-path tool, and replace <SKILL_DIR> with it.

# Check all links in a single file
python3 <SKILL_DIR>/scripts/check_links.py -f path/to/file.md -t all

# Check local links in a specific directory
python3 <SKILL_DIR>/scripts/check_links.py -d docs

# Check all links in the project
python3 <SKILL_DIR>/scripts/check_links.py -a -t all

# Check only external network links in the project
python3 <SKILL_DIR>/scripts/check_links.py -a -t external
```

## Notes

When running checks, pay attention to where the check report is generated and the tool's compatibility with special usage. The notes are as follows:

- After the script finishes, the detailed check results are printed directly to the console. To save the log, redirect the output to a file (e.g., append `> link_check_report.txt`) either via the model or manually by the user.
- The link parser supports not only standard Markdown links but also the `src` attribute of HTML `<img>` tags.
- For probing external network resources, built-in fault tolerance and retry logic handles status codes such as 403 and 404 to reduce false positives.
