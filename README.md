# 🐍 HYDRA TOKENS ANTIGRAVITY

<div align="center">

![HYDRA Banner](https://img.shields.io/badge/HYDRA-TOKENS%20ANTIGRAVITY-6B21A8?style=for-the-badge&logo=googlegemini&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Google%20Antigravity-4F46E5?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.1.0-F59E0B?style=for-the-badge)
![Skills](https://img.shields.io/badge/Skills-4%20Heads-EC4899?style=for-the-badge)
![MCP Tools](https://img.shields.io/badge/MCP%20Tools-6-06B6D4?style=for-the-badge)

**A modular token-saving system for Google Antigravity IDE.**  
*Cut AI API costs by up to 90% using Skills, Rules, Agents and MCP — the 9-headed HYDRA approach.*

[📦 Install](#-installation) · [📖 Docs](#-architecture) · [🧪 Examples](#-examples) · [🤝 Contribute](#-contributing)

</div>

---

## ⚡ What is HYDRA?

**HYDRA TOKENS ANTIGRAVITY** is a framework of modular Skills, Rules, and MCP configurations designed to **dramatically reduce token consumption** when working with AI agents in the Google Antigravity IDE.

Inspired by the mythological Hydra — where cutting one head makes two grow — this system attacks token waste from **9 different angles (heads)** simultaneously. Each head is an independent, composable module:

| Head | Module | Type | Savings Potential |
|------|--------|------|-------------------|
| 🐍 HEAD-1 | `hydra` | **Skill** | Orchestrator — activates full system |
| 🔌 HEAD-2 | `hydra_mcp` | **Skill** | Smart MCP selector (up to -96% input tokens) |
| 🗜️ HEAD-3 | `hydra_compress` | **Skill** | Semantic context compressor |
| 🔍 HEAD-4 | `hydra_audit` | **Skill** | Token cost auditor |
| 📐 HEAD-5 | `HYDRA_OUTPUT_FORMAT` | **Rule** | Compact output format enforcer |
| 🛡️ HEAD-6 | `HYDRA_CONTEXT_GUARD` | **Rule** | Context saturation monitor |
| 🚫 HEAD-7 | `HYDRA_NO_REPEAT` | **Rule** | Anti-repetition guard |
| 📊 HEAD-8 | `hydra_tracker` | **MCP Config** | Session token usage tracker |
| 🤖 HEAD-9 | `hydra_agent` | **Agent Template** | Minimal system prompt agent |

---

## 📊 Research-Backed Impact

Based on findings from Reddit, GitHub, Medium, machinelearningmastery.com and official AI provider documentation:

| Technique | Source | Potential Savings |
|-----------|--------|------------------|
| Dynamic MCP tool loading | Maxim AI Research | **Up to 96%** of input tokens |
| Prompt caching (static system prompts) | Anthropic / OpenAI docs | **80–90%** on repeated tokens |
| Semantic context compression | Microsoft LLMLingua | **20–80%** reduction |
| Model routing (simple → small model) | Industry benchmark 2025 | **40–70%** cost savings |
| Semantic output caching | Vector DB research | **15–88%** API call reduction |
| Manual prompt optimization | General engineering | **20–50%** reduction |

---

## 📁 Project Structure

```
hydra-tokens-antigravity/
├── README.md                          # This file
├── HYDRA_ARCHITECTURE.md             # Technical architecture diagram
├── INSTALL.md                         # Installation guide
│
├── skills/
│   ├── hydra/SKILL.md                # HEAD-1: Main orchestrator skill
│   ├── hydra_mcp/SKILL.md            # HEAD-2: MCP smart selector skill
│   ├── hydra_compress/SKILL.md       # HEAD-3: Context compressor skill
│   └── hydra_audit/SKILL.md          # HEAD-4: Token audit skill
│
├── rules/
│   └── AGENTS.md                      # HEAD-5,6,7: Global HYDRA rules
│
├── mcp/
│   └── hydra_tracker_config.json     # HEAD-8: Token tracker MCP config
│
├── agents/
│   └── hydra_agent_template.md       # HEAD-9: Optimized agent template
│
└── examples/
    ├── hydra_basic/                   # Basic HYDRA usage
    ├── hydra_mcp_select/              # MCP selection example
    └── hydra_compress_demo/           # Context compression demo
```

---

## 📦 Installation

### Prerequisites
- Google Antigravity IDE installed
- Access to `~/.gemini/config/` directory

### Quick Install (4 skills + rules)

```powershell
# Clone the repository
git clone https://github.com/Mailor-Jorge/hydra-tokens-antigravity.git
cd hydra-tokens-antigravity

# Run the installer script
.\install.ps1
```

### Manual Install

```powershell
# 1. Copy skills to Antigravity config
Copy-Item -Recurse skills\hydra     "$env:USERPROFILE\.gemini\config\skills\hydra"
Copy-Item -Recurse skills\hydra_mcp "$env:USERPROFILE\.gemini\config\skills\hydra_mcp"
Copy-Item -Recurse skills\hydra_compress "$env:USERPROFILE\.gemini\config\skills\hydra_compress"
Copy-Item -Recurse skills\hydra_audit "$env:USERPROFILE\.gemini\config\skills\hydra_audit"

# 2. Append rules to your global AGENTS.md
Add-Content "$env:USERPROFILE\.gemini\config\AGENTS.md" (Get-Content rules\AGENTS.md -Raw)
```

After installation, **restart Antigravity IDE**. The 4 skills will appear in your Customizations panel.

---

## 🚀 Usage

### 🗣️ A. Chat Commands & Triggers

| Command | Action / Description |
|---------|----------------------|
| `hydra`, `/hydra`, `modo hydra` | Activates HYDRA orchestrator and runs **System Scan** |
| `hydra audit`, `quanto custa` | Runs **HEAD-4 Token Auditor** (cost report + efficiency score) |
| `hydra mcp [task]` | Runs **HEAD-2 Smart MCP Selector** (recommends minimal tools) |
| `hydra compress`, `compactar contexto` | Forces **HEAD-3 Semantic Context Compression** immediately |
| `hydra checkpoint` | Saves current session state to `.hydra_checkpoint.json` |
| `hydra snippet [file] [sym]` | Extracts only a specific function/class from a file |
| `hydra cache list/save/get` | Manages response cache (save, retrieve, list) |
| `hydra snapshot [dir]` | Scans directory and reports token costs per file |
| `hydra limit N` | Caps response output to ~N tokens |
| `hydra limit off` | Removes output token limit |
| `hydra diff on/off` | Toggles diff-only mode for file edits (default: ON) |

---

### 🛠️ B. Native MCP Server Tools (`hydra-tools-mcp`) — 6 Tools

Run directly via natural language or MCP tool calls:

| Tool | Parameters | Function & Savings |
|------|------------|--------------------|
| `hydra_filter_log` | `file_path`, `max_lines` | Filters large logs locally, returning only error lines (**-99.8% tokens**) |
| `hydra_token_estimate` | `file_path` | Estimates tokens **before** loading into context |
| `hydra_clean_scratch` | `dry_run` | Cleans `.tmp`, `.log`, `.bak` files from scratch workspace |
| `hydra_snippet` | `file_path`, `symbol` | Extracts a single function/class from file (**-90% tokens**) |
| `hydra_cache` | `action`, `key`, `value` | Saves/retrieves repeated responses (**-100% on repeats**) |
| `hydra_context_snapshot` | `directory`, `max_depth` | Scans dir and reports token cost per file |

#### Natural Language Examples:
- *"Filter errors from `skyrim.log`"* → `hydra_filter_log`
- *"Estimate token cost of `main.py`"* → `hydra_token_estimate`
- *"Extract function OnPageReset from MyMod.psc"* → `hydra_snippet`
- *"Cache this response about compiling Papyrus"* → `hydra_cache`
- *"Scan the project directory for heavy files"* → `hydra_context_snapshot`
---

### 🤖 C. Automatic Behaviors (zero user input required)

These actions run **automatically** during normal chat interaction — no commands needed:

| When | What Happens | Triggered By |
|------|-------------|--------------|
| **Every 10 turns** | `hydra_compress` — compresses conversation history into a semantic digest | HEAD-6 rule |
| **Every 15 turns** | `hydra_context_snapshot` — scans workspace and reports top 5 heaviest files | HEAD-6 rule |
| **Every 20 turns** | Asks: *"Deseja executar `hydra_clean_scratch`?"* to clean temp files | HEAD-6 rule |
| **When reading a file** | Asks: *"Deseja extrair apenas a função X via `hydra_snippet`?"* instead of loading the full file | HEAD-6 snippet-first rule |
| **When topic is repeated** | Silently checks `hydra_cache` — if hit, offers cached answer (0 generation tokens) | HEAD-6 cache-check rule |
| **When editing a file** | Shows **only the diff** (changed lines), never re-outputs the entire file | HEAD-5 diff-only mode |
| **When opening a log file** | Asks: *"Usar `hydra_filter_log` para extrair apenas erros?"* | HEAD-2 interactive protocol |
| **When opening a large file** | Asks: *"Rodar `hydra_token_estimate` primeiro?"* to check token cost before loading | HEAD-2 interactive protocol |
| **Context > 20k tokens** | Emergency compress — immediate context reduction before processing next message | HEAD-6 emergency threshold |

> **Note:** All "Asks" prompts can be answered with yes/no. If you say yes, HYDRA runs the tool automatically. If no, it proceeds normally.

---

You can run `@mailoko/hydra-tools-mcp` locally or register it in any MCP-compatible environment:

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

## 🏗️ Architecture

See [HYDRA_ARCHITECTURE.md](./HYDRA_ARCHITECTURE.md) for the full technical diagram.

```
User Request
     │
     ▼
┌─────────────────────────────────────────┐
│           HEAD-1: hydra (Orchestrator)  │
│  Analyzes request → selects heads       │
└──────┬──────────┬────────────┬──────────┘
       │          │            │
       ▼          ▼            ▼
  HEAD-2       HEAD-3       HEAD-4
  MCP Select   Compress     Audit
       │          │            │
       └──────────┴────────────┘
                  │
       ┌──────────▼──────────┐
       │   HEAD-5,6,7 Rules  │  ← Always active
       │   Format/Guard/NoRep│
       └──────────┬──────────┘
                  │
       ┌──────────▼──────────┐
       │  HEAD-8: MCP Tracker│  ← Monitors usage
       └──────────┬──────────┘
                  │
       ┌──────────▼──────────┐
       │ HEAD-9: Agent Tmpl  │  ← Minimal footprint
       └─────────────────────┘
```

---

## 🧪 Examples

### Example 1: Full HYDRA Mode Session
See [examples/hydra_basic/](./examples/hydra_basic/)

### Example 2: Smart MCP Selection
See [examples/hydra_mcp_select/](./examples/hydra_mcp_select/)

### Example 3: Context Compression Mid-Session
See [examples/hydra_compress_demo/](./examples/hydra_compress_demo/)

---

## 🔬 How Each Head Works

### HEAD-2: Smart MCP Selector
Instead of loading ALL MCP tool definitions (which can consume thousands of tokens), `hydra_mcp` uses a **task-description analysis** to load only the servers relevant to the current work. Research shows this alone can reduce input tokens by up to **96%**.

### HEAD-3: Context Compressor
When a conversation grows long, the agent re-reads the entire history every turn. `hydra_compress` triggers a **semantic digest** — a condensed summary of key decisions, file paths, and current state — replacing raw history with a clean checkpoint.

### HEAD-5–7: Rules Triangle
The three HYDRA rules form a protective triangle:
- **FORMAT** → output stays compact
- **GUARD** → context doesn't balloon
- **NO_REPEAT** → no wasted confirmations

---

## 📈 Token Budget Monitor

The HYDRA system tracks your active customization budget. As seen in Antigravity IDE:
- Rules consume ~4% budget
- Skills consume ~2% budget  
- HYDRA is designed to stay **under 6% total budget** for all 9 heads combined

---

## 🤝 Contributing

Contributions welcome! Each new "head" should:
1. Target a specific token waste source
2. Have a measurable savings metric
3. Be non-breaking (optional activation)
4. Include an example in `examples/`

---

## 📄 License

MIT License — see [LICENSE](./LICENSE) for details.

---

## 🙏 Credits

- Research sources: Reddit r/MachineLearning, Medium, machinelearningmastery.com, getmaxim.ai, stackone.com
- Built for [Google Antigravity IDE](https://antigravity.google)
- Inspired by the Hydra of Lerna — because token waste has many heads

---

<div align="center">

**HYDRA TOKENS ANTIGRAVITY** — *Every token saved is a battle won.*

Made with 🐍 by [@Mailor-Jorge](https://github.com/Mailor-Jorge)

</div>
