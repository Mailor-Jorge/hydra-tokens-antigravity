# AGPL-3.0 NETWORK INTERACTION & COMPLIANCE ASSESSMENT

---

## 1. Network Interaction Applicability
- **Direct Remote Network Interaction Applicable:** **NO (Currently Local Stdio / IPC)**
- **Component Analysis:**
  - `hydra_mcp_server.py`: Operates purely over local standard input/output (`stdio`) JSON-RPC processes spawned by the local Antigravity IDE host.
  - Skills & Rules (`skills/`, `rules/`): Evaluated within the agentic context of the local IDE host.
  - No HTTP web server, REST API, or SaaS endpoint is hosted or exposed by this codebase.

## 2. Remote Deployment Scenario & Source-Access Safeguard
If an entity or developer wraps `hydra-tools-mcp` or HYDRA core modules behind a remote network service (e.g., a shared corporate MCP HTTP proxy or SaaS API), **Section 13 of the AGPL-3.0 applies**:
- The operator must provide prominent network-accessible means for users to download the Corresponding Source code of the modified version.
- **Source Access Location:** Official public source code must remain accessible at:  
  `https://github.com/Mailor-Jorge/hydra-tokens-antigravity`

## 3. Residual Risks & Status
- **Compliance Status:** VERIFIED (local execution compliant; network disclosure requirements documented).
