import { readFileSync } from "node:fs";
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

function main() {
  const artifact = process.argv[2] || "./evals/artifacts/test-01.jsonl";
  const outReport = process.argv[3] || "./evals/reports/usage.md";
  const text = readFileSync(artifact, "utf8");
  const usage = {};
  const lines = text.split("\n").filter(Boolean);
  let provider = "";
  let model = "";
  for (const line of lines) {
    const m1 = line.match(/input[_\s]?tokens[:=]\s*(\d+)/i);
    const m2 = line.match(/output[_\s]?tokens[:=]\s*(\d+)/i);
    const m3 = line.match(/total[_\s]?tokens[:=]\s*(\d+)/i);
    const m4 = line.match(/cost[:=]\s*\$?([\d.]+)/i);
    if (m1) usage.input_tokens = Number(m1[1]);
    if (m2) usage.output_tokens = Number(m2[1]);
    if (m3) usage.total_tokens = Number(m3[1]);
    if (m4) usage.cost = Number(m4[1]);
    try {
      const obj = JSON.parse(line);
      const u = obj?.usage || obj?.data?.usage;
      if (u) {
        if (typeof u.input_tokens === "number") usage.input_tokens = u.input_tokens;
        if (typeof u.output_tokens === "number") usage.output_tokens = u.output_tokens;
        if (typeof u.total_tokens === "number") usage.total_tokens = u.total_tokens;
        if (typeof u.cost === "number") usage.cost = u.cost;
      }
      const p = obj?.part;
      if (p?.tokens) {
        if (typeof p.tokens.input === "number") usage.input_tokens = p.tokens.input;
        if (typeof p.tokens.output === "number") usage.output_tokens = p.tokens.output;
        if (typeof p.tokens.total === "number") usage.total_tokens = p.tokens.total;
        if (typeof p.tokens.reasoning === "number") usage.reasoning_tokens = p.tokens.reasoning;
        if (p.tokens.cache) {
          if (typeof p.tokens.cache.read === "number") usage.cache_read_tokens = p.tokens.cache.read;
          if (typeof p.tokens.cache.write === "number") usage.cache_write_tokens = p.tokens.cache.write;
        }
      }
      if (typeof p?.cost === "number") {
        usage.cost = p.cost;
      }
    } catch {}
    if (!provider || !model) {
      const mp = line.match(/providerID=([a-z0-9-]+)/i);
      const mm = line.match(/modelID=([a-z0-9._-]+)/i);
      if (mp) provider = mp[1];
      if (mm) model = mm[1];
    }
  }
  const found = Object.keys(usage).length > 0;
  const result = { found, usage, provider, model, artifact };
  console.log(JSON.stringify(result, null, 2));

  try {
    const dir = path.dirname(outReport);
    mkdirSync(dir, { recursive: true });
    const title = "LLM 用量与成本报告";
    const linesOut = [];
    linesOut.push(`# ${title}`);
    linesOut.push("");
    linesOut.push("1. 概述");
    linesOut.push("");
    linesOut.push(`- 数据来源：${artifact}`);
    if (provider) linesOut.push(`- 推理提供方：${provider}`);
    if (model) linesOut.push(`- 模型：${model}`);
    linesOut.push("- 解析方法：从会话结束事件与追加统计文本中提取 tokens 与 cost 字段");
    linesOut.push("");
    linesOut.push("2. 用量数据");
    linesOut.push("");
    linesOut.push("| 指标 | 数值 |");
    linesOut.push("| --- | --- |");
    linesOut.push(`| 输入 tokens | ${usage.input_tokens ?? "-"} |`);
    linesOut.push(`| 输出 tokens | ${usage.output_tokens ?? "-"} |`);
    if (usage.cache_read_tokens !== undefined || usage.cache_write_tokens !== undefined) {
      linesOut.push(`| 缓存读取 tokens | ${usage.cache_read_tokens ?? 0} |`);
      linesOut.push(`| 缓存写入 tokens | ${usage.cache_write_tokens ?? 0} |`);
    }
    if (usage.reasoning_tokens !== undefined) {
      linesOut.push(`| 推理 tokens | ${usage.reasoning_tokens ?? 0} |`);
    }
    linesOut.push(`| 总计 tokens | ${usage.total_tokens ?? "-"} |`);
    linesOut.push(`| 费用 | ${usage.cost ?? "-"} |`);
    linesOut.push("");
    linesOut.push("3. 复现命令");
    linesOut.push("");
    linesOut.push("```bash");
    linesOut.push("# 生成本报告");
    const filePath = new URL(import.meta.url).pathname;
    linesOut.push(`node ${path.relative(process.cwd(), filePath)} "${artifact}" "${outReport}"`);
    linesOut.push("```");
    linesOut.push("");
    linesOut.push("4. 备注");
    linesOut.push("");
    linesOut.push("- 若使用的 Agent 输出为非结构化文本，本报告将仅记录可解析到的字段。");
    writeFileSync(outReport, linesOut.join("\n"), "utf8");
  } catch {}
}

main();
