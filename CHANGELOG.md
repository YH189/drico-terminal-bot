# Changelog

## Phase 6: Code intelligence

- Commands (indexed project only): `explain-file`, `complexity`, `secrets` (masked), `deps`, `todos`, `loc`, `largefiles`.
- Paths must stay under the current indexed project root; symlink escape blocked.
- Python cyclomatic complexity, manifest parsing (`requirements.txt`, `pyproject.toml`, `package.json`), TODO/FIXME scan, LOC by extension, large-file listing (default 100 KB).

## Phase 5: Knowledge indexing, synonyms, phrases, project-first search

- `index <folder>` syncs `.txt`/`.md`/`.jsonl` into a per-project pack (skips `.git`, `node_modules`, `__pycache__`, `venv`, hidden paths, binaries, files over 1 MB; blocks symlink escape).
- `~/.drico/synonyms.json` validated on load; query terms expand through synonym lists.
- `ask` honors quoted phrases and searches the current project pack before global packs.
- `watch <folder>` polls mtimes every 5 seconds and re-indexes on change (Ctrl+C to stop).

## Phase 4: Productivity SQLite and commands

- SQLite `drico.db` for tasks (with dependencies, blocked/next, cycle detection), notes, reminders, and focus state.
- Commands: task, note, focus, remind, brief, backup/restore (zip-slip safe), export/import (MD/CSV with formula escape), schedule (crontab argv + `# drico:` marker), `new` templates (`python-cli`, `python-package`, `fastapi-basic`).
- `ensure_db` wired in bootstrap; reminder checks each interactive loop iteration.

## Phase 3: Safe calculator and utilities

- AST calculator (`drico_bot/calc/safe_eval.py`) with whitelist and limits.
- Utilities plugin: json, base64, hash sha256, uuid, timestamp, hex, bin, dec, regex.

## Phase 2: Bug fixes

- `large language models` alias maps to `llm`.
- `tool count` prints total tools.
- Reference commands use word boundaries.
- `show`/`help` generated from registry.
- Loading delay skipped when `DRICO_NO_DELAY` or stdout is not a TTY.

## Phase 1: Plugin architecture and refactor

- Core registry, dispatcher, config, plugin loader, and built-in plugins.
- Security: input length limits, directory/file permissions, config validation, plugin path listing, handler error isolation.
