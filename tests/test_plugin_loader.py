from drico_bot.core.config import load_config
from drico_bot.core.plugin_loader import load_builtin_plugins
from drico_bot.core.registry import Registry


def test_builtin_plugins_load(drico_home):
    registry = Registry()
    load_builtin_plugins(registry, load_config())
    names = {entry.name for entry in registry.plugin_statuses()}
    assert "basics" in names
    assert "tools" in names
    assert "knowledge" in names


def test_disabled_plugin_skipped(drico_home, monkeypatch):
    config_path = __import__("pathlib").Path(drico_home) / "config.toml"
    config_path.write_text(
        "[disabled]\nplugins = [\"calculator\"]\n",
        encoding="utf-8",
    )
    registry = Registry()
    load_builtin_plugins(registry, load_config())
    statuses = {entry.name: entry.status for entry in registry.plugin_statuses()}
    assert statuses.get("calculator") == "disabled"
