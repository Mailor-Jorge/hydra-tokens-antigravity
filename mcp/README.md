# @mailoko/hydra-tools-mcp

> Official native Model Context Protocol (MCP) server for **HYDRA TOKENS ANTIGRAVITY** — cutting AI API costs by up to 90% using local token optimization tools.

![License](https://img.shields.io/npm/l/@mailoko/hydra-tools-mcp?style=for-the-badge)
![Version](https://img.shields.io/npm/v/@mailoko/hydra-tools-mcp?style=for-the-badge&color=orange)
![Platform](https://img.shields.io/badge/Platform-Google%20Antigravity%20%7C%20MCP-blue?style=for-the-badge)
![Downloads](https://img.shields.io/npm/dm/@mailoko/hydra-tools-mcp?style=for-the-badge&color=green)

---

## ⚡ What is `@mailoko/hydra-tools-mcp`?

`@mailoko/hydra-tools-mcp` is a zero-dependency, local stdio MCP server for Google Antigravity IDE and any MCP-compatible client. It processes heavy operations — log filtering, snippet extraction, token estimation, context snapshots, and response caching — **locally on your machine before sending data to the AI model**, saving thousands of input and generation tokens per request.

---

## 🛠️ Available Tools (6)

### 1. `hydra_filter_log`
Filters large log files locally in milliseconds, returning ONLY matching error/warning lines.
- **Inputs:**
  - `file_path` (string, required): Absolute path to the log file.
  - `max_lines` (number, optional): Max error lines to return (default: `50`).
- **Impact:** Up to **99.8%** token reduction on log inspection.

### 2. `hydra_token_estimate`
Calculates file size, character count, and estimated tokens **before** loading a file into context.
- **Inputs:**
  - `file_path` (string, required): Absolute path to the file.
- **Impact:** Prevents accidental context bloat from opening massive files.

### 3. `hydra_clean_scratch`
Scans and cleans up temporary `.tmp`, `.log`, and `.bak` files from the scratch directory.
- **Inputs:**
  - `dry_run` (boolean, optional): If `true`, only reports files without deleting (default: `true`).
- **Impact:** Keeps workspace clean and light.

### 4. `hydra_snippet`
Extracts only a specific function, class, or code block from a file by name.
- **Inputs:**
  - `file_path` (string, required): Absolute path to the source file.
  - `symbol` (string, required): Name of function, class, event, or state to extract.
  - `context_lines` (number, optional): Extra lines of context above/below (default: `2`).
- **Impact:** Up to **90%** token reduction on file reads.

### 5. `hydra_cache`
Saves, retrieves, or lists cached responses to avoid regenerating repeated answers.
- **Inputs:**
  - `action` (string, required): `"save"`, `"get"`, `"list"`, or `"delete"`.
  - `key` (string, optional): Cache key or question topic.
  - `value` (string, optional): Content to cache (required for `"save"`).
- **Impact:** **100%** reduction on repeated questions (0 generation tokens).

### 6. `hydra_context_snapshot`
Scans a directory and reports estimated token costs per file, sorted by heaviest.
- **Inputs:**
  - `directory` (string, required): Absolute path to directory to scan.
  - `max_depth` (number, optional): Max directory depth (default: `2`).
  - `extensions` (string, optional): Comma-separated extension filter (e.g. `".py,.md,.psc"`).
- **Impact:** Identifies heavy files before loading.

---

## 🤖 Automatic Triggers (HYDRA Integration)

When used alongside **HYDRA TOKENS ANTIGRAVITY** rules & skills, these tools trigger automatically during chat interactions:

| Trigger Event | Automated Action | Tool Used |
|---------------|------------------|-----------|
| **Every 15 turns** | Workspace token scan (top 5 heaviest files) | `hydra_context_snapshot` |
| **Every 20 turns** | Prompt to clean scratch workspace | `hydra_clean_scratch` |
| **Opening a file** | Prompts to extract single function instead of full read | `hydra_snippet` |
| **Opening a log** | Prompts to filter error lines locally | `hydra_filter_log` |
| **Opening heavy file** | Prompts for token cost estimate before load | `hydra_token_estimate` |
| **Repeated query** | Checks local cache for instant 0-token answer | `hydra_cache` |

---

## 🚀 Installation & Setup

Add this configuration to your MCP settings file (e.g., Google Antigravity `~/.gemini/config/mcp_config.json` or Claude Desktop `claude_desktop_config.json`):

### Option A: NPX (Recommended)

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

### Option B: Local Python Script

```json
{
  "mcpServers": {
    "hydra-tools-mcp": {
      "command": "python",
      "args": ["C:\\Users\\YourUsername\\.gemini\\config\\hydra_mcp_server.py"]
    }
  }
}
```

---

## 🔗 Project Links

- **GitHub Repository:** [Mailor-Jorge/hydra-tokens-antigravity](https://github.com/Mailor-Jorge/hydra-tokens-antigravity)
- **Walkthrough Guide:** [WALKTHROUGH.md](https://github.com/Mailor-Jorge/hydra-tokens-antigravity/blob/main/WALKTHROUGH.md)
- **NPM Package:** [@mailoko/hydra-tools-mcp](https://www.npmjs.com/package/@mailoko/hydra-tools-mcp)
- **License:** MIT
