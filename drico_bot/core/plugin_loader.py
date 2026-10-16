"""Load built-in and user plugins."""

import importlib
import importlib.util
import sys
from pathlib import Path

from drico_bot.core.config import get
from drico_bot.knowledge.pack import get_drico_home


def _disabled_plugins(config):
    return set(get(config, "disabled.plugins", []) or [])


def _record_and_load(registry, path, stem, disabled, load_module):
    path_str = str(path)
    if stem in disabled:
        registry.record_plugin(stem, "disabled", path_str)
        return
    try:
        module = load_module(path, stem)
    except Exception as exc:
        print(
            "Drico > Warning: failed to load plugin {0}: {1}".format(stem, exc)
        )
        registry.record_plugin(stem, "error", path_str)
        return
    try:
        if hasattr(module, "register"):
            module.register(registry)
    except Exception as exc:
        print(
            "Drico > Warning: failed to register plugin {0}: {1}".format(stem, exc)
        )
        registry.record_plugin(stem, "error", path_str)
        return
    registry.record_plugin(stem, "loaded", path_str)


def load_builtin_plugins(registry, config):
    plugins_dir = Path(__file__).resolve().parent.parent / "plugins"
    disabled = _disabled_plugins(config)

    for path in sorted(plugins_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        stem = path.stem

        def load_module(_path, plugin_stem):
            module_name = "drico_bot.plugins.{0}".format(plugin_stem)
            return importlib.import_module(module_name)

        _record_and_load(registry, path, stem, disabled, load_module)


def _import_user_plugin(path, stem):
    module_name = "drico_user_plugin.{0}".format(stem)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load spec for {0}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_user_plugins(registry, config):
    plugins_dir = get_drico_home() / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    disabled = _disabled_plugins(config)

    for path in sorted(plugins_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        stem = path.stem

        def load_module(plugin_path, plugin_stem):
            return _import_user_plugin(plugin_path, plugin_stem)

        _record_and_load(registry, path, stem, disabled, load_module)
