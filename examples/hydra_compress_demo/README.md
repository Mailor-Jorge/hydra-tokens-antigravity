# HYDRA Example 3: Context Compression Mid-Session (HEAD-3)

## Scenario
In a long refactoring session, turn count reaches 10 or context size exceeds 15,000 tokens. HYDRA automatically triggers context compression to prevent context saturation.

## Execution Flow

```
[System Event: Turn 10 reached]

[HYDRA HEAD-6] AUTO-COMPRESS TRIGGERED
Before : ~18,500 tokens across 10 turns
Compressing history into semantic checkpoint...

==================================================
CHECKPOINT CREATED:
- Working directory: C:\Projects\MyMod
- Files modified: ScriptA.psc (done), ScriptB.psc (in progress)
- Decisions made: Using SKI_ConfigBase vanilla MCM, DEBUG tab added
- Active blockers: None
==================================================

After  : ~1,800 tokens
Saved  : ~16,700 tokens (90.2% reduction)

Continuing turn 11 from compressed checkpoint...
```

---

## Key Benefits
- **Prevents Reasoning Degradation:** Models stay focused and accurate without getting "lost in the middle" of long chat logs.
- **Massive Cost Savings:** Reduces API costs per request by 80–90% for all subsequent turns.
- **State Preservation:** Keeps exact task state, modified files, and uncompleted actions while discarding raw conversational noise.
