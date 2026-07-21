# HYDRA HEAD-9: Optimized Agent Template

## Overview
This is the minimal-footprint agent system prompt template for Antigravity projects.
Use this as a base when creating new agents or configuring subagents.

The design philosophy: **every token in the system prompt is a recurring tax on every request.**
This template achieves maximum capability with minimum token cost.

---

## Template: HYDRA_AGENT_SYSTEM_PROMPT

```
You are [AGENT_NAME], a specialized agent for [ONE_SENTENCE_ROLE].

## Scope
- Do: [3-5 bullet points of what this agent does]
- Do not: [2-3 bullet points of what this agent avoids]

## Output Format
- [preferred format: code/JSON/markdown/plain]
- [max length guideline]
- [key formatting rule]

## Context
[INJECT_MINIMAL_CONTEXT_HERE — max 500 tokens]

## Task
[CURRENT_TASK_DESCRIPTION]
```

---

## Template Variables

| Variable | Description | Token Budget |
|----------|-------------|-------------|
| `[AGENT_NAME]` | Short, descriptive name | 2-5 tokens |
| `[ONE_SENTENCE_ROLE]` | Precise role definition | 10-20 tokens |
| `Do:` bullets | Core capabilities | 30-75 tokens |
| `Do not:` bullets | Scope boundaries | 20-50 tokens |
| `Output Format` | Response structure | 20-40 tokens |
| `[INJECT_MINIMAL_CONTEXT_HERE]` | Task-specific context | Max 500 tokens |
| `[CURRENT_TASK_DESCRIPTION]` | What to do now | 20-100 tokens |
| **TOTAL** | Full system prompt | **~200-800 tokens** |

Compare to typical verbose system prompts: 2,000–10,000 tokens.
**HYDRA template achieves 75-90% reduction.**

---

## Anti-Pattern Examples

### ❌ BLOATED system prompt (4,500 tokens):
```
You are an expert AI coding assistant with deep knowledge of software engineering
principles, best practices, design patterns, and modern development workflows.
Your role is to help developers write clean, maintainable, efficient code while
following industry standards and conventions...
[continues for 3 more paragraphs explaining obvious things]

When responding, you should:
- Always be helpful and professional
- Provide complete solutions
- Explain your reasoning clearly
- Consider edge cases
- Follow best practices
- Make sure the code works
[20 more obvious bullet points]
```

### ✅ HYDRA template (200 tokens):
```
You are CodeReviewer, specialized in Python code review.

## Scope
- Do: find bugs, suggest optimizations, enforce PEP-8
- Do not: rewrite entire files, add unrelated features

## Output Format
- Structured: [File:Line] Issue | Fix
- One fix per line, no prose explanation unless asked

## Task
Review the provided Python file for security vulnerabilities.
```

---

## Subagent Configuration Template

When spawning subagents in Antigravity, use this minimal configuration:

```python
# HYDRA-optimized subagent definition
subagent_config = {
    "name": "hydra_worker",
    "role": "[specific role - max 10 words]",
    "prompt": """
[CONTEXT]: [2-3 sentences of essential context only]
[TASK]: [exact task description]
[FORMAT]: [expected output format]
[RETURN]: [what to report back when done]
    """,
    "model": "flash",  # Use smallest capable model
    "tools": ["only_needed_tool_1", "only_needed_tool_2"]  # Minimal toolset
}
```

---

## Tiered Model Selection Guide (HEAD-9 Strategy)

Match model to task complexity — bigger is not always better:

| Task Type | Recommended Model | Reason |
|-----------|-----------------|--------|
| File reading, simple search | flash_lite | Maximum speed, minimum cost |
| Code formatting, simple edits | flash | Good balance |
| Research, web search | flash | Sufficient for most searches |
| Complex reasoning, architecture | pro/inherit | Requires deep reasoning |
| Multi-file refactoring | pro | Needs large context + reasoning |
| Simple yes/no decisions | flash_lite | Overkill to use flagship |

**Rule: Default to `flash`. Escalate to `pro` only when `flash` demonstrably fails.**

---

## Checkpoint Template

Use this template to save agent state for context compression (HEAD-3 integration):

```json
{
  "agent": "hydra_agent_v1",
  "checkpoint_at": "ISO_TIMESTAMP",
  "goal": "Brief task goal",
  "progress": "X/N steps complete",
  "completed": ["step1", "step2"],
  "current": "step3 description",
  "pending": ["step4", "step5"],
  "files_touched": ["path/file1", "path/file2"],
  "decisions": {
    "key_decision": "chosen_option"
  },
  "blockers": [],
  "resume_instruction": "One sentence on how to resume from this point"
}
```

Save to `.hydra_checkpoint.json`. Load at session start to skip re-reading history.

---

## Usage

1. Copy the template above
2. Fill in the variables for your specific agent
3. Keep it under 500 tokens total
4. Test: if the agent still works, you haven't lost capability — you've gained efficiency
5. Report savings with `hydra audit`
