# Threat model

## Assets

- User tasks, notes, reminders, and knowledge packs under `DRICO_HOME`.
- User-authored plugins in `DRICO_HOME/plugins/`.
- Local git repositories accessed by git tools commands.

## Trust boundaries

| Trust | Components |
|-------|------------|
| Trusted | Python stdlib, Drico built-in plugins in `drico_bot/plugins/`. |
| Semi-trusted | User plugins (`~/.drico/plugins/*.py`) — same privilege as the user running Drico. |
| Untrusted | Downloaded pack archives (validated by SHA-256, license allowlist, zip-slip checks). |
| Remote | Only URLs listed in `drico_bot/data/sources.json` via explicit `packs download`. |

## Out of scope

- Protecting against malicious code the user intentionally installs as a plugin.
- Multi-user machine isolation (single-user desktop model).
- Remote code execution via LLM (no LLM is present).

## Controls (S1–S15 summary)

- File permissions `0700` / `0600` with warnings when loose.
- Path resolution and zip-slip prevention on backup/restore and pack extract.
- Dashboard binds `127.0.0.1`, validates `Host`, CSRF on POST, response security headers, 64 KB POST cap.
- CI runs with `permissions: contents: read` and pinned GitHub Action SHAs.
