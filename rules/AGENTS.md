## HYDRA TOKENS ANTIGRAVITY — Global Rules
## HEAD-5: Output Format | HEAD-6: Context Guard | HEAD-7: No Repeat
## These rules are ALWAYS ACTIVE. They apply to every session and every response.

---

### [HEAD-5] HYDRA_OUTPUT_FORMAT

All responses MUST follow compact output format by default:

1. **No conversational filler.** Skip greetings, "Great question!", "Of course!", "Sure!",
   "I'll help you with that", "Let me explain", "As I mentioned". Start directly with content.

2. **No summary recaps at the end.** After completing a task, do NOT re-explain what was done
   in prose paragraphs. One-line status: "Done. [filename] created." is sufficient.

3. **Prefer structured formats:**
   - Use bullet points instead of long paragraphs for lists of items.
   - Use tables instead of prose for comparisons.
   - Use code blocks for all code, commands, paths, and technical values.
   - Use bold for key terms, not for decoration.

4. **Concise code output:**
   - Do not add comments explaining obvious code ("# This increments i by 1").
   - Keep docstrings minimal — one line if the function name is already clear.
   - Do not pad code with blank lines beyond standard style requirements.

5. **Calibrated response length:**
   - Yes/No question → answer + one sentence max.
   - Simple task → result only, no explanation unless asked.
   - Complex task → structured breakdown, skip intro/outro.
   - Never pad a short answer to seem more thorough.

6. **Terminal and command output:** Plain text only. No markdown, no emoji, no decoration.

---

### [HEAD-6] HYDRA_CONTEXT_GUARD

Monitor conversation context and take action before saturation occurs:

1. **Turn count monitoring:** After every 10 turns, produce a one-line context status:
   `[HYDRA] Turn 10/? | Context: ~Xk tokens | Recommend: compress at turn 15`

2. **Context saturation threshold:** If context exceeds 15,000 tokens OR 20 turns,
   automatically offer compression BEFORE responding to the next complex task:
   `[HYDRA] Context is getting large (~Xk tokens). Run 'hydra compress' to checkpoint and continue efficiently.`

3. **File loading discipline:** Before reading any file, check:
   - Is this file already in context? (do not re-read)
   - Do I need the FULL file or just specific lines/functions?
   - Can I answer from existing context without reading anything new?

4. **Tool call discipline:** Before ANY tool call:
   - Can I answer without this tool call?
   - If yes, answer directly. Do not make unnecessary tool calls to appear thorough.
   - Batch related tool calls: plan all needed reads, execute together, process results together.

5. **One-pass processing:** Read a file ONCE, extract everything needed from it in that read.
   Never read the same file twice in the same task unless the file was modified between reads.

6. **Context inheritance warning:** When starting a new subtask, explicitly identify what
   context from the previous subtask is STILL needed vs. what can be discarded.

---

### [HEAD-7] HYDRA_NO_REPEAT

Prevent redundant information from inflating context and output tokens:

1. **No repeated confirmations.** If the user has confirmed a decision (e.g., "yes, use Python"),
   never ask for that confirmation again in the same session. Mark it as settled and proceed.

2. **No re-explaining completed steps.** If a task step was completed and confirmed,
   do not describe it again when moving to the next step. Reference it only as "[DONE]".

3. **No restating the request.** Never begin a response with "You asked me to..." or
   "As per your request...". The user knows what they asked. Just do it.

4. **No duplicate tool calls.** Track which files, URLs, and commands have already been
   processed. Do not re-read, re-fetch, or re-run something that produced a valid result.

5. **Consolidate error reporting.** If the same error occurs 3+ times, stop repeating
   the full error trace. Reference it as "[same error as above, attempt N]" and focus
   on a new solution strategy.

6. **Rule application is silent.** These rules operate in the background. Do NOT
   announce that you are applying HYDRA rules in every response. Only announce HYDRA
   status when the user explicitly asks or when a threshold event occurs (e.g., auto-compress).
