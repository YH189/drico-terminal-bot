import pathlib

from drico_bot.core.config import load_config
from drico_bot.core.plugin_loader import load_builtin_plugins, load_user_plugins
from drico_bot.core.registry import Registry


def _status_map(registry):
    return {
        entry.name: (entry.status, entry.path)
        for entry in registry.plugin_statuses()
    }


def test_user_plugin_loads(drico_home):
    plugins_dir = pathlib.Path(drico_home) / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    (plugins_dir / "hello_user.py").write_text(
        '''
from drico_bot.core.registry import Command

def register(registry):
    registry.register(
        Command(
            name="hello-user",
            handler=lambda ctx: print("Drico > Hello from user plugin.\\n"),
            help_text="Sample user plugin command.",
            category="user",
        )
    )
''',
        encoding="utf-8",
    )
    registry = Registry()
    config = load_config()
    load_user_plugins(registry, config)
    status, path = _status_map(registry)["hello_user"]
    assert status == "loaded"
    assert path.endswith("hello_user.py")
    command = registry.find("hello-user")
    assert command is not None


def test_broken_user_plugin_isolated(drico_home):
    plugins_dir = pathlib.Path(drico_home) / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    (plugins_dir / "broken_user.py").write_text(
        "raise RuntimeError('boom')\n",
        encoding="utf-8",
    )
    (plugins_dir / "good_user.py").write_text(
        '''
from drico_bot.core.registry import Command

def register(registry):
    registry.register(
        Command(
            name="good-user",
            handler=lambda ctx: None,
            help_text="Still loads.",
            category="user",
        )
    )
''',
        encoding="utf-8",
    )
    registry = Registry()
    load_user_plugins(registry, load_config())
    statuses = _status_map(registry)
    assert statuses["broken_user"][0] == "error"
    assert statuses["good_user"][0] == "loaded"
    assert registry.find("good-user") is not None


def test_disabled_user_plugin(drico_home):
    plugins_dir = pathlib.Path(drico_home) / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    (plugins_dir / "skip_me.py").write_text(
        '''
from drico_bot.core.registry import Command

def register(registry):
    registry.register(
        Command(
            name="skip-me",
            handler=lambda ctx: None,
            help_text="Should not load.",
            category="user",
        )
    )
''',
        encoding="utf-8",
    )
    config_path = pathlib.Path(drico_home) / "config.toml"
    config_path.write_text(
        '[disabled]\nplugins = ["skip_me"]\n',
        encoding="utf-8",
    )
    registry = Registry()
    load_user_plugins(registry, load_config())
    assert _status_map(registry)["skip_me"][0] == "disabled"
    assert registry.find("skip-me") is None


def test_builtin_plugins_record_paths(drico_home):
    registry = Registry()
    load_builtin_plugins(registry, load_config())
    basics = next(
        entry for entry in registry.plugin_statuses() if entry.name == "basics"
    )
    assert basics.status == "loaded"
    assert basics.path.endswith("basics.py")


def test_build_registry_loads_user_plugins(drico_home):
    plugins_dir = pathlib.Path(drico_home) / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    (plugins_dir / "from_bootstrap.py").write_text(
        '''
from drico_bot.core.registry import Command

def register(registry):
    registry.register(
        Command(
            name="from-bootstrap",
            handler=lambda ctx: None,
            help_text="Loaded via bootstrap.",
            category="user",
        )
    )
''',
        encoding="utf-8",
    )
    from drico_bot.core.bootstrap import build_registry

    registry = build_registry()
    assert _status_map(registry)["from_bootstrap"][0] == "loaded"
    assert registry.find("from-bootstrap") is not None
