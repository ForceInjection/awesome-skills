import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

function readText(p) {
  return readFileSync(p, "utf8");
}

function splitReports(text) {
  const lines = text.split("\n");
  const blocks = [];
  let current = null;
  for (const line of lines) {
    const m = line.match(/^##\s*评审结果\s*-\s*(?:\[(.+?)\]|(.+))\s*$/);
    if (m) {
      if (current) blocks.push(current);
      const type = m[1] || m[2] || "";
      current = { type, content: [line] };
    } else if (current) {
      current.content.push(line);
    }
  }
  if (current) blocks.push(current);
  return blocks;
}

function normalizeName(t) {
  if (/大纲/.test(t)) return "outline";
  if (/内容/.test(t)) return "content";
  if (/资产/.test(t) || /链接/.test(t)) return "assets";
  if (/格式/.test(t)) return "format";
  return t.replace(/\s+/g, "-").toLowerCase();
}

function extractTextFromJsonl(text) {
  const out = [];
  for (const line of text.split("\n").filter(Boolean)) {
    try {
      const obj = JSON.parse(line);
      const msg =
        obj?.message?.text ||
        obj?.text ||
        obj?.data?.text ||
        obj?.part?.text ||
        null;
      if (typeof msg === "string") out.push(msg);
      else if (Array.isArray(obj?.message?.content)) {
        for (const c of obj.message.content) {
          if (c?.type === "text" && typeof c?.text === "string") out.push(c.text);
        }
      }
    } catch {
      // ignore
    }
  }
  return out.join("\n");
}

function main() {
  const artifact = process.argv[2] || "./evals/artifacts/test-01.jsonl";
  const outDir = process.argv[3] || "./evals/reports";
  const raw = readText(artifact);
  const extracted = extractTextFromJsonl(raw);
  const payload = extracted && extracted.trim().length > 0 ? extracted : raw;
  const blocks = splitReports(payload);
  mkdirSync(outDir, { recursive: true });
  const written = [];
  for (const b of blocks) {
    const name = normalizeName(b.type);
    const p = path.join(outDir, `${name}.md`);
    writeFileSync(p, b.content.join("\n"), "utf8");
    written.push(p);
  }
  const result = { reports: written, count: written.length };
  console.log(JSON.stringify(result, null, 2));
}

main();
