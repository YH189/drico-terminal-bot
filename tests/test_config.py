from pathlib import Path

from drico_bot.core.config import ensure_drico_home, get, load_config


def test_ensure_drico_home_creates_config(drico_home, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", drico_home)
    path = ensure_drico_home()
    assert path == Path(drico_home)
    assert (path / "config.toml").is_file()


def test_get_dotted_key(drico_home, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", drico_home)
    home = ensure_drico_home()
    (home / "config.toml").write_text(
        "[disabled]\nplugins = [\"test\"]\n",
        encoding="utf-8",
    )
    config = load_config()
    assert get(config, "disabled.plugins") == ["test"]
