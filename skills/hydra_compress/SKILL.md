---
name: hydra_compress
description: >
  HYDRA HEAD-3: Semantic context compressor. Creates structured digests of conversation
  history and file context to prevent context saturation. Implements checkpointing,
  rolling summaries, and semantic state serialization. Trigger with 'hydra compress',
  'compactar contexto', 'resumir historico', 'hydra checkpoint', 'context too long'.
---

# HYDRA TOKENS ANTIGRAVITY — HEAD-3: Context Compressor

## The Problem
In long agent sessions, the conversation history grows unbounded. Every new message
forces the model to re-read ALL previous messages. A 10-turn conversation can balloon
to 20,000+ tokens of input for each subsequent response — even when most of that
history is no longer relevant.

**Research shows: semantic summarization alone can reduce context by 60–80%.**

---

## Activation Phrases
- `hydra compress`, `hydra checkpoint`
- `compactar contexto`, `resumir historico`
- `context too long`, `contexto grande`
- Auto-triggered when context exceeds ~15,000 tokens

---

## Compression Protocol

When activated, execute the following steps in order:

### STEP 1 — Context Snapshot
Scan the current conversation and identify:
```
=== HYDRA COMPRESS: SNAPSHOT ===
Turns in history   : N
Estimated tokens   : ~X
Files in context   : [list]
Key decisions made : [list top 5]
Current task state : [what we are doing right now]
Files changed      : [list modified files]
Pending actions    : [what still needs to be done]
```

### STEP 2 — Generate Semantic Digest
Produce a compact, structured digest that captures ONLY the essential state:

```markdown
## HYDRA CHECKPOINT — [timestamp]

### Project Context
- Working dir: [path]
- Tech stack: [technologies]
- Current goal: [brief description]

### Decisions Made (do not revisit)
- [decision 1]: [outcome]
- [decision 2]: [outcome]
- [decision 3]: [outcome]

### Files Modified
| File | Change Type | Status |
|------|-------------|--------|
| [file] | [add/edit/delete] | [done/pending] |

### Current State
[1-3 sentence description of exactly where we are in the task]

### Next Actions
1. [immediate next step]
2. [following step]
3. [if applicable]

### Known Issues / Blockers
- [any unresolved problems]
```

### STEP 3 — Announce Compression
Report to the user:
```
[HYDRA HEAD-3] Context compressed.
Before: ~X tokens | After: ~Y tokens | Saved: ~Z tokens (W%)
Checkpoint saved. History before this point has been replaced with the digest above.
Continuing from current state...
```

---

## Compression Strategies

### Strategy C1: Rolling Summary (automatic, every 10 turns)
After every 10 conversation turns, automatically generate a mini-summary of those
10 turns and replace them in context with the summary. Keep only the last 3 turns raw.

**Format:**
```
[SUMMARY of turns 1-10]: Key points and decisions from early session.
[SUMMARY of turns 11-20]: Progress made, files modified, issues found.
[RAW] Turn 21: [full turn]
[RAW] Turn 22: [full turn]
[RAW] Turn 23: [full turn] ← current
```

### Strategy C2: File Context Minimization
Instead of keeping full file contents in context:
- After a file is analyzed, replace it with a **file summary stub**:
```
[FILE STUB: path/to/file.py]
Purpose: [one line description]
Key functions: [list of function names only]
Last modified: [what we changed]
Lines: [X total]
[Full content available via read_file tool if needed]
```

### Strategy C3: Semantic Deduplication
Scan the context for repeated information and remove duplicates:
- Same error message appearing multiple times → keep only the first + count
- Same file path mentioned repeatedly → consolidate references
- Repeated instructions already confirmed → mark as [CONFIRMED] and collapse

### Strategy C4: State Serialization Checkpoint
For complex, long-running tasks, serialize the full state to a file:
```json
{
  "hydra_checkpoint": {
    "version": "1.0",
    "timestamp": "ISO-8601",
    "goal": "brief task description",
    "completed_steps": ["step1", "step2"],
    "pending_steps": ["step3", "step4"],
    "key_files": ["path/to/file1", "path/to/file2"],
    "decisions": { "decision_key": "outcome" },
    "current_state": "one paragraph state description"
  }
}
```
Save to: `.hydra_checkpoint.json` in the working directory.
On next session, load this file to restore context with minimal token cost.

---

## Auto-Compression Triggers

The compressor should activate automatically when:

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Turn count | > 15 turns | Rolling summary of oldest 10 |
| Context size | > 15,000 tokens | Full compress + checkpoint |
| File count in context | > 5 files | Replace old files with stubs |
| Repeated errors | > 3 of same error | Collapse to single reference |
| Task completion | Any step marked done | Archive completed step details |

---

## Quick Commands

```
hydra compress now        → Immediate full compression
hydra checkpoint save     → Save state to .hydra_checkpoint.json
hydra checkpoint load     → Restore from saved checkpoint
hydra compress report     → Show what can be compressed without doing it
hydra compress history    → Compress only conversation history, keep files
```
