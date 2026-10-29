# NotebookLM status (2026-10-29)
Notebook bd2a2bb3-8af9-477f-b29f-daba938ca3bd could NOT be queried.
- `nlm login --check` says the credentials are valid, but every API call (CLI and MCP) returns "Authentication expired".
- MCP refresh_auth did not fix it.
- The user needs to re-login interactively in a browser (`nlm login --clear`).

Fallback: the six .md files in the project root look like exports from this notebook (they carry NotebookLM-style numeric citations), so they are used as a proxy for it. Artifacts 927e0f8a… and 03dce093… have not been read.
