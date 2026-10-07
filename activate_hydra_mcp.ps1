# PowerShell Script to Automatically Configure & Activate HYDRA MCP Tools in Antigravity IDE
# Usage: .\activate_hydra_mcp.ps1

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  HYDRA MCP AUTOMATIC ACTIVATOR v1.2" -ForegroundColor Cyan
Write-Host "  Auto-registers hydra-tools-mcp in Antigravity Panel" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

$userProfile = $env:USERPROFILE
$configDir = "$userProfile\.gemini\config"
$mcpConfigPath = "$configDir\mcp_config.json"
$targetServerScript = "$configDir\hydra_mcp_server.py"
$schemasTargetDir = "$userProfile\.gemini\antigravity\mcp\hydra-tools-mcp"

# 1. Copy MCP server script to config dir
$sourceServerScript = ".\mcp\hydra_mcp_server.py"
if (-not (Test-Path $sourceServerScript)) {
    $sourceServerScript = "..\mcp\hydra_mcp_server.py"
}

if (Test-Path $sourceServerScript) {
    Copy-Item -Path $sourceServerScript -Destination $targetServerScript -Force
    Write-Host "  [OK] Copied hydra_mcp_server.py to $targetServerScript" -ForegroundColor Green
} else {
    Write-Host "  [WARN] Source hydra_mcp_server.py not found locally, checking existing target..." -ForegroundColor Yellow
}

# 2. Ensure schemas directory exists and copy schemas if available
if (-not (Test-Path $schemasTargetDir)) {
    New-Item -ItemType Directory -Path $schemasTargetDir -Force | Out-Null
    Write-Host "  [OK] Created MCP schemas directory at $schemasTargetDir" -ForegroundColor Green
}

$existingSchemas = Get-ChildItem "$userProfile\.gemini\antigravity\mcp\hydra-tools-mcp\*.json" -ErrorAction SilentlyContinue
if ($existingSchemas) {
    Write-Host "  [OK] Verified $($existingSchemas.Count) MCP tool schema JSON files active." -ForegroundColor Green
}

# 3. Read & Merge mcp_config.json
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

$mcpData = @{ "mcpServers" = @{} }
if (Test-Path $mcpConfigPath) {
    try {
        $rawJson = Get-Content $mcpConfigPath -Raw -ErrorAction Stop
        if ($rawJson.Trim().Length -gt 0) {
            $mcpData = $rawJson | ConvertFrom-Json
        }
    } catch {
        Write-Host "  [WARN] Could not parse existing mcp_config.json, re-creating..." -ForegroundColor Yellow
    }
}

if (-not $mcpData.mcpServers) {
    $mcpData | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value @{} -Force
}

# Add or Update hydra-tools-mcp entry
$hydraEntry = [ordered]@{
    "command" = "python"
    "args"    = @($targetServerScript)
}

if ($mcpData.mcpServers.PSObject.Properties['hydra-tools-mcp']) {
    $mcpData.mcpServers.'hydra-tools-mcp' = $hydraEntry
    Write-Host "  [OK] Updated 'hydra-tools-mcp' entry in mcp_config.json" -ForegroundColor Green
} else {
    $mcpData.mcpServers | Add-Member -MemberType NoteProperty -Name "hydra-tools-mcp" -Value $hydraEntry -Force
    Write-Host "  [NEW] Registered 'hydra-tools-mcp' in mcp_config.json" -ForegroundColor Green
}

# Save updated mcp_config.json
$jsonOutput = $mcpData | ConvertTo-Json -Depth 10
Set-Content -Path $mcpConfigPath -Value $jsonOutput -Encoding UTF8
Write-Host "  [OK] Saved updated $mcpConfigPath" -ForegroundColor Green

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  HYDRA MCP TOOLS ACTIVATED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "  Registered Tools: hydra_filter_log, hydra_token_estimate," -ForegroundColor White
Write-Host "  hydra_clean_scratch, hydra_snippet, hydra_cache," -ForegroundColor White
Write-Host "  hydra_context_snapshot, hydra_dependency_trace," -ForegroundColor White
Write-Host "  hydra_edit_verify, hydra_file_hash." -ForegroundColor White
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""
