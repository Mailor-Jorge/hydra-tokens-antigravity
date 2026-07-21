# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-07-21

### Added
- **3 New MCP Tools** (total: 6 tools)
  - `hydra_snippet` — Extract specific functions/classes from files (-90% tokens on file reads)
  - `hydra_cache` — Save/retrieve/list/delete cached responses (-100% on repeated questions)
  - `hydra_context_snapshot` — Scan directories and report token cost per file
- **HEAD-8 HYDRA_TRUNCATE** — Manual output limiter (`hydra limit N` / `hydra limit off`)
- **Diff-only mode** (HEAD-5.7) — Always active, never re-output entire file on edits
- **Snippet-first rule** (HEAD-6.7) — Ask before loading full files
- **Cache check rule** (HEAD-6.8) — Check cache before generating repeated answers
- **Context snapshot cycle** (HEAD-6.4) — Automatic scan every 15 turns
- **WALKTHROUGH.md** — Complete guide from first install to advanced usage (PT-BR)
- **Expanded Interactive Protocol** — 6 confirmation prompts (from 3)
- **11 Quick Commands** (from 5)

### Changed
- README.md updated with v1.1.0 badges, 6 tools table, expanded commands
- NPM package `@mailoko/hydra-tools-mcp` bumped to 1.1.0
- Python MCP server `hydra_mcp_server.py` expanded from 3 to 6 handlers
- `hydra_mcp/SKILL.md` expanded with snippet, cache, snapshot protocols

## [1.0.2] - 2026-07-21

### Fixed
- NPM package metadata corrections

## [1.0.1] - 2026-07-21

### Fixed
- Initial NPM publish corrections

## [1.0.0] - 2026-07-21

### Added
- Initial release with 9-headed architecture
- 4 Skills: hydra, hydra_mcp, hydra_compress, hydra_audit
- 3 Rules: OUTPUT_FORMAT, CONTEXT_GUARD, NO_REPEAT
- 3 MCP Tools: hydra_filter_log, hydra_token_estimate, hydra_clean_scratch
- NPM package `@mailoko/hydra-tools-mcp`
- Full documentation: README, INSTALL, ARCHITECTURE, CHANGELOG
- GitHub Actions CI/CD pipeline
- PowerShell installer script
