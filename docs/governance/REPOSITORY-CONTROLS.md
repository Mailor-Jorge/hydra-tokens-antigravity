# REPOSITORY BRANCH & ACCESS CONTROLS AUDIT

---

## 1. Target Controls Configuration (`main` branch)

| Control Parameter | Target Standard | GitHub Free / Team Policy | Status |
|-------------------|-----------------|---------------------------|--------|
| Pull Request Merging | Required | Configurable via Settings | RECOMMENDED |
| Code Owner Reviews | Required (`.github/CODEOWNERS`) | Requires Pro / Org | CONFIGURED IN REPO |
| Force Push Protection | Blocked | Configurable via Ruleset | RECOMMENDED |
| Branch Deletion | Blocked | Configurable via Ruleset | RECOMMENDED |
| Automated Secret Scanning | Active | GitHub Secret Scanning | ACTIVE / VERIFIED |
| Forensic Bundle Exclusions | `.evidence/`, `*.bundle` in `.gitignore` | Enforced locally | VERIFIED |
