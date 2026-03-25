import { readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { existsSync as fsExistsSync, readFileSync as fsReadFileSync } from "node:fs";

function parseJsonl(jsonlText) {
  const out = [];
  for (const line of jsonlText.split("\n").filter(Boolean)) {
    try {
      out.push(JSON.parse(line));
    } catch {
      // skip non-JSON lines
    }
  }
  return out;
}

function checkMdTranslatorOutput(inputPath) {
  const dir = path.dirname(inputPath);
  const base = path.basename(inputPath, ".md");
  const candidates = [
    path.join(dir, `${base}.zh.md`),
    path.join(dir, `${base}_zh.md`),
    path.join(dir, `${base}-zh.md`),
  ];
  const existing = candidates.find((p) => fsExistsSync(p));
  const outputExists = Boolean(existing);
  let preservesImageLinks = false;
  let preservesCodeBlocks = false;
  let outputIsMarkdown = false;
  if (existing) {
    const txt = fsReadFileSync(existing, "utf8");
    outputIsMarkdown = existing.endsWith(".md");
    preservesImageLinks = /!\[[^\]]*\]\(img\/diagram\.png\)/.test(txt);
    preservesCodeBlocks = /```[a-zA-Z0-9]*[\s\S]*?```/.test(txt);
  }
  const results = { outputExists, outputIsMarkdown, preservesImageLinks, preservesCodeBlocks };
  const score =
    Object.values(results).reduce((acc, v) => acc + (v ? 1 : 0), 0) / Object.keys(results).length;
  return { checks: results, score, overall_pass: score === 1 };
}

function checkDocReviewerReports(reportsDir) {
  const required = ["outline.md", "content.md", "assets.md", "format.md"];
  const results = {};

  required.forEach((f) => {
    const p = path.join(reportsDir, f);
    const key = `has${f.replace(".md", "").charAt(0).toUpperCase()}${f.replace(".md", "").slice(1)}`;
    results[key] = fsExistsSync(p);
  });

  let structureOk = true;
  for (const f of required) {
    const p = path.join(reportsDir, f);
    if (fsExistsSync(p)) {
      const content = fsReadFileSync(p, "utf8");
      if (!content.includes("## 评审结果") || !content.includes("### 发现的问题")) {
        structureOk = false;
        break;
      }
    }
  }
  results.structureOk = structureOk;

  const score = Object.values(results).reduce((acc, v) => acc + (v ? 1 : 0), 0) / Object.keys(results).length;
  return { checks: results, score, overall_pass: score === 1 };
}

function main() {
  const artifact = process.argv[2] || "./evals/artifacts/test-01.jsonl";
  const secondaryArg = process.argv[3];
  const skill = process.env.SKILL || "doc-reviewer";

  if (skill === "md-translator") {
    const inputPath = secondaryArg;
    if (!inputPath || !fsExistsSync(inputPath)) {
      console.error(JSON.stringify({ error: "missing-or-invalid-input-path", path: inputPath }));
      process.exit(1);
    }
    const result = checkMdTranslatorOutput(inputPath);
    console.log(JSON.stringify(result, null, 2));
    if (!result.overall_pass) process.exit(1);
  } else {
    // 默认或 doc-reviewer 行为
    const reportsDir = secondaryArg || "./evals/reports/doc-reviewer";
    if (!fsExistsSync(reportsDir)) {
      console.error(JSON.stringify({ error: "reports-dir-not-found", path: reportsDir }));
      process.exit(1);
    }
    const result = checkDocReviewerReports(reportsDir);
    console.log(JSON.stringify(result, null, 2));
    if (!result.overall_pass) process.exit(1);
  }
}

main();
