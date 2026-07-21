# HYDRA Example 1: Basic HYDRA Mode Session

## Scenario
A developer starting a new coding session wants to minimize token waste from the start.

## Conversation Example

---

**User:** hydra

**Agent Response:**
```
=== HYDRA SYSTEM SCAN ===
[1] Skills active    : hydra(140t), hydra_mcp(180t), hydra_compress(220t), hydra_audit(200t), caveman(90t), graphify(140t)
[2] Rules active     : user_global(810t), HYDRA_OUTPUT_FORMAT(120t), HYDRA_CONTEXT_GUARD(90t), HYDRA_NO_REPEAT(60t)
[3] MCP servers      : none loaded (0t)
[4] Context size     : ~1,850 tokens (clean session start)
[5] Waste detected   : graphify skill loaded but no graph query detected

=== RECOMMENDATIONS ===
→ HEAD-2: Disable graphify skill if no graph analysis planned (saves 140t)
→ HEAD-4: Run 'hydra audit' for detailed cost breakdown
→ Status: EFFICIENT — good session start

─ HYDRA: active | context: ~1.8k tokens | heads: [1,5,6,7]
```

---

**User:** I need to edit 3 Python files to add logging

**Agent Response:**
```
[HYDRA] Task type: File Operations | Loading: filesystem tools only

Ready. Which 3 files?
```

---

**Result:**
- Standard approach would load all MCP servers + full tool schemas: ~8,000 tokens
- HYDRA approach: filesystem only: ~300 tokens
- **Savings: ~7,700 tokens on this request alone**
