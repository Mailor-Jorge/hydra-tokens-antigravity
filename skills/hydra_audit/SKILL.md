---
name: hydra_audit
description: >
  HYDRA HEAD-4: Token cost auditor. Analyzes all active customizations (skills, rules, MCP
  servers) and estimates their token footprint. Generates a detailed cost report with
  optimization recommendations. Trigger with 'hydra audit', 'auditoria de tokens',
  'custo atual', 'token report', 'quanto custa'.
---

# HYDRA TOKENS ANTIGRAVITY — HEAD-4: Token Auditor

## Purpose
Provide a transparent, actionable report of EXACTLY how many tokens your current
Antigravity configuration is consuming before you even type your first message.

**Visibility is the foundation of optimization: you cannot reduce what you cannot see.**

---

## Activation Phrases
- `hydra audit`, `hydra audit full`
- `auditoria de tokens`, `custo atual`
- `token report`, `quanto custa`
- `how many tokens am i using`

---

## Audit Protocol

When activated, generate the following report:

### SECTION 1: Customization Token Cost

```
╔══════════════════════════════════════════════════════╗
║         HYDRA TOKEN AUDIT REPORT                     ║
║         Generated: [timestamp]                       ║
╠══════════════════════════════════════════════════════╣
║ RULES LOADED                                         ║
║   user_global                          : ~810 tokens ║
║   HYDRA_OUTPUT_FORMAT (HEAD-5)         : ~120 tokens ║
║   HYDRA_CONTEXT_GUARD (HEAD-6)         : ~90  tokens ║
║   HYDRA_NO_REPEAT (HEAD-7)             : ~60  tokens ║
║   [other rules...]                     : ~XXX tokens ║
║   SUBTOTAL RULES                       : ~X,XXX tok  ║
╠══════════════════════════════════════════════════════╣
║ SKILLS LOADED                                        ║
║   hydra (this skill - HEAD-1)          : ~XXX tokens ║
║   hydra_mcp (HEAD-2)                   : ~XXX tokens ║
║   hydra_compress (HEAD-3)              : ~XXX tokens ║
║   hydra_audit (HEAD-4)                 : ~XXX tokens ║
║   caveman                              : ~90  tokens ║
║   graphify                             : ~140 tokens ║
║   antigravity-guide                    : ~171 tokens ║
║   [other skills...]                    : ~XXX tokens ║
║   SUBTOTAL SKILLS                      : ~X,XXX tok  ║
╠══════════════════════════════════════════════════════╣
║ MCP SERVERS LOADED                                   ║
║   [server name]    [tool count] [schema]  : ~XX tok  ║
║   SUBTOTAL MCP                         : ~X,XXX tok  ║
╠══════════════════════════════════════════════════════╣
║ CONVERSATION CONTEXT                                 ║
║   System prompt overhead               : ~X,XXX tok  ║
║   Current history                      : ~X,XXX tok  ║
║   Files in context                     : ~X,XXX tok  ║
╠══════════════════════════════════════════════════════╣
║ TOTAL BASELINE INPUT TOKENS            : ~XX,XXX tok ║
║ CUSTOMIZATION BUDGET USED              : X.X%        ║
╚══════════════════════════════════════════════════════╝
```

### SECTION 2: Waste Detection

Automatically flag these patterns as WASTE:

| Issue | Severity | Tokens Wasted | Recommendation |
|-------|----------|---------------|----------------|
| Skills active but never triggered this session | MEDIUM | ~XXX | Disable between sessions |
| MCP servers loaded with no tool calls | HIGH | ~XXX–XXX | Unload immediately |
| Conversation history > 10 turns uncompressed | HIGH | ~X,XXX | Run HEAD-3 compress |
| Files opened but not referenced in last 5 turns | MEDIUM | ~XXX | Replace with stubs |
| Rules with overlapping instructions | LOW | ~XXX | Consolidate |
| Duplicate permission grants in config | LOW | ~XXX | Clean config.json |

### SECTION 3: Optimization Score

```
HYDRA EFFICIENCY SCORE: [0-100]

Breakdown:
  Skill hygiene      : XX/25
  MCP efficiency     : XX/25
  Context management : XX/25
  Output format      : XX/25

Status: [EXCELLENT | GOOD | NEEDS WORK | CRITICAL]

Top 3 actions to improve score:
  1. [most impactful action]
  2. [second action]
  3. [third action]
```

### SECTION 4: Session Cost Estimate

```
COST ESTIMATE (rough, based on typical API pricing):
  Input tokens per request  : ~X,XXX tokens
  Output tokens per response: ~XXX tokens
  ─────────────────────────────────────────
  At Claude Sonnet pricing  : ~$X.XXX / request
  At Gemini Flash pricing   : ~$X.XXX / request
  At GPT-4o-mini pricing    : ~$X.XXX / request
  
  Projected session cost (20 requests):
    High model              : ~$X.XX
    With HYDRA optimizations: ~$X.XX (save ~XX%)
```

---

## Audit Flags Reference

### 🔴 CRITICAL (act immediately)
- Context > 50,000 tokens
- > 5 MCP servers loaded for a simple task
- Conversation history > 30 turns uncompressed

### 🟡 WARNING (act soon)
- Context > 15,000 tokens
- > 3 unused skills active in current session
- Any single rule > 1,000 tokens

### 🟢 OK (monitor)
- Context < 10,000 tokens
- MCP usage matches task type
- All active skills triggered at least once

---

## Quick Commands

```
hydra audit              → Full audit report
hydra audit quick        → Summary only (top 3 issues)
hydra audit mcp          → MCP-specific audit
hydra audit skills       → Skills/rules-specific audit
hydra audit cost         → Cost estimation only
hydra audit history      → Compare current vs last audit
```

---

## Audit Tips

1. **Run audit at session start** to baseline your token footprint.
2. **Run audit at ~10 turns** to catch context bloat early.
3. **Compare audits** across sessions to track improvement.
4. **Use audit results** to inform which HYDRA heads to activate.
5. **Share audit reports** in issue trackers to explain token costs to team members.
