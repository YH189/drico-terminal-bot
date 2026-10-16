"""Load ~/.drico/config.toml (stdlib only)."""

import sys
from pathlib import Path

from drico_bot.knowledge.pack import get_drico_home

DEFAULT_CONFIG = """\
# Drico configuration

[disabled]
plugins = []
"""


def ensure_drico_home():
    home = get_drico_home()
    home.mkdir(parents=True, exist_ok=True)
    config_path = home / "config.toml"
    if not config_path.is_file():
        config_path.write_text(DEFAULT_CONFIG, encoding="utf-8")
    return home


def _parse_toml_simple(text):
    """Minimal TOML subset for string and string-list values."""
    data = {}
    section = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip()
            data.setdefault(section, {})
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        target = data if section is None else data.setdefault(section, {})
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if not inner:
                target[key] = []
            else:
                parts = []
                for item in inner.split(","):
                    item = item.strip().strip('"').strip("'")
                    if item:
                        parts.append(item)
                target[key] = parts
        else:
            target[key] = value.strip('"').strip("'")
    return data


def _parse_config_text(text):
    if sys.version_info >= (3, 11):
        import tomllib

        return tomllib.loads(text)
    return _parse_toml_simple(text)


def load_config():
    ensure_drico_home()
    path = get_drico_home() / "config.toml"
    if not path.is_file():
        return {}
    try:
        return _parse_config_text(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def get(config, key, default=None):
    """Get a dotted key such as disabled.plugins from parsed config."""
    parts = key.split(".")
    current = config
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
