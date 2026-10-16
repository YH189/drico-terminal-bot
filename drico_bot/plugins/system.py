"""Setup, doctor, where, examples, reset, and per-command help (Phase 13)."""

import shutil

from drico_bot.core.confirm import confirm_typed
from drico_bot.core.config import ensure_drico_home
from drico_bot.core.doctor import run_doctor
from drico_bot.core.registry import Command
from drico_bot.core.security import secure_mkdir
from drico_bot.knowledge.pack import get_drico_home, get_knowledge_db_path, get_packs_root


EXAMPLES = [
    ("ask what is BM25", "Search knowledge packs"),
    ("task add Write docs", "Add a task"),
    ("git summary", "Repository overview"),
    ("packs list", "List knowledge packs"),
    ("dashboard", "Open local task dashboard"),
    ("doctor", "Run environment checks"),
]


def _handle_setup(context):
    home = ensure_drico_home()
    secure_mkdir(str(home / "plugins"))
    secure_mkdir(str(get_packs_root()))
    print("Drico > Setup complete at {0}.\n".format(home))


def _handle_doctor(context):
    print(run_doctor())
    print()


def _handle_where(context):
    home = get_drico_home()
    print("Drico > Paths:")
    print("  home: {0}".format(home))
    print("  config: {0}".format(home / "config.toml"))
    print("  database: {0}".format(home / "drico.db"))
    print("  knowledge: {0}".format(get_knowledge_db_path()))
    print("  packs: {0}".format(get_packs_root()))
    print("  plugins: {0}".format(home / "plugins"))
    print()


def _handle_examples(context):
    print("Drico > Examples:\n")
    for cmd, desc in EXAMPLES:
        print("  {0}  — {1}".format(cmd, desc))
    print()


def _handle_reset(context):
    parts = context.normalized.split()
    if len(parts) < 2 or parts[1] != "--all":
        print("Drico > Usage: reset --all (type DELETE to confirm)\n")
        return
    if not confirm_typed("Type DELETE to erase all data under DRICO_HOME: ", "DELETE"):
        print("Drico > Cancelled.\n")
        return
    home = get_drico_home()
    if home.is_dir():
        shutil.rmtree(home)
    print("Drico > Reset complete.\n")


def _match_help_command(context):
    return context.normalized.startswith("help ") and len(context.normalized) > 5


def _handle_help_command(context):
    query = context.normalized.split(None, 1)[1].strip().lower()
    command = context.session.registry.find(query)
    if command is None:
        print("Drico > No help for '{0}'.\n".format(query))
        return
    names = [command.name] + list(command.aliases)
    print("Drico > {0}".format(" / ".join(names)))
    if command.help_text:
        print("  {0}".format(command.help_text))
    print()


def register(registry):
    registry.register(
        Command(
            name="setup",
            handler=_handle_setup,
            help_text="Create ~/.drico layout and defaults.",
            category="system",
        )
    )
    registry.register(
        Command(
            name="doctor",
            handler=_handle_doctor,
            help_text="Check Python, paths, and data permissions.",
            category="system",
        )
    )
    registry.register(
        Command(
            name="where",
            handler=_handle_where,
            help_text="Show important Drico paths.",
            category="system",
        )
    )
    registry.register(
        Command(
            name="examples",
            handler=_handle_examples,
            help_text="Show example commands.",
            category="system",
        )
    )
    registry.register(
        Command(
            name="reset",
            handler=_handle_reset,
            help_text="reset --all erases DRICO_HOME (confirm DELETE).",
            category="system",
            destructive=True,
        )
    )
    registry.register(
        Command(
            name="help_command",
            handler=_handle_help_command,
            help_text="help <command> details.",
            category="system",
            match_fn=_match_help_command,
            priority=15,
            show_in_help=False,
        )
    )
