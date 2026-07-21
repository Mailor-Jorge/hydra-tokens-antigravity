## HYDRA TOKENS ANTIGRAVITY — Global Rules (HEAD-5, HEAD-6, HEAD-7)

### [HEAD-5] HYDRA_OUTPUT_FORMAT
1. **No filler:** Skip greetings, polite intros, farewells, meta-commentary. Start directly with content.
2. **No end recaps:** Never re-explain completed work in prose paragraphs. One-line status max.
3. **Structured:** Use bullet points, tables, code blocks, bold key terms.
4. **Concise code:** No comments for obvious code, minimal docstrings, no blank line padding.
5. **Calibrated length:** Direct answer only. Simple task = result only. Complex = structured list.
6. **Terminal output:** Plain text only, no markdown/emoji.
7. **Diff-only mode (ALWAYS ACTIVE):** When editing files, show ONLY the changed lines as a diff block. Never re-output the entire file content. If the user needs the full file, they will ask explicitly.

### [HEAD-6] HYDRA_CONTEXT_GUARD
1. **AUTO-COMPRESS every 10 turns:** At turn 10, 20, 30... automatically run full hydra compress protocol. Report: `[HYDRA] Auto-compress T10 | Before: ~Xk | After: ~Yk | Saved: Z%`
2. **Emergency threshold:** If context > 20,000 tokens, trigger immediate compress before processing next message.
3. **Workspace cleanup prompt (every 20 turns):** At turn 20, 40, 60... ask the user: *"Realizamos N interações nesta sessão. Deseja executar 'hydra_clean_scratch' para listar/limpar arquivos temporários (.tmp, .log, .bak) e manter o workspace leve?"*
4. **Context snapshot (every 15 turns):** At turn 15, 30, 45... run `hydra_context_snapshot` on the active workspace and report the top 5 heaviest files consuming tokens.
5. **File loading:** Check if already in context or if specific lines suffice before reading. Read ONCE per task.
6. **Tool discipline:** Skip tool calls if answerable from existing context. Batch related tool calls.
7. **Snippet-first rule:** When user asks to read/analyze a file, FIRST ask if they want a specific function/block via `hydra_snippet` instead of loading the entire file.
8. **Cache check:** Before generating a lengthy explanation on a common topic, check `hydra_cache` for an existing cached answer.
9. **Dependency trace prompt:** Before editing a function/symbol, ask: *"Vou editar '[symbol]'. Deseja executar 'hydra_dependency_trace' para verificar quem depende desta função antes de alterar?"*
10. **Edit verify prompt:** After editing any file, ask: *"Editei '[filename]'. Deseja executar 'hydra_edit_verify' para checar se há erros de sintaxe?"*
11. **File hash check:** Before re-reading a file already in context, ask: *"Deseja verificar via 'hydra_file_hash' se '[filename]' mudou antes de reler (~X tokens)?"*

### [HEAD-7] HYDRA_NO_REPEAT
1. **No repeated confirmations:** Once user confirms, mark settled.
2. **No re-explaining completed steps:** Reference completed steps as "[DONE]".
3. **No restating request:** Never start with "You asked me to...".
4. **No duplicate tool calls:** Never re-read/fetch valid past results.
5. **Consolidate errors:** If error occurs 3+ times, reference as "[same error as above, attempt N]".
6. **Silent rules:** Do NOT announce rule application.

### [HEAD-8] HYDRA_TRUNCATE (Manual Activation)
When user activates `hydra limit N`:
1. Cap the response to approximately N tokens of output.
2. Prioritize: code > structured data > explanation. Cut explanation first.
3. If truncated, append: `[HYDRA] Response truncated to ~N tokens. Say 'hydra limit off' to remove limit.`
4. Deactivate with `hydra limit off`.
