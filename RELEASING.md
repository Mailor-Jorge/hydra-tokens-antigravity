# RELEASE GOVERNANCE & GATES

**Project:** HYDRA TOKENS ANTIGRAVITY  
**Release Authority:** Mailor-Jorge  

---

## 1. Versioning Standard
This project adheres to **Semantic Versioning 2.0.0 (SemVer)**:
`MAJOR.MINOR.PATCH`

- **MAJOR:** Incompatible architectural shifts, breaking rule syntax, breaking MCP tool schema.
- **MINOR:** Backward-compatible new tools, additional skills, non-breaking features.
- **PATCH:** Bug fixes, documentation updates, security patches.

---

## 2. Mandatory Pre-Release Gates

Before tagging and publishing any release:
1. **Repository Cleanliness:** No unstaged or untracked development residue.
2. **Secret Scan:** Clean git grep secret check.
3. **Syntax / Compile Check:** Python MCP server syntax validation (`py_compile`).
4. **License Integrity:** Canonical AGPL-3.0 in place, notices intact.
5. **NPM Package Parity:** `package.json` version matches release git tag.

---

## 3. Release Artifacts & Integrity
- Every release tag must be immutable.
- NPM tarballs must record SHA-512 integrity hashes.
