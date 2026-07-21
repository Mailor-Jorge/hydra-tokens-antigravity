---
name: hydra_mcp
description: >
  HYDRA HEAD-2: Smart MCP server selector. Analyzes the current task and loads ONLY the
  MCP tool definitions needed, dramatically reducing input token overhead from unused tool
  schemas. Research shows dynamic MCP loading can reduce input tokens by up to 96%.
  Trigger with 'hydra mcp', 'qual mcp usar', 'selecionar mcp', 'mcp selector'.
---

# HYDRA TOKENS ANTIGRAVITY — HEAD-2: Smart MCP Selector

## The Problem
Every MCP server loaded into context injects its full tool schema (names, descriptions,
parameter definitions) into the model's input tokens — EVEN if you never use those tools.
A typical MCP server can add 500–3,000 tokens per session.

**Loading 5 unnecessary MCP servers = ~5,000–15,000 wasted input tokens per request.**

---

## Activation Phrases
- `hydra mcp [task description]`
- `qual mcp usar`, `selecionar mcp`
- `mcp selector`, `mcp otimizar`

---

## Upon Activation: MCP Analysis Protocol

When activated, perform this analysis:

### Step 1 — Task Classification
Classify the current task into one of these categories:

| Category | Keywords | Recommended MCP Servers |
|----------|----------|------------------------|
| **File Operations** | read, write, edit, create file | filesystem only |
| **Web Research** | search, browse, fetch URL | web/browser only |
| **Code Execution** | run, execute, test, compile | shell/terminal only |
| **Database** | query, SQL, database, records | database only |
| **Version Control** | git, commit, push, branch | git only |
| **AI/Model Tasks** | generate, classify, embed | model-specific only |
| **No External Data** | explain, analyze existing, review | NONE — use context only |

### Step 2 — Report and Recommend
Output a compact MCP recommendation:
```
=== HYDRA MCP SELECTOR ===
Task type    : [detected category]
Needed MCPs  : [list only required servers]
Skip MCPs    : [list servers to avoid loading]
Token saving : ~X tokens saved by not loading [skipped servers]
Action       : Proceed with minimal MCP set
```

---

## MCP Schema Optimization Rules

### Rule MCP-1: Strip Unnecessary Descriptions
When configuring MCP servers, use the minimal schema pattern:
- Keep: function name, required parameters, parameter types
- Remove: verbose descriptions, optional examples, nested metadata

**Bloated schema (HIGH COST):**
```json
{
  "name": "read_file",
  "description": "Reads the content of a file from the filesystem. This tool allows you to access any file that the user has granted permission to read. It returns the raw content of the file as a string. Use this when you need to examine existing code...",
  "parameters": { ... }
}
```

**Optimized schema (LOW COST):**
```json
{
  "name": "read_file",
  "description": "Read file content.",
  "parameters": { "path": { "type": "string" } }
}
```

### Rule MCP-2: Batch Tool Calls
Instead of sequential calls, batch related operations:
```
✅ Read 5 files in one call → process together
❌ Read file 1 → respond → read file 2 → respond → ...
```

### Rule MCP-3: Code-Execute-Summary Pattern
For large data processing tasks, instead of reading raw data into context:
1. Write a small script to process the data
2. Execute the script
3. Return only the summary/result

This keeps raw data OUT of the context window entirely.

### Rule MCP-4: Tool Result Compression
When an MCP tool returns a large response:
- Extract ONLY the fields needed for the current task
- Discard metadata, timestamps, and unrelated fields
- If the result is >1,000 tokens, summarize before passing to main context

---

## MCP Token Cost Reference Table

| MCP Server Type | Approx Schema Tokens | Load if... |
|----------------|---------------------|------------|
| Filesystem tools | ~300–500 | Task involves files |
| Web/Browser tools | ~400–700 | Task requires URL fetching |
| Shell/Terminal | ~200–300 | Task requires code execution |
| Database tools | ~500–1,000 | Task involves data queries |
| Git tools | ~300–600 | Task involves version control |
| Image/Vision tools | ~400–800 | Task involves images |
| Custom/Complex MCP | ~1,000–3,000 | Only when explicitly needed |

**Target: Load ≤2 MCP server types per task session.**

---

## Interactive User Confirmation Protocol

Whenever the user asks to analyze a log file, inspect a potentially large file, or do workspace cleanup:
**DO NOT read the raw file immediately.** Ask the user if they want to use a HYDRA MCP tool first:

1. **Log Analysis:**
   > *"Detectei o arquivo `[filename.log]`. Deseja usar `hydra_filter_log` para extrair apenas as linhas de erro locais (economizando ~99% de tokens) antes de abrir o arquivo inteiro?"*

2. **Large File Inspection:**
   > *"O arquivo `[filename.ext]` pode consumir muitos tokens. Deseja rodar `hydra_token_estimate` primeiro para ver a estimativa de custo de tokens e tamanho em KB?"*

3. **Workspace Cleanup:**
   > *"Deseja executar `hydra_clean_scratch` para listar/limpar arquivos temporários `.tmp`, `.log` e `.bak` do workspace?"*

4. **Function/Block Reading (AUTOMATIC):**
   When user asks to read or analyze a specific function/class/event in a file:
   > *"Deseja que eu extraia apenas a função `[symbol]` via `hydra_snippet` em vez de carregar o arquivo inteiro (~X tokens)?"*

5. **Repeated Topic Detection (AUTOMATIC):**
   When user asks about a topic that may have been answered before:
   - Silently check `hydra_cache(action='get', key='topic')` first.
   - If cache hit: *"Encontrei uma resposta cacheada para este tópico. Deseja usar o cache (0 tokens de geração) ou gerar uma resposta nova?"*
   - If cache miss: generate normally, then offer to cache: *"Deseja salvar esta resposta no cache para reutilização futura?"*

7. **Dependency Trace (AUTOMATIC before editing a symbol):**
   Before modifying a function, class, or event:
   > *"Vou editar a função `[symbol]`. Deseja executar `hydra_dependency_trace` primeiro para verificar se outras partes do código dependem dela e evitar quebras?"*

8. **Post-Edit Verification (AUTOMATIC after editing a file):**
   After making edits to any code file:
   > *"Editei o arquivo `[filename]`. Deseja executar `hydra_edit_verify` para verificar se há erros de sintaxe ou blocos não fechados?"*

9. **File Hash Re-read Prevention (AUTOMATIC before re-reading):**
   Before loading a file that was previously read in context:
   > *"Deseja verificar via `hydra_file_hash` se `[filename]` realmente mudou antes de reler (~X tokens)?"*

---

## Quick Commands

```
hydra mcp off              → Suggest disabling all non-essential MCP servers
hydra mcp report           → Show estimated token cost of all currently loaded MCPs
hydra mcp task: [desc]     → Get MCP recommendation for specific task description
hydra snippet [file] [sym] → Extract only a specific function/class from file
hydra trace [file] [sym]   → Trace callers/dependencies of symbol across project
hydra verify [file]        → Run post-edit syntax check on file
hydra hash [file]          → Check if file content changed (MD5)
hydra cache list/save/get  → Manage response cache
hydra snapshot [dir]       → Scan directory and report token costs per file
hydra limit N              → Cap response output to ~N tokens
hydra limit off            → Remove output token limit
hydra diff on/off          → Toggle diff-only mode for file edits (default: ON)
```

