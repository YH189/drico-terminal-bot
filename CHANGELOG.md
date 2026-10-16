# Changelog

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
