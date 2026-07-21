# HYDRA Example 2: Smart MCP Selection (HEAD-2)

## Scenario
A developer wants to inspect a file without loading unnecessary MCP servers (like Database, Git, or Web search tools) that inflate the input token context window.

## Conversation Flow

**User:** `hydra mcp read and edit Python file`

**Agent Response:**
```
=== HYDRA MCP SELECTOR ===
Task type    : File Operations
Needed MCPs  : filesystem (or local hydra-tools-mcp)
Skip MCPs    : database, web-browser, git, vision-tools
Token saving : ~4,500 tokens saved by skipping 4 unused MCP schemas
Action       : Proceeding with minimal tool schema
```

---

**User:** `Can you filter errors from C:\logs\skyrim.log using HYDRA MCP?`

**Agent Response:**
```
Calling tool: hydra_filter_log(file_path="C:\logs\skyrim.log")
Result: Extracted 3 critical lines out of 25,000 total log lines.

Error Summary:
1. L452: Papyrus error - Script missing property 'myProp'
2. L1204: SkyUI conflict - Failed to attach MCM delegate
3. L8901: Memory allocation warning

[Tokens used: 120 input tokens | Tokens saved: ~48,000 tokens]
```

## How It Works
Instead of sending 25,000 lines of logs into the AI's context window (~75,000 tokens), the local HYDRA MCP server filters the log natively on your machine in milliseconds and returns ONLY the 3 lines containing errors.
