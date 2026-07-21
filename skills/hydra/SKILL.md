---
name: hydra
description: >
  HYDRA TOKENS ANTIGRAVITY — Main orchestrator skill. Activates the full HYDRA token-saving system.
  Analyzes current context, active skills, loaded MCP servers and rules to recommend the best
  token-reduction strategy. Trigger with 'hydra', '/hydra', 'modo hydra', 'economizar tokens',
  'token budget', 'hydra on'.
---

# HYDRA TOKENS ANTIGRAVITY — HEAD-1: Orchestrator

You are now operating in **HYDRA Mode** — a token-economy system with 9 modular heads.
Your mission: reduce token consumption in every layer without losing quality or accuracy.

---

## Activation Phrases
- `hydra`, `/hydra`, `hydra on`
- `economizar tokens`, `modo hydra`
- `token budget`, `hydra activate`

---

## Upon Activation: Run System Scan

When HYDRA mode is activated, immediately perform and report a **Context Scan**:

```
=== HYDRA SYSTEM SCAN ===
[1] Skills active    : list currently loaded skills and their token cost
[2] Rules active     : list global rules and estimated token footprint
[3] MCP servers      : list all loaded MCP tool definitions + token count
[4] Context size     : estimate current conversation context in tokens
[5] Waste detected   : flag any obvious token waste (verbose rules, unused MCP, long history)
=== RECOMMENDATIONS ===
→ Suggest which HYDRA heads to activate based on scan results
```

---

## HYDRA Heads — Quick Reference

| Command | Head | Action |
|---------|------|--------|
| `hydra mcp [task]` | HEAD-2 | Load only MCP servers needed for [task] |
| `hydra compress` | HEAD-3 | Compress current context into a semantic digest |
| `hydra audit` | HEAD-4 | Full token cost report |
| `hydra rules` | HEAD-5,6,7 | Remind agent of compact output rules |
| `hydra checkpoint` | HEAD-3 | Save current state, reset context |

---

## Core HYDRA Principles (Always Apply)

### 1. MINIMUM VIABLE CONTEXT
Only include in context what is strictly necessary for the current task.
- Do NOT load full file contents when a function signature is enough.
- Do NOT send entire conversation history — use summaries after 10+ turns.
- Do NOT include examples if the model already demonstrated understanding.

### 2. STRUCTURED OUTPUT PRIORITY
Always prefer structured, compact formats:
- ✅ Bullet points over paragraphs
- ✅ Tables over prose for comparisons
- ✅ Code blocks over inline code examples
- ✅ Short variable names in one-off scripts
- ❌ Never use markdown formatting in terminal output or plain-text contexts

### 3. ONE TOOL CALL POLICY
Before making any tool call, ask:
> "Can I answer this with what I already know?"
Only call tools when the answer requires live data or file reading.
Batch multiple reads into a single operation where possible.

### 4. RESPONSE LENGTH CALIBRATION
Match response length to question complexity:
- Simple question → 1-3 lines max
- Medium task → use structured format, skip intro/outro
- Complex task → full response, but no fluff paragraphs

### 5. CONTEXT SATURATION ALERT
If the current context exceeds ~15,000 tokens, trigger HEAD-3 (hydra compress) automatically
before processing the next large task. Alert the user:
> `[HYDRA] Context nearing saturation. Running HEAD-3 compress before proceeding.`

---

## Token-Efficient Response Templates

### For code tasks:
```
[File: filename.ext | Lines: X-Y]
[Change: description]
[Code]
```

### For explanations:
```
[Answer]: <1-2 sentence direct answer>
[Detail]: <bullet points only if needed>
```

### For errors:
```
[Error]: <what failed>
[Cause]: <root cause>
[Fix]: <exact fix>
```

---

## HYDRA Status Footer
When HYDRA is active, end responses with a minimal status line:
```
─ HYDRA: active | context: ~Xk tokens | heads: [list active heads]
```
