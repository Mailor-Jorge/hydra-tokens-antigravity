# HYDRA TOKENS ANTIGRAVITY — Installation Guide

## Quick Install

### Step 1: Clone the Repository

```powershell
git clone https://github.com/Mailor-Jorge/hydra-tokens-antigravity.git
cd hydra-tokens-antigravity
```

### Step 2: Run the Installer

```powershell
.\install.ps1
```

### Step 3: Restart Antigravity IDE

Close and reopen Antigravity IDE. The 4 HYDRA skills will appear in your
**Customizations → Skills** panel.

---

## Manual Installation

### Install Skills (4 heads)

```powershell
# Navigate to project folder
cd hydra-tokens-antigravity

# Copy all 4 HYDRA skills to Antigravity config
Copy-Item -Recurse skills\hydra     "$env:USERPROFILE\.gemini\config\skills\hydra" -Force
Copy-Item -Recurse skills\hydra_mcp "$env:USERPROFILE\.gemini\config\skills\hydra_mcp" -Force
Copy-Item -Recurse skills\hydra_compress "$env:USERPROFILE\.gemini\config\skills\hydra_compress" -Force
Copy-Item -Recurse skills\hydra_audit   "$env:USERPROFILE\.gemini\config\skills\hydra_audit" -Force
```

### Install Rules (3 heads)

```powershell
# Check if AGENTS.md exists; create it if not
$agentsPath = "$env:USERPROFILE\.gemini\config\AGENTS.md"
if (-not (Test-Path $agentsPath)) {
    New-Item -ItemType File -Path $agentsPath -Force
}

# Append HYDRA rules to your existing AGENTS.md
Add-Content -Path $agentsPath -Value "`n`n"
Add-Content -Path $agentsPath -Value (Get-Content rules\AGENTS.md -Raw)
Write-Host "HYDRA rules added to AGENTS.md"
```

### Install MCP Token Tracker (optional, HEAD-8)

```powershell
# View your current MCP config
Get-Content "$env:USERPROFILE\.gemini\config\mcp_config.json"

# Merge the HYDRA tracker config
# (manually copy the 'hydra-token-tracker' block from mcp\hydra_tracker_config.json
#  into your mcp_config.json under the 'mcpServers' object)
notepad "$env:USERPROFILE\.gemini\config\mcp_config.json"
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
