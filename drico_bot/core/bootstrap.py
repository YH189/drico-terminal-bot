"""Build registry and run knowledge CLI."""

import sys

from drico_bot.core.config import ensure_drico_home, load_config
from drico_bot.core.plugin_loader import load_builtin_plugins
from drico_bot.core.registry import Registry


def build_registry():
    ensure_drico_home()
    config = load_config()
    registry = Registry()
    load_builtin_plugins(registry, config)
    return registry


def run_cli(argv):
    from drico_bot.plugins.knowledge import run_cli as knowledge_run_cli

    registry = build_registry()
    return knowledge_run_cli(argv, registry=registry)
