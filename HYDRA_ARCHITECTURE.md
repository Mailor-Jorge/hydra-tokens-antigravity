# HYDRA TOKENS ANTIGRAVITY — Architecture

## System Overview

```
╔══════════════════════════════════════════════════════════════════╗
║                  HYDRA TOKENS ANTIGRAVITY v1.0                   ║
║           9-Headed Token Economy System for Antigravity IDE       ║
╚══════════════════════════════════════════════════════════════════╝

 USER REQUEST
      │
      ▼
 ┌────────────────────────────────────────────────────────────┐
 │             HEAD-1: HYDRA ORCHESTRATOR (Skill)              │
 │  • System scan    • Head routing    • Status reporting      │
 └───┬──────────────┬──────────────┬──────────────┬───────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
┌─────────┐  ┌─────────────┐  ┌──────────┐  ┌──────────────┐
│ HEAD-2  │  │   HEAD-3    │  │  HEAD-4  │  │  HEAD-9      │
│MCP      │  │Context      │  │Token     │  │Agent         │
│Selector │  │Compressor   │  │Auditor   │  │Template      │
│(Skill)  │  │(Skill)      │  │(Skill)   │  │(Template)    │
└─────────┘  └─────────────┘  └──────────┘  └──────────────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                           │
              ┌────────────▼────────────┐
              │   ALWAYS-ON RULE LAYER  │
              ├─────────────────────────┤
              │ HEAD-5: Output Format   │
              │ HEAD-6: Context Guard   │
              │ HEAD-7: No Repeat       │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   HEAD-8: MCP TRACKER   │
              │  (Token Usage Monitor)  │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │     AI MODEL CALL       │
              │  (Minimum viable input) │
              └─────────────────────────┘
```

---

## Token Flow Diagram

```
WITHOUT HYDRA:
┌──────────────────────────────────────────────────────────┐
│ System prompt       : 5,000 tokens (verbose)             │
│ All rules (always)  : 2,500 tokens (unfiltered)          │
│ All skills (always) : 3,000 tokens (loaded always)       │
│ All MCP tools       : 8,000 tokens (all servers)         │
│ Full chat history   : 12,000 tokens (no compression)     │
│ User message        : 50 tokens                          │
│ ─────────────────────────────────────────────────────── │
│ TOTAL INPUT         : 30,550 tokens per request          │
│ Estimated cost      : ~$0.09 per request                 │
└──────────────────────────────────────────────────────────┘

WITH HYDRA:
┌──────────────────────────────────────────────────────────┐
│ System prompt       : 500 tokens (HYDRA template)        │
│ Rules (selective)   : 600 tokens (3 HYDRA rules)         │
│ Skills (on-demand)  : 400 tokens (only triggered ones)   │
│ MCP tools           : 300 tokens (only needed servers)   │
│ Compressed history  : 2,000 tokens (semantic digest)     │
│ User message        : 50 tokens                          │
│ ─────────────────────────────────────────────────────── │
│ TOTAL INPUT         : 3,850 tokens per request           │
│ Estimated cost      : ~$0.01 per request                 │
│ ─────────────────────────────────────────────────────── │
│ SAVINGS             : 26,700 tokens | ~88% reduction     │
└──────────────────────────────────────────────────────────┘
```

---

## Data Flow: Each Head's Processing

### HEAD-2 MCP Selector Flow
```
Task arrives → Classify task type → Map to required MCP servers
→ Load ONLY those servers → Process → Discard after task
```

### HEAD-3 Context Compressor Flow
```
Context > threshold → Snapshot current state → 
Generate semantic digest → Replace raw history →
Save checkpoint file → Continue with clean context
```

### HEAD-4 Auditor Flow
```
Audit triggered → Scan all loaded customizations →
Count tokens per component → Detect waste patterns →
Generate efficiency score → Output recommendations
```

---

## Integration Points

```
C:\Users\{USER}\.gemini\config\
├── AGENTS.md              ← HEAD-5,6,7 rules appended here
├── mcp_config.json        ← HEAD-8 tracker added here
└── skills\
    ├── hydra\             ← HEAD-1 installed here
    ├── hydra_mcp\         ← HEAD-2 installed here
    ├── hydra_compress\    ← HEAD-3 installed here
    └── hydra_audit\       ← HEAD-4 installed here
```

---

## Performance Benchmarks

Based on research from industry sources (2025 data):

| Optimization Layer | Technique | Savings Range |
|-------------------|-----------|--------------|
| MCP Dynamic Loading | HEAD-2 | 50–96% of tool tokens |
| Context Compression | HEAD-3 | 60–80% of history tokens |
| Prompt Caching | HEAD-5 rules | 80–90% on repeated tokens |
| Output Format Rules | HEAD-5 | 15–40% output tokens |
| Context Guard | HEAD-6 | Prevents unbounded growth |
| Anti-Repetition | HEAD-7 | 10–25% context tokens |
| Agent Template | HEAD-9 | 75–90% system prompt tokens |
| **Combined HYDRA** | All heads | **70–90% total reduction** |
