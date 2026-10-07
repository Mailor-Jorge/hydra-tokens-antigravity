# HYDRA TOKENS ANTIGRAVITY — Installation Guide

## Quick Install

### Step 1: Clone the Repository

```powershell
git clone https://github.com/Mailor-Jorge/hydra-tokens-antigravity.git
cd hydra-tokens-antigravity
```

### Step 2: Run the Installer (Auto-installs Skills, Rules & MCP Tools)

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

> **Note:** `install.ps1` automatically executes `activate_hydra_mcp.ps1` to register `hydra-tools-mcp` inside your `mcp_config.json` and enable all 9 native HYDRA tools in the Antigravity panel!

### Step 3: Standalone MCP Activation (Optional)

If you ever need to re-activate or update the HYDRA MCP tools in your panel, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\activate_hydra_mcp.ps1
```

---

## Verify Installation

After restarting Antigravity IDE, go to **Settings → Customizations**. You should see:

**Skills:**
- ✅ `hydra` — HYDRA TOKENS ANTIGRAVITY Main Orchestrator
- ✅ `hydra_mcp` — HYDRA HEAD-2: Smart MCP Selector
- ✅ `hydra_compress` — HYDRA HEAD-3: Context Compressor
- ✅ `hydra_audit` — HYDRA HEAD-4: Token Auditor

**Rules (in AGENTS.md):**
- ✅ `HYDRA_OUTPUT_FORMAT` (HEAD-5)
- ✅ `HYDRA_CONTEXT_GUARD` (HEAD-6)
- ✅ `HYDRA_NO_REPEAT` (HEAD-7)

**Token budget impact:** All 4 skills + 3 rules should add approximately **4–6%** to your
customization budget — a minimal footprint for maximum token savings.

---

## First Use

Once installed, test HYDRA with these commands in Antigravity IDE:

```
1. Type: hydra audit
   → Should generate a token cost report of your current configuration

2. Type: hydra
   → Should activate HYDRA mode and show a system scan

3. Type: hydra mcp file operations
   → Should recommend minimal MCP servers for file tasks

4. Type: hydra compress
   → Should show what can be compressed in your current context
```

---

## Uninstallation

```powershell
# Remove HYDRA skills
Remove-Item -Recurse -Force "$env:USERPROFILE\.gemini\config\skills\hydra"
Remove-Item -Recurse -Force "$env:USERPROFILE\.gemini\config\skills\hydra_mcp"
Remove-Item -Recurse -Force "$env:USERPROFILE\.gemini\config\skills\hydra_compress"
Remove-Item -Recurse -Force "$env:USERPROFILE\.gemini\config\skills\hydra_audit"

# Remove HYDRA rules from AGENTS.md
# (manually remove the HYDRA sections from your AGENTS.md file)
notepad "$env:USERPROFILE\.gemini\config\AGENTS.md"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skills not showing in IDE | Restart Antigravity IDE after installation |
| `hydra` trigger not working | Type the full phrase: "modo hydra" or "/hydra" |
| Rules not applying | Check that AGENTS.md was saved correctly |
| MCP tracker not connecting | Ensure Node.js is installed (`node --version`) |
| Budget exceeded after install | Use caveman mode alongside HYDRA for extra savings |
