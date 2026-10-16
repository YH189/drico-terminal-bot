# Security policy

Drico (`drico-terminal-bot`) is an offline, stdlib-only developer toolkit. Report issues privately to the repository owner.

## Supported versions

Security fixes apply to the latest `main` branch.

## Design principles

- No network access except `drico_bot/knowledge/download.py` for curated pack downloads from `sources.json`.
- No `eval`, `exec`, `pickle`, or `shell=True`.
- Parameterized SQL only.
- Destructive actions require confirmation (`reset --all` requires typing `DELETE`).
- User data lives under `DRICO_HOME` (default `~/.drico/`). Never commit databases, packs, or personal exports.

## Reporting

Include steps to reproduce, Python version, and whether user plugins are in use. Do not include secrets or full database dumps.
