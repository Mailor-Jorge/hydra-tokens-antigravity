# @mailoko/hydra-tools-mcp

> Official native Model Context Protocol (MCP) server for **HYDRA TOKENS ANTIGRAVITY** — cutting AI API costs by up to 88% using token optimization tools.

![License](https://img.shields.io/npm/l/@mailoko/hydra-tools-mcp)
![Version](https://img.shields.io/npm/v/@mailoko/hydra-tools-mcp)
![Platform](https://img.shields.io/badge/Platform-Google%20Antigravity%20%7C%20MCP-blue)

---

## ⚡ What is `@mailoko/hydra-tools-mcp`?

This is the native stdio MCP server for the **HYDRA TOKENS ANTIGRAVITY** framework. It processes large log files, estimates token footprints, and manages workspace temporary files **locally on your machine before sending data to the AI model**, saving thousands of input tokens per request.

---

## 🛠️ Available Tools

### 1. `hydra_filter_log`
Filters large log files (e.g. 50,000+ lines) locally in milliseconds, returning ONLY matching error/warning lines to the LLM.
- **Input:** `file_path` (string), `max_lines` (optional int, default 50)
- **Impact:** Reduces input tokens by **up to 99.8%** (sends ~100 tokens instead of 50,000).

### 2. `hydra_token_estimate`
Calculates exact file size in KB, character count, word count, and estimated tokens **before** you load a file into context.
- **Input:** `file_path` (string)
- **Impact:** Prevents accidental context bloat from opening giant files.

### 3. `hydra_clean_scratch`
Scans and cleans up temporary `.tmp`, `.log`, and `.bak` files from the scratch directory to keep the agent workspace clean.
- **Input:** `dry_run` (boolean, default true)

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
