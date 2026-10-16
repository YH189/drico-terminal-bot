"""Load ~/.drico/config.toml (stdlib only)."""

import os
import sys
from pathlib import Path

from drico_bot.core.security import secure_mkdir, secure_write_file, warn_data_permissions
from drico_bot.knowledge.pack import get_drico_home

DEFAULT_CONFIG = """\
# Drico configuration

[disabled]
plugins = []
"""


def ensure_drico_home():
    home = get_drico_home()
    secure_mkdir(str(home))
    config_path = home / "config.toml"
    if not config_path.is_file():
        secure_write_file(str(config_path), DEFAULT_CONFIG)
    else:
        try:
            os.chmod(str(config_path), 0o600)
        except OSError:
            pass
    warn_data_permissions(str(home))
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


def _validate_config(data):
    """Return sanitized config; invalid keys fall back with warnings."""
    if not isinstance(data, dict):
        print("Drico > Warning: config.toml root must be a table. Using defaults.")
        return {}
    out = {}
    disabled = data.get("disabled")
    if disabled is None:
        out["disabled"] = {"plugins": []}
    elif not isinstance(disabled, dict):
        print("Drico > Warning: [disabled] must be a table. Ignoring.")
        out["disabled"] = {"plugins": []}
    else:
        plugins = disabled.get("plugins", [])
        if not isinstance(plugins, list):
            print("Drico > Warning: disabled.plugins must be a list. Using [].")
            plugins = []
        else:
            plugins = [p for p in plugins if isinstance(p, str)]
        out["disabled"] = {"plugins": plugins}
    return out


def load_config():
    ensure_drico_home()
    path = get_drico_home() / "config.toml"
    if not path.is_file():
        return _validate_config({})
    try:
        raw = _parse_config_text(path.read_text(encoding="utf-8"))
        return _validate_config(raw)
    except (OSError, ValueError) as exc:
        print("Drico > Warning: could not read config.toml ({0}). Using defaults.".format(exc))
        return _validate_config({})


def get(config, key, default=None):
    """Get a dotted key such as disabled.plugins from parsed config."""
    parts = key.split(".")
    current = config
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
