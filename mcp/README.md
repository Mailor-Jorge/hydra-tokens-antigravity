# @mailoko/hydra-tools-mcp

> Official native Model Context Protocol (MCP) server for **HYDRA TOKENS ANTIGRAVITY** — cutting AI API costs by up to 88% using token optimization tools.

![License](https://img.shields.io/npm/l/@mailoko/hydra-tools-mcp)
![Version](https://img.shields.io/npm/v/@mailoko/hydra-tools-mcp)
![Platform](https://img.shields.io/badge/Platform-Google%20Antigravity%20%7C%20MCP-blue)

---

## ⚡ What is `@mailoko/hydra-tools-mcp`?

This is the native stdio MCP server for the **HYDRA TOKENS ANTIGRAVITY** framework. It processes large log files, estimates token footprints, extracts code snippets, caches responses, and scans directories **locally on your machine before sending data to the AI model**, saving thousands of input tokens per request.

---

## 🛠️ Available Tools (6)

### 1. `hydra_filter_log`
Filters large log files locally in milliseconds, returning ONLY matching error/warning lines.
- **Input:** `file_path`, `max_lines` (optional, default 50)
- **Impact:** Up to **99.8%** token reduction.

### 2. `hydra_token_estimate`
Calculates file size, character count, and estimated tokens **before** loading into context.
- **Input:** `file_path`
- **Impact:** Prevents accidental context bloat.

### 3. `hydra_clean_scratch`
Cleans up temporary `.tmp`, `.log`, `.bak` files from the scratch directory.
- **Input:** `dry_run` (boolean, default true)

### 4. `hydra_snippet`
Extracts only a specific function, class, or code block from a file by name.
- **Input:** `file_path`, `symbol`, `context_lines` (optional, default 2)
- **Impact:** Up to **90%** token reduction on file reads.

### 5. `hydra_cache`
Saves, retrieves, or lists cached responses to avoid regenerating repeated answers.
- **Input:** `action` (save/get/list/delete), `key`, `value`
- **Impact:** **100%** reduction on repeated questions (0 generation tokens).

### 6. `hydra_context_snapshot`
Scans a directory and reports estimated token costs per file, sorted by heaviest.
- **Input:** `directory`, `max_depth` (optional), `extensions` (optional)
- **Impact:** Identifies heavy files before loading.

---

## 🚀 Installation & Setup

Add this configuration to your MCP-compatible application (e.g. Google Antigravity IDE `~/.gemini/config/mcp_config.json` or Claude Desktop config):

```json
{
  "mcpServers": {
    "hydra-tools-mcp": {
      "command": "npx",
      "args": ["-y", "@mailoko/hydra-tools-mcp@latest"]
    }
  }
}
```

---

## 🔗 Project Links

- **GitHub Repository:** [Mailor-Jorge/hydra-tokens-antigravity](https://github.com/Mailor-Jorge/hydra-tokens-antigravity)
- **NPM Package:** [@mailoko/hydra-tools-mcp](https://www.npmjs.com/package/@mailoko/hydra-tools-mcp)
- **License:** MIT
