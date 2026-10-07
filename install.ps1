# PowerShell Installer for HYDRA TOKENS ANTIGRAVITY
# Run this script from the hydra-tokens-antigravity directory

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  HYDRA TOKENS ANTIGRAVITY -- Installer v1.2" -ForegroundColor Cyan
Write-Host "  9-Headed Token Economy System for Antigravity IDE" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

$configPath = "$env:USERPROFILE\.gemini\config"
$skillsPath = "$configPath\skills"
$agentsPath = "$configPath\AGENTS.md"

# Check that Antigravity config exists
if (-not (Test-Path $configPath)) {
    Write-Host "[ERROR] Antigravity config not found at: $configPath" -ForegroundColor Red
    Write-Host "Please install Google Antigravity IDE first." -ForegroundColor Red
    exit 1
}

Write-Host "[1/5] Installing HYDRA Skills..." -ForegroundColor Yellow

$skills = @("hydra", "hydra_mcp", "hydra_compress", "hydra_audit")
foreach ($skill in $skills) {
    $src = ".\skills\$skill"
    $dst = "$skillsPath\$skill"
    
    if (Test-Path $src) {
        Copy-Item -Recurse -Force $src $skillsPath
        Write-Host "  [OK] $skill installed" -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] $skill not found at $src" -ForegroundColor DarkYellow
    }
}

Write-Host ""
Write-Host "[2/5] Installing HYDRA Rules to AGENTS.md..." -ForegroundColor Yellow

if (-not (Test-Path $agentsPath)) {
    New-Item -ItemType File -Path $agentsPath -Force | Out-Null
    Write-Host "  [NEW] Created AGENTS.md" -ForegroundColor Cyan
}

$rulesContent = Get-Content ".\rules\AGENTS.md" -Raw -ErrorAction SilentlyContinue
if ($rulesContent) {
    $existingContent = Get-Content $agentsPath -Raw -ErrorAction SilentlyContinue
    if ($existingContent -and $existingContent.Contains("HYDRA TOKENS ANTIGRAVITY")) {
        Write-Host "  [SKIP] HYDRA rules already present in AGENTS.md" -ForegroundColor DarkYellow
    } else {
        Add-Content -Path $agentsPath -Value "`n`n$rulesContent"
        Write-Host "  [OK] HYDRA rules added to AGENTS.md" -ForegroundColor Green
    }
} else {
    Write-Host "  [WARN] rules\AGENTS.md not found" -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "[3/5] Activating HYDRA MCP Tools in Antigravity Panel..." -ForegroundColor Yellow
if (Test-Path ".\activate_hydra_mcp.ps1") {
    powershell -ExecutionPolicy Bypass -File ".\activate_hydra_mcp.ps1"
} else {
    Write-Host "  [WARN] activate_hydra_mcp.ps1 script not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/5] Verifying Installation..." -ForegroundColor Yellow

$installed = 0
foreach ($skill in $skills) {
    $skillFile = "$skillsPath\$skill\SKILL.md"
    if (Test-Path $skillFile) {
        Write-Host "  [OK] $skill - verified" -ForegroundColor Green
        $installed++
    } else {
        Write-Host "  [FAIL] $skill - not found at $skillFile" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "[5/5] Installation Summary" -ForegroundColor Yellow
Write-Host "  Skills installed : $installed / 4" -ForegroundColor White
Write-Host "  Rules installed  : HEAD-5, HEAD-6, HEAD-7" -ForegroundColor White
Write-Host "  MCP Tools Status : AUTO-ACTIVATED (hydra-tools-mcp in mcp_config.json)" -ForegroundColor Green

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  HYDRA installation complete!" -ForegroundColor Green
Write-Host "  Restart Antigravity IDE to activate all 9 heads." -ForegroundColor White
Write-Host ""
Write-Host "  First command to try: hydra audit" -ForegroundColor Yellow
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""
