"""Load built-in plugins from drico_bot/plugins/."""

import importlib
from pathlib import Path

from drico_bot.core.config import get


def load_builtin_plugins(registry, config, plugins_dir=None):
    if plugins_dir is None:
        plugins_dir = Path(__file__).resolve().parent.parent / "plugins"
    else:
        plugins_dir = Path(plugins_dir)
    disabled = set(get(config, "disabled.plugins", []) or [])

    for path in sorted(plugins_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        stem = path.stem
        plugin_path = str(path.resolve())
        if stem in disabled:
            registry.record_plugin(stem, "disabled", plugin_path)
            continue
        module_name = "drico_bot.plugins.{0}".format(stem)
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            print(
                "Drico > Warning: failed to load plugin {0}: {1}".format(stem, exc)
            )
            registry.record_plugin(stem, "error", plugin_path)
            continue
        try:
            if hasattr(module, "register"):
                module.register(registry)
        except Exception as exc:
            print(
                "Drico > Warning: failed to register plugin {0}: {1}".format(stem, exc)
            )
            registry.record_plugin(stem, "error", plugin_path)
            continue
        registry.record_plugin(stem, "loaded", plugin_path)
