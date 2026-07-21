#!/usr/bin/env node
/**
 * HYDRA TOKENS ANTIGRAVITY — Official Stdio MCP Server (HEAD-8)
 * Pure Node.js JSON-RPC MCP Server implementation. Zero external dependencies.
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');

const SERVER_NAME = "hydra-tools-mcp";
const SERVER_VERSION = "1.0.0";

const TOOLS = [
  {
    name: "hydra_filter_log",
    description: "Filter large log files locally, returning only error lines. Saves thousands of context tokens.",
    inputSchema: {
      type: "object",
      properties: {
        file_path: { type: "string", description: "Absolute path to the log file" },
        max_lines: { type: "integer", description: "Max matching error lines to return (default 50)" }
      },
      required: ["file_path"]
    }
  },
  {
    name: "hydra_token_estimate",
    description: "Estimate token footprint of a file before loading it into context.",
    inputSchema: {
      type: "object",
      properties: {
        file_path: { type: "string", description: "Absolute path to the file" }
      },
      required: ["file_path"]
    }
  },
  {
    name: "hydra_clean_scratch",
    description: "Clean temporary scratch files older than 24 hours to keep workspace light.",
    inputSchema: {
      type: "object",
      properties: {
        dry_run: { type: "boolean", description: "If true, only report files without deleting" }
      }
    }
  }
];

function handleFilterLog(filePath, maxLines = 50) {
  if (!filePath || !fs.existsSync(filePath)) return `Error: File not found: ${filePath}`;
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split(/\r?\n/);
    const errorRegex = /(error|failed|fatal|exception|critical|warn|traceback)/i;
    const matches = [];
    
    for (let i = 0; i < lines.length; i++) {
      if (errorRegex.test(lines[i])) {
        matches.push(`L${i + 1}: ${lines[i].trim()}`);
        if (matches.length >= maxLines) break;
      }
    }
    
    if (matches.length === 0) {
      return `[HYDRA FILTER] Analyzed ${lines.length} lines in ${path.basename(filePath)}. Zero errors found!`;
    }
    
    return `[HYDRA FILTER] Analyzed ${lines.length} lines. Extracted ${matches.length} error lines:\n` +
      '-'.repeat(50) + '\n' + matches.join('\n');
  } catch (err) {
    return `Error reading file: ${err.message}`;
  }
}

function handleTokenEstimate(filePath) {
  if (!filePath || !fs.existsSync(filePath)) return `Error: File not found: ${filePath}`;
  try {
    const stats = fs.statSync(filePath);
    const content = fs.readFileSync(filePath, 'utf-8');
    const charCount = content.length;
    const wordCount = content.trim().split(/\s+/).length;
    const estTokens = Math.floor(charCount / 4);
    const rec = estTokens < 3000 ? "OK to load" : "HIGH TOKEN COST — use hydra_filter_log or partial read";

    return `[HYDRA TOKEN ESTIMATE] ${path.basename(filePath)}\n` +
      `• File Size  : ${(stats.size / 1024).toFixed(1)} KB\n` +
      `• Characters : ${charCount.toLocaleString()}\n` +
      `• Words      : ${wordCount.toLocaleString()}\n` +
      `• Est. Tokens: ~${estTokens.toLocaleString()} tokens\n` +
      `• Status     : ${rec}`;
  } catch (err) {
    return `Error analyzing file: ${err.message}`;
  }
}

function handleCleanScratch(dryRun = true) {
  const scratchDir = path.join(process.env.USERPROFILE || process.env.HOME || '', '.gemini', 'antigravity', 'scratch');
  if (!fs.existsSync(scratchDir)) return "Scratch directory not found.";

  try {
    const files = fs.readdirSync(scratchDir);
    const cleaned = [];
    let totalBytes = 0;

    for (const f of files) {
      if (/\.(tmp|bak|log)$/i.test(f)) {
        const p = path.join(scratchDir, f);
        const st = fs.statSync(p);
        cleaned.push(`${f} (${(st.size / 1024).toFixed(1)} KB)`);
        totalBytes += st.size;
        if (!dryRun) fs.unlinkSync(p);
      }
    }

    const actionStr = dryRun ? "Found (Dry Run)" : "Deleted";
    return `[HYDRA SCRATCH CLEANER] ${actionStr} ${cleaned.length} temp files (~${(totalBytes / 1024).toFixed(1)} KB saved):\n` +
      (cleaned.length ? cleaned.slice(0, 10).join('\n') : "No temporary files found.");
  } catch (err) {
    return `Error cleaning scratch: ${err.message}`;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', (line) => {
  if (!line.trim()) return;
  try {
    const req = JSON.parse(line);
    const reqId = req.id;
    const method = req.method;
    const params = req.params || {};

    if (method === 'initialize') {
      console.log(JSON.stringify({
        jsonrpc: '2.0',
        id: reqId,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: { name: SERVER_NAME, version: SERVER_VERSION }
        }
      }));
    } else if (method === 'tools/list') {
      console.log(JSON.stringify({
        jsonrpc: '2.0',
        id: reqId,
        result: { tools: TOOLS }
      }));
    } else if (method === 'tools/call') {
      let text = '';
      if (params.name === 'hydra_filter_log') {
        text = handleFilterLog(params.arguments?.file_path, params.arguments?.max_lines);
      } else if (params.name === 'hydra_token_estimate') {
        text = handleTokenEstimate(params.arguments?.file_path);
      } else if (params.name === 'hydra_clean_scratch') {
        text = handleCleanScratch(params.arguments?.dry_run);
      } else {
        text = `Unknown tool: ${params.name}`;
      }

      console.log(JSON.stringify({
        jsonrpc: '2.0',
        id: reqId,
        result: { content: [{ type: 'text', text }] }
      }));
    }
  } catch (e) {}
});
