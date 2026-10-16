# Drico specification

This document is the source of truth for Drico (`drico-terminal-bot`). If this file conflicts with any other note, **the stricter rule wins**.

## Non-negotiable rules

1. **Zero cost** — Python standard library only. No new dependencies. No paid services, accounts, API keys, or telemetry.
2. **No LLM** — No Ollama, OpenAI, Anthropic, Hugging Face, Gemini, or any AI model/API.
3. **Offline** — No network except Phase 11 `pack download` from `drico_bot/data/sources.json` with license, size cap, and SHA-256 verification.
4. **No eval/exec/pickle/shell=True** — Parameterized SQL only. Subprocess with argument lists.
5. **Honest output** — Cite sources for knowledge answers; say when nothing matches.
6. **Safety** — Confirm destructive actions (default no). No overwrite without confirmation.
7. **Privacy** — Data under `~/.drico/` (`DRICO_HOME`). Never commit personal data, `.db`, packs, logs, backups.
8. **Compatibility** — Python 3.8+ (3.10 primary). No `str.removeprefix` in new code; use slicing.
9. **Tests** — pytest; CI on Ubuntu 3.10 and 3.12. Never weaken tests to pass.

## Security charter (S1–S15)

- **S1** Data dirs `0700`, secret files `0600`; warn if looser.
- **S2** User-only; no sudo; no system file changes.
- **S3** No network except Phase 11 download module.
- **S4** Input limits: command 1000 chars; note/task 5000; file read 1 MB; regex pattern 200; regex text 100 KB.
- **S5** Paths resolved; no escape from allowed roots; no symlink escape when indexing.
- **S6** Parameterized SQL only.
- **S7** Subprocess argv only; env allowlist for `run`.
- **S8** Mask secrets (first 4 chars only); never log full secrets.
- **S9** Confirm delete/overwrite/restore/undo/hooks/schedule destructive/macro destructive.
- **S10** Short errors; stack traces only with `DRICO_DEBUG=1`.
- **S11** Defensive security content only.
- **S12** Free licenses only for packs (allowlist in Phase 11).
- **S13** Plugins only from repo `drico_bot/plugins/` and `~/.drico/plugins/`; show paths in `plugins` output.
- **S14** CI `permissions: contents: read`; pinned action SHAs.
- **S15** Dashboard: localhost only, Host allowlist, CSRF on POST, security headers, 64 KB POST limit.

## Public usefulness (U1–U7)

- **U1** Free for everyone.
- **U2** Offline-first Ubuntu; graceful degradation.
- **U3** `NO_COLOR`, plain theme, accessible output.
- **U4** `drico setup`, `help <command>`, `examples`.
- **U5** `where`, `reset --all` (type DELETE).
- **U6** README, SECURITY.md, THREAT_MODEL.md.
- **U7** Actionable error messages.

## Phases (summary)

| Phase | Scope |
|-------|--------|
| 1 | Plugin registry, dispatcher, config, built-in plugins, snapshots |
| 2 | Bug fixes: llm alias, tool count, word boundaries, dynamic help, DRICO_NO_DELAY |
| 3 | AST calculator, utilities (json, base64, hash, uuid, timestamp, hex, bin, dec, regex) |
| 4 | SQLite tasks/notes/focus/remind/brief/backup/restore/export/import/schedule/templates |
| 5 | Knowledge: index folder, synonyms, phrases, project-first, watch |
| 6 | Code intelligence: explain-file, complexity, secrets, deps, todos, loc, largefiles |
| 7 | Git tools: summary, hotspots, blame, stale-branches, undo-last, hooks |
| 8 | Macros, safe `run` whitelist, logs |
| 9 | User plugins `~/.drico/plugins/` |
| 10 | readline, ANSI themes, notify-send |
| 11 | `pack download` from sources.json only |
| 12 | Local dashboard 127.0.0.1:8765 |
| 13 | doctor, packaging, docs, final security review |

Full acceptance criteria match the owner’s autonomous run prompt (Phases 1–13 detailed requirements).

## Allowed pack licenses (Phase 11)

CC0-1.0, CC-BY-4.0, CC-BY-SA-4.0, MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, PSF-2.0, Public-Domain.
