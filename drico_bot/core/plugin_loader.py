"""Load built-in plugins from drico_bot/plugins/."""

import importlib
from pathlib import Path

from drico_bot.core.config import get


def load_builtin_plugins(registry, config):
    plugins_dir = Path(__file__).resolve().parent.parent / "plugins"
    disabled = set(get(config, "disabled.plugins", []) or [])

    for path in sorted(plugins_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        stem = path.stem
        if stem in disabled:
            registry.record_plugin(stem, "disabled")
            continue
        module_name = "drico_bot.plugins.{0}".format(stem)
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            print(
                "Drico > Warning: failed to load plugin {0}: {1}".format(stem, exc)
            )
            registry.record_plugin(stem, "error")
            continue
        try:
            if hasattr(module, "register"):
                module.register(registry)
        except Exception as exc:
            print(
                "Drico > Warning: failed to register plugin {0}: {1}".format(stem, exc)
            )
            registry.record_plugin(stem, "error")
            continue
        registry.record_plugin(stem, "loaded")
